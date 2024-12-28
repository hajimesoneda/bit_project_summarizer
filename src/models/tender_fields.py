"""Tender analysis field definitions and extraction rules"""
from typing import Dict, Any

class TenderField:
    def __init__(self, name: str, keywords: list[str], extraction_rules: str):
        self.name = name
        self.keywords = keywords
        self.extraction_rules = extraction_rules

TENDER_FIELDS: Dict[str, TenderField] = {
    "案件名": TenderField(
        "案件名",
        ["案件名", "件名", "調達案件名", "業務名", "事業名"],
        "プロジェクト名や業務内容を端的に表現している部分を抽出してください"
    ),
    "発注機関": TenderField(
        "発注機関",
        ["発注機関", "契約担当官", "支出負担行為担当官", "調達機関"],
        "省庁名、部署名、組織名などを含む正式名称を抽出してください"
    ),
    "入札の種類": TenderField(
        "入札の種類",
        ["入札方式", "入札区分", "調達方式", "契約方式"],
        "一般競争入札、指名競争入札、総合評価落札方式などの入札方式を特定してください"
    ),
    "CMSの有無": TenderField(
        "CMSの有無",
        ["CMS", "コンテンツ管理システム", "WordPress", "コンテンツマネジメントシステム"],
        "システム要件からCMSの必要性を判断し、「有」「無」で回答してください"
    ),
    "要件概要": TenderField(
        "要件概要",
        ["業務概要", "案件概要", "調達概要", "業務内容", "仕様概要"],
        """以下の点を必ず含めて要約してください：
        1. プロジェクトの目的
        2. 主要な開発・導入項目
        3. 特記すべき技術要件
        4. 保守・運用に関する要件"""
    )
}