"""PDF text extraction utility"""
from PyPDF2 import PdfReader
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self):
        self.supported_versions = range(1, 3)  # PDF version 1.x ~ 2.x をサポート
    
    def extract_text(self, file_handle) -> str:
        """
        PDFからテキストを抽出する
        
        Args:
            file_handle: PDF file object (BytesIO)
            
        Returns:
            str: 抽出されたテキスト
        """
        if not self._is_valid_pdf(file_handle):
            return ""
            
        text = []
        try:
            file_handle.seek(0)
            pdf = PdfReader(file_handle)
            
            for page_num, page in enumerate(pdf.pages):
                page_text = self._extract_page_text(page, page_num)
                if page_text:
                    text.append(page_text)
            
            return "\n\n".join(text)
            
        except Exception as e:
            logger.error(f"PDF処理中にエラーが発生: {str(e)}")
            return ""
    
    def _is_valid_pdf(self, file_handle) -> bool:
        """PDFファイルが有効かチェック"""
        try:
            file_handle.seek(0)
            header = file_handle.read(1024).decode('utf-8', errors='ignore')
            file_handle.seek(0)
            
            if not header.startswith('%PDF-'):
                logger.error("無効なPDFファイル: PDFヘッダーが見つかりません")
                return False
                
            version = self._get_pdf_version(header)
            if version and version not in self.supported_versions:
                logger.warning(f"サポート外のPDFバージョン: {version}")
                
            return True
            
        except Exception as e:
            logger.error(f"PDFファイルの検証中にエラー: {str(e)}")
            return False
    
    def _get_pdf_version(self, header: str) -> Optional[int]:
        """PDFバージョンを取得"""
        try:
            if '%PDF-' in header:
                version_str = header[header.find('%PDF-')+5:header.find('%PDF-')+7]
                return int(float(version_str))
        except:
            pass
        return None
    
    def _extract_page_text(self, page, page_num: int) -> str:
        """ページからテキストを抽出"""
        try:
            page_text = page.extract_text()
            if not page_text:
                logger.warning(f"ページ {page_num + 1} からテキストを抽出できませんでした")
                return ""
            return page_text.strip()
        except Exception as e:
            logger.error(f"ページ {page_num + 1} の処理中にエラー: {str(e)}")
            return ""