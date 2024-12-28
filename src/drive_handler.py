from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import logging
from src.utils.pdf_extractor import PDFExtractor
from src.utils.document_extractor import DocumentExtractor

logger = logging.getLogger(__name__)

class DriveHandler:
    def __init__(self, credentials):
        self.service = build('drive', 'v3', credentials=credentials)
        self.pdf_extractor = PDFExtractor()
        self.document_extractor = DocumentExtractor()
    
    def get_folder_contents(self, folder_id):
        try:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name, mimeType)"
            ).execute()
            return results.get('files', [])
        except Exception as e:
            logger.error(f"フォルダ内容の取得中にエラー: {str(e)}")
            return []
    
    def extract_text(self, file_id, mime_type):
        """ファイルからテキストを抽出"""
        try:
            if mime_type.startswith('application/vnd.google-apps.'):
                return self._extract_google_workspace_file(file_id, mime_type)
            else:
                return self._extract_binary_file(file_id, mime_type)
        except Exception as e:
            logger.error(f"テキスト抽出中にエラー: {str(e)}")
            return ""

    def _extract_google_workspace_file(self, file_id, mime_type):
        """Google Workspaceファイルを処理"""
        try:
            export_mime_type = self._get_export_mime_type(mime_type)
            if not export_mime_type:
                logger.warning(f"未対応のGoogle Workspaceファイル: {mime_type}")
                return ""

            content = self.service.files().export(
                fileId=file_id,
                mimeType=export_mime_type
            ).execute()
            
            return self.document_extractor.extract_text(content, mime_type)
        except Exception as e:
            logger.error(f"Google Workspaceファイルの処理中にエラー: {str(e)}")
            return ""

    def _extract_binary_file(self, file_id, mime_type):
        """バイナリファイルを処理"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                _, done = downloader.next_chunk()
            
            fh.seek(0)
            
            if mime_type == 'application/pdf':
                return self.pdf_extractor.extract_text(fh)
            else:
                return self.document_extractor.extract_text(fh, mime_type)
                
        except Exception as e:
            logger.error(f"バイナリファイルの処理中にエラー: {str(e)}")
            return ""

    def _get_export_mime_type(self, mime_type):
        """エクスポート用のMIMEタイプを取得"""
        mime_type_map = {
            'application/vnd.google-apps.document': 'text/plain',
            'application/vnd.google-apps.spreadsheet': 'text/csv',
            'application/vnd.google-apps.presentation': 'text/plain'
        }
        return mime_type_map.get(mime_type)