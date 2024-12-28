class TextProcessor:
    @staticmethod
    def chunk_text(text, max_chunk_size=2000):  # Reduced from 4000 to 2000
        """Split text into smaller chunks while preserving context"""
        chunks = []
        current_chunk = ""
        
        # Split by double newlines to preserve paragraph structure
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < max_chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        # Normalize newlines
        text = text.replace('\r\n', '\n')
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
        # Truncate extremely long lines
        lines = text.split('\n')
        truncated_lines = [line[:1000] if len(line) > 1000 else line for line in lines]
        return '\n'.join(truncated_lines)