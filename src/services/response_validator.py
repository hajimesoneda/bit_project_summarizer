"""Validator for OpenAI API responses"""
import logging
from typing import Dict, Any, Optional
from src.models.tender_fields import TENDER_FIELDS
from src.models.tender_response import TenderResponse, TenderFieldContent

logger = logging.getLogger(__name__)

class ResponseValidator:
    @staticmethod
    def validate_and_clean(response: Any) -> Optional[TenderResponse]:
        """Validate and clean the OpenAI response"""
        try:
            # Handle None response
            if response is None:
                logger.error("Received None response")
                return TenderResponse.create_empty(TENDER_FIELDS.keys())

            # Basic structure validation
            if not isinstance(response, dict):
                logger.error(f"Response is not a dictionary: {type(response)}")
                return TenderResponse.create_empty(TENDER_FIELDS.keys())

            items = response.get("項目")
            if not isinstance(items, dict):
                logger.error(f"Invalid or missing '項目' in response: {response}")
                return TenderResponse.create_empty(TENDER_FIELDS.keys())

            # Process each field
            cleaned_items = {}
            for field_name in TENDER_FIELDS.keys():
                field_data = items.get(field_name, {})
                
                # Handle various field data formats
                if isinstance(field_data, str):
                    content = field_data
                elif isinstance(field_data, dict):
                    content = field_data.get("内容", field_data.get("content", ""))
                else:
                    content = str(field_data) if field_data is not None else ""

                # Ensure content is a string and clean it
                content = str(content).strip()
                
                cleaned_items[field_name] = TenderFieldContent(
                    見出し=field_name,
                    内容=content
                )

            return TenderResponse(項目=cleaned_items)

        except Exception as e:
            logger.error(f"Error validating response: {str(e)}")
            logger.error(f"Original response: {response}")
            return TenderResponse.create_empty(TENDER_FIELDS.keys())