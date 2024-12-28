"""OpenAI prompt builder for tender analysis"""
import json
from typing import Dict, Any, List
from src.models.tender_fields import TENDER_FIELDS
from src.services.prompt_templates import SYSTEM_PROMPT_TEMPLATE, CONSOLIDATION_PROMPT_TEMPLATE

class PromptBuilder:
    def __init__(self):
        self.response_format = self._create_response_format()
    
    def build_system_prompt(self) -> str:
        """システムプロンプトを構築"""
        field_instructions = self._build_field_instructions()
        return SYSTEM_PROMPT_TEMPLATE.format(
            field_instructions=field_instructions,
            response_format=self.response_format
        )

    def build_consolidation_prompt(self, results: List[Dict[str, Any]]) -> str:
        """結果統合用のプロンプトを構築"""
        results_json = json.dumps(results, ensure_ascii=False, indent=2)
        return CONSOLIDATION_PROMPT_TEMPLATE.format(
            results=results_json,
            response_format=self.response_format
        )

    def _build_field_instructions(self) -> str:
        """フィールドごとの抽出指示を構築"""
        instructions = []
        for field in TENDER_FIELDS.values():
            instruction = (
                f"【{field.name}】\n"
                f"- 探すキーワード: {', '.join(field.keywords)}\n"
                f"- 抽出ルール: {field.extraction_rules}\n"
            )
            instructions.append(instruction)
        return ''.join(instructions)

    def _create_response_format(self) -> str:
        """応答フォーマットのテンプレートを作成"""
        template = {
            "項目": {
                f.name: {"見出し": f.name, "内容": ""} 
                for f in TENDER_FIELDS.values()
            }
        }
        return json.dumps(template, ensure_ascii=False, indent=2)