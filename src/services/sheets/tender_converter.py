"""Converter for tender information to spreadsheet format"""
import logging
from typing import Dict, Any, Optional, List, Union
from src.models.tender_response import TenderResponse

logger = logging.getLogger(__name__)

class TenderConverter:
    def get_project_name(self, tender_info: Union[Dict[str, Any], TenderResponse]) -> str:
        """Get project name from tender information"""
        try:
            project_name = None
            
            if isinstance(tender_info, TenderResponse):
                project_field = tender_info.項目.get("案件名")
                if project_field and project_field.内容:
                    project_name = project_field.内容
            elif isinstance(tender_info, dict) and "項目" in tender_info:
                project_info = tender_info["項目"].get("案件名", {})
                if isinstance(project_info, dict):
                    project_name = project_info.get("内容", "")
            
            # Ensure we return a valid string
            if not project_name or not str(project_name).strip():
                logger.warning("No project name found, using default")
                return "未名案件"
                
            return str(project_name).strip()
            
        except Exception as e:
            logger.error(f"Error getting project name: {str(e)}")
            return "未名案件"

    def convert_to_values(self, tender_info: Union[Dict[str, Any], TenderResponse]) -> List[List[str]]:
        """Convert tender info to spreadsheet values"""
        try:
            values = []
            
            if isinstance(tender_info, TenderResponse):
                # Handle TenderResponse object
                for field_name, field_content in tender_info.項目.items():
                    values.append([
                        str(field_content.見出し).strip(),
                        str(field_content.内容).strip()
                    ])
            elif isinstance(tender_info, dict) and "項目" in tender_info:
                # Handle dictionary format
                items = tender_info["項目"]
                for field_name, field_content in items.items():
                    if isinstance(field_content, dict):
                        heading = str(field_content.get("見出し", field_name)).strip()
                        content = str(field_content.get("内容", "")).strip()
                        values.append([heading, content])
            
            if not values:
                logger.warning("No valid data found in tender info")
                return [["見出し", "内容"]]  # Return at least headers
                
            return values
            
        except Exception as e:
            logger.error(f"Error converting tender data: {str(e)}")
            logger.error(f"Tender info: {tender_info}")
            return [["見出し", "内容"]]  # Return headers on error