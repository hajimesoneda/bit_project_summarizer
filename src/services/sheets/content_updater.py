"""Content update service for Google Sheets"""
import logging
from typing import List

logger = logging.getLogger(__name__)

class ContentUpdater:
    def __init__(self, service):
        self.service = service

    def update_content(self, spreadsheet_id: str, sheet_name: str, values: List[List[str]]) -> None:
        """Update sheet content with new values"""
        try:
            if not values:
                logger.warning("No values to update")
                return

            # Ensure all values are strings
            sanitized_values = [
                [str(cell).strip() for cell in row]
                for row in values
            ]

            # Update the sheet
            range_name = f'{sheet_name}!A2:B{len(sanitized_values) + 1}'
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': sanitized_values}
            ).execute()
            
            logger.info(f"Successfully updated {len(sanitized_values)} rows in sheet {sheet_name}")
            
        except Exception as e:
            logger.error(f"Error updating sheet content: {str(e)}")
            logger.error(f"Sheet: {sheet_name}, Values: {values}")
            raise