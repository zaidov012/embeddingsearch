from typing import List, Tuple, Dict
from pypdf import PdfReader
import io
import re
from config import settings


class DocumentProcessor:
    """Service for processing PDF documents."""
    
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
        self.max_chunk_size = settings.CHUNK_SIZE * 3  # Maximum size before force-splitting
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _detect_headers(self, text: str) -> List[Dict[str, any]]:
        """
        Detect headers and subheaders in text using common patterns.
        Returns list of dicts with header info: {position, level, text}
        """
        headers = []
        lines = text.split('\n')
        current_pos = 0
        
        # Common header patterns
        patterns = [
            # Numbered headers: 1. Title, 1.1 Subtitle, etc.
            (r'^(\d+\.(?:\d+\.)*)\s+(.+)$', 1),
            # Roman numerals: I. Title, II. Title
            (r'^([IVXLCDM]+)\.\s+(.+)$', 1),
            # Lettered headers: A. Title, B. Title
            (r'^([A-Z])\.\s+(.+)$', 2),
            # ALL CAPS headers (minimum 3 words or 15 chars)
            (r'^([A-Z][A-Z\s]{14,})$', 1),
            # Title Case headers (3+ consecutive capitalized words)
            (r'^((?:[A-Z][a-z]+\s+){2,}[A-Z][a-z]+)$', 2),
            # Headers ending with colon
            (r'^(.{3,50}):$', 2),
            # Chapter/Section keywords
            (r'^(Chapter|Section|Part|Article|Appendix)\s+(\d+|[IVXLCDM]+|[A-Z])[\s:-]*(.*)$', 1),
        ]
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Skip empty lines or very short lines
            if len(line_stripped) < 3:
                current_pos += len(line) + 1
                continue
            
            # Check each pattern
            for pattern, default_level in patterns:
                match = re.match(pattern, line_stripped)
                if match:
                    # Determine header level based on indentation and pattern
                    indent_level = len(line) - len(line.lstrip())
                    level = default_level + (indent_level // 4)  # Adjust level by indentation
                    
                    headers.append({
                        'position': current_pos,
                        'level': min(level, 3),  # Cap at level 3
                        'text': line_stripped,
                        'line_num': i
                    })
                    break
            
            current_pos += len(line) + 1
        
        return headers
    
    def _split_by_headers(self, text: str) -> List[Tuple[str, Dict[str, any]]]:
        """
        Split text by detected headers.
        Returns list of tuples: (chunk_text, metadata)
        """
        headers = self._detect_headers(text)
        
        if not headers:
            # No headers detected, fall back to paragraph-based chunking
            return self._split_by_paragraphs(text)
        
        chunks = []
        
        # Split text at each header
        for i, header in enumerate(headers):
            start_pos = header['position']
            
            # Find end position (next header or end of text)
            if i < len(headers) - 1:
                end_pos = headers[i + 1]['position']
            else:
                end_pos = len(text)
            
            section_text = text[start_pos:end_pos].strip()
            
            # If section is too large, split it further
            if len(section_text) > self.max_chunk_size:
                sub_chunks = self._split_large_section(section_text, header)
                chunks.extend(sub_chunks)
            else:
                chunks.append((section_text, {
                    'header': header['text'],
                    'header_level': header['level']
                }))
        
        return chunks
    
    def _split_large_section(self, text: str, header: Dict) -> List[Tuple[str, Dict]]:
        """Split a large section into smaller chunks while preserving context."""
        chunks = []
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        header_text = header['text']
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If adding this paragraph exceeds max size, save current chunk
            if current_chunk and len(current_chunk) + len(para) > self.max_chunk_size:
                chunks.append((current_chunk.strip(), {
                    'header': header_text,
                    'header_level': header['level'],
                    'is_partial': True
                }))
                current_chunk = para + "\n\n"
            else:
                current_chunk += para + "\n\n"
        
        # Add remaining text
        if current_chunk.strip():
            chunks.append((current_chunk.strip(), {
                'header': header_text,
                'header_level': header['level'],
                'is_partial': len(chunks) > 0
            }))
        
        return chunks
    
    def _split_by_paragraphs(self, text: str) -> List[Tuple[str, Dict]]:
        """
        Fallback method: split by paragraphs when no headers detected.
        """
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If adding this paragraph exceeds target size, save current chunk
            if current_chunk and len(current_chunk) + len(para) > self.chunk_size:
                chunks.append((current_chunk.strip(), {'type': 'paragraph_group'}))
                current_chunk = para + "\n\n"
            else:
                current_chunk += para + "\n\n"
        
        # Add remaining text
        if current_chunk.strip():
            chunks.append((current_chunk.strip(), {'type': 'paragraph_group'}))
        
        return chunks
    
    def chunk_text(self, text: str) -> List[Tuple[str, int]]:
        """
        Split text into chunks by headers/structure.
        Returns list of tuples: (chunk_text, chunk_index)
        
        This is the main chunking method that uses header-based splitting.
        """
        if not text:
            return []
        
        # Get chunks with metadata
        chunks_with_meta = self._split_by_headers(text)
        
        # Convert to simple format with index
        indexed_chunks = []
        for i, (chunk_text, metadata) in enumerate(chunks_with_meta):
            if chunk_text.strip():
                indexed_chunks.append((chunk_text, i))
        
        return indexed_chunks
    
    def process_pdf(self, pdf_content: bytes, filename: str) -> List[dict]:
        """
        Process PDF: extract text, chunk it by headers/structure, and prepare for embedding.
        Returns list of chunk dictionaries with metadata.
        """
        text = self.extract_text_from_pdf(pdf_content)
        
        # Get chunks with metadata using header-based splitting
        chunks_with_meta = self._split_by_headers(text)
        
        processed_chunks = []
        for chunk_index, (chunk_text, metadata) in enumerate(chunks_with_meta):
            if chunk_text.strip():  # Only include non-empty chunks
                chunk_data = {
                    "text": chunk_text,
                    "chunk_index": chunk_index,
                    "filename": filename
                }
                
                # Add header information if available
                if 'header' in metadata:
                    chunk_data['header'] = metadata['header']
                    chunk_data['header_level'] = metadata.get('header_level', 0)
                    chunk_data['is_partial'] = metadata.get('is_partial', False)
                elif 'type' in metadata:
                    chunk_data['chunk_type'] = metadata['type']
                
                processed_chunks.append(chunk_data)
        
        return processed_chunks


# Singleton instance
document_processor = DocumentProcessor()
