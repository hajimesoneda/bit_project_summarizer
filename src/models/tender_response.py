"""Data models for tender analysis responses"""
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class TenderFieldContent:
    見出し: str
    内容: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

@dataclass
class TenderResponse:
    項目: Dict[str, TenderFieldContent]

    @classmethod
    def create_empty(cls, field_names: list[str]) -> 'TenderResponse':
        """Create an empty response with all fields"""
        return cls(項目={
            name: TenderFieldContent(見出し=name, 内容="")
            for name in field_names
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "項目": {
                name: field.to_dict()
                for name, field in self.項目.items()
            }
        }