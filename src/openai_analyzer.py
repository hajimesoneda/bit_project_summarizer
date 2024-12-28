from src.services.openai_service import OpenAIService
from src.text_processor import TextProcessor
import time

class TenderAnalyzer:
    def __init__(self, api_key):
        self.openai_service = OpenAIService(api_key)
        self.text_processor = TextProcessor()
    
    def analyze_tender(self, text):
        cleaned_text = self.text_processor.clean_text(text)
        text_chunks = self.text_processor.chunk_text(cleaned_text)
        
        all_info = []
        for chunk in text_chunks:
            chunk_info = self.openai_service.analyze_chunk(chunk)
            if chunk_info:
                all_info.append(chunk_info)
            time.sleep(1)
        
        if all_info:
            return self.openai_service.consolidate_results(all_info)
        return None