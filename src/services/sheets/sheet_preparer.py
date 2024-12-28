"""Sheet preparation service for Google Sheets"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SheetPreparer:
    def __init__(self, service):
        self.service = service

    def prepare_sheet(self, spreadsheet_id: str, sheet_name: str) -> Optional[int]:
        """Prepare sheet for data update"""
        try:
            sheet_id = self._get_or_create_sheet(spreadsheet_id, sheet_name)
            if sheet_id:
                self._clear_existing_content(spreadsheet_id, sheet_id)
                self._setup_headers(spreadsheet_id, sheet_name)
            return sheet_id
        except Exception as e:
            logger.error(f"Error preparing sheet: {str(e)}")
            return None

    def _get_or_create_sheet(self, spreadsheet_id: str, sheet_name: str) -> Optional[int]:
        """Get existing sheet or create new one"""
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id).execute()
            
            existing_sheet = next(
                (sheet for sheet in sheet_metadata['sheets'] 
                 if sheet['properties']['title'] == sheet_name),
                None
            )
            
            if existing_sheet:
                return existing_sheet['properties']['sheetId']
            
            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_name,
                                'gridProperties': {
                                    'frozenRowCount': 1
                                }
                            }
                        }
                    }]
                }
            ).execute()
            
            return result['replies'][0]['addSheet']['properties']['sheetId']
            
        except Exception as e:
            logger.error(f"Error getting/creating sheet: {str(e)}")
            return None

    def _clear_existing_content(self, spreadsheet_id: str, sheet_id: int) -> None:
        """Clear existing content from sheet"""
        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [{
                        'updateCells': {
                            'range': {
                                'sheetId': sheet_id,
                                'startRowIndex': 1
                            },
                            'fields': 'userEnteredValue'
                        }
                    }]
                }
            ).execute()
        except Exception as e:
            logger.error(f"Error clearing sheet content: {str(e)}")

    def _setup_headers(self, spreadsheet_id: str, sheet_name: str) -> None:
        """Set up header row"""
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f'{sheet_name}!A1:B1',
                valueInputOption='RAW',
                body={'values': [['見出し', '内容']]}
            ).execute()
        except Exception as e:
            logger.error(f"Error setting up headers: {str(e)}")