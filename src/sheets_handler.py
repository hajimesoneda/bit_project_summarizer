"""Google Sheets handler for tender analysis results"""
from googleapiclient.discovery import build
import logging
from typing import Dict, Any, Optional, List, Union
from src.models.tender_response import TenderResponse
from src.services.sheets.sheet_preparer import SheetPreparer
from src.services.sheets.content_updater import ContentUpdater
from src.services.sheets.format_adjuster import FormatAdjuster
from src.services.sheets.tender_converter import TenderConverter

logger = logging.getLogger(__name__)

class SheetsHandler:
    def __init__(self, credentials):
        """Initialize the sheets handler with Google credentials"""
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet_preparer = SheetPreparer(self.service)
        self.content_updater = ContentUpdater(self.service)
        self.format_adjuster = FormatAdjuster(self.service)
        self.tender_converter = TenderConverter()
    
    def create_or_append_sheet(self, spreadsheet_id: str, tender_info: Union[Dict[str, Any], TenderResponse], default_sheet_name: str) -> None:
        """Create or update a sheet with tender information"""
        try:
            # Get project name for sheet title
            sheet_name = self.tender_converter.get_project_name(tender_info)
            if not sheet_name:
                logger.warning(f"Using default sheet name: {default_sheet_name}")
                sheet_name = default_sheet_name
            
            logger.info(f"Using sheet name: {sheet_name}")
            
            # Convert tender info to spreadsheet values
            values = self.tender_converter.convert_to_values(tender_info)
            if not values:
                logger.warning("No data to update in spreadsheet")
                return
            
            # Prepare sheet
            sheet_id = self.sheet_preparer.prepare_sheet(spreadsheet_id, sheet_name)
            if sheet_id is None:
                logger.error("Failed to prepare sheet")
                return
            
            # Update sheet content
            self.content_updater.update_content(spreadsheet_id, sheet_name, values)
            
            # Adjust column widths
            self.format_adjuster.adjust_column_widths(spreadsheet_id, sheet_id)
            
        except Exception as e:
            logger.error(f"Error updating spreadsheet: {str(e)}")
            raise