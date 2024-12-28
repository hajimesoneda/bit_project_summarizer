"""Format adjustment service for Google Sheets"""
import logging

logger = logging.getLogger(__name__)

class FormatAdjuster:
    def __init__(self, service):
        self.service = service

    def adjust_column_widths(self, spreadsheet_id: str, sheet_id: int) -> None:
        """Adjust column widths to fit content"""
        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [{
                        'autoResizeDimensions': {
                            'dimensions': {
                                'sheetId': sheet_id,
                                'dimension': 'COLUMNS',
                                'startIndex': 0,
                                'endIndex': 2
                            }
                        }
                    }]
                }
            ).execute()
        except Exception as e:
            logger.error(f"Error adjusting column widths: {str(e)}")
            raise