"""OpenAI API service for tender analysis"""
from openai import OpenAI
import json
import os
import logging
from typing import Optional, List
from src.services.prompt_builder import PromptBuilder
from src.services.response_validator import ResponseValidator
from src.models.tender_response import TenderResponse

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI APIキーが設定されていません")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv('GPT_MODEL', 'gpt-4')
        self.prompt_builder = PromptBuilder()
        self.validator = ResponseValidator()
    
    def analyze_chunk(self, text: str) -> Optional[TenderResponse]:
        """テキストチャンクを分析"""
        if not text.strip():
            logger.warning("Empty text chunk received")
            return None
        
        try:
            response = self._make_openai_request(
                system_content=self.prompt_builder.build_system_prompt(),
                user_content=f"以下の文書を分析してください:\n\n{text}"
            )
            
            # レスポンスのログ出力
            logger.info(f"OpenAI Response:\n{response}")
            
            # レスポンスの検証と変換
            validated_response = self.validator.validate_and_clean(json.loads(response))
            if validated_response:
                logger.info(f"Validated response: {validated_response.to_dict()}")
            return validated_response
            
        except Exception as e:
            logger.error(f"Error analyzing chunk: {str(e)}")
            return None

    def consolidate_results(self, results: List[TenderResponse]) -> Optional[TenderResponse]:
        """複数の分析結果を統合"""
        if not results:
            logger.warning("No results to consolidate")
            return None

        try:
            results_dict = [result.to_dict() for result in results]
            response = self._make_openai_request(
                system_content="あなたは入札案件の分析結果を統合する専門家です。",
                user_content=self.prompt_builder.build_consolidation_prompt(results_dict)
            )
            
            # レスポンスの検証と変換
            return self.validator.validate_and_clean(json.loads(response))
            
        except Exception as e:
            logger.error(f"Error consolidating results: {str(e)}")
            return results[0] if results else None

    def _make_openai_request(self, system_content: str, user_content: str) -> str:
        """OpenAI APIリクエストを実行"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content.strip()