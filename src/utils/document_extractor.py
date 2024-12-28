"""Document text extraction utility"""
import logging
import docx
import pandas as pd

logger = logging.getLogger(__name__)

class DocumentExtractor:
    def extract_text(self, file_handle, mime_type: str) -> str:
        """
        各種ドキュメントからテキストを抽出
        
        Args:
            file_handle: ファイルオブジェクト
            mime_type: MIMEタイプ
            
        Returns:
            str: 抽出されたテキスト
        """
        try:
            if mime_type == 'application/vnd.google-apps.document':
                return self._extract_google_doc(file_handle)
            elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return self._extract_docx(file_handle)
            elif mime_type in ['application/vnd.google-apps.spreadsheet', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                return self._extract_spreadsheet(file_handle)
            else:
                logger.warning(f"未対応のMIMEタイプ: {mime_type}")
                return ""
        except Exception as e:
            logger.error(f"ドキュメント処理中にエラー: {str(e)}")
            return ""

    def _extract_google_doc(self, content: str) -> str:
        """Google Documentのテキストを抽出"""
        try:
            if isinstance(content, bytes):
                return content.decode('utf-8')
            return content
        except Exception as e:
            logger.error(f"Google Document処理中にエラー: {str(e)}")
            return ""

    def _extract_docx(self, file_handle) -> str:
        """Word文書からテキストを抽出"""
        try:
            doc = docx.Document(file_handle)
            text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text)
            return "\n".join(text)
        except Exception as e:
            logger.error(f"Word文書処理中にエラー: {str(e)}")
            return ""

    def _extract_spreadsheet(self, file_handle) -> str:
        """スプレッドシートからテキストを抽出"""
        try:
            df = pd.read_excel(file_handle)
            return df.to_string(index=False)
        except Exception as e:
            logger.error(f"スプレッドシート処理中にエラー: {str(e)}")
            return ""