"""Main entry point for tender analysis system"""
from src.config.env_manager import EnvManager
from src.config.google_auth import get_google_auth
from src.drive_handler import DriveHandler
from src.sheets_handler import SheetsHandler
from src.openai_analyzer import TenderAnalyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_files(drive_handler, folder_id):
    """Process files from Google Drive and extract text"""
    files = drive_handler.get_folder_contents(folder_id)
    all_text = ""
    for file in files:
        text = drive_handler.extract_text(file['id'], file['mimeType'])
        all_text += text + "\n\n"
    return all_text

def update_spreadsheet(sheets_handler, spreadsheet_id, tender_info, folder_name):
    """Update spreadsheet with tender information"""
    try:
        sheets_handler.create_or_append_sheet(
            spreadsheet_id, 
            tender_info,
            folder_name
        )
        
        # Get project name from tender info
        project_name = ""
        if hasattr(tender_info, '項目'):
            project_field = tender_info.項目.get("案件名")
            if project_field and project_field.内容:
                project_name = project_field.内容
        
        if project_name:
            logger.info(f"案件「{project_name}」の分析が完了しました")
        else:
            logger.info("案件の分析が完了しました")
            
    except Exception as e:
        logger.error(f"スプレッドシートの更新中にエラー: {str(e)}")

def main():
    try:
        # 環境変数マネージャーの初期化と読み込み
        env_manager = EnvManager()
        env_manager.reload_env()
        
        # 設定値の取得
        target_folder_id = env_manager.get_env('DRIVE_FOLDER_ID')
        output_spreadsheet_id = env_manager.get_env('SPREADSHEET_ID')
        folder_name = env_manager.get_env('FOLDER_NAME', 'デフォルト案件名')
        openai_api_key = env_manager.get_env('OPENAI_API_KEY')
        
        # 認証情報の取得
        credentials = get_google_auth()
        
        # 各ハンドラーの初期化
        drive_handler = DriveHandler(credentials)
        sheets_handler = SheetsHandler(credentials)
        tender_analyzer = TenderAnalyzer(openai_api_key)
        
        # ファイル処理
        all_text = process_files(drive_handler, target_folder_id)
        if not all_text.strip():
            logger.error("処理対象のテキストが見つかりませんでした")
            return
        
        # OpenAIによる分析
        tender_info = tender_analyzer.analyze_tender(all_text)
        
        if tender_info:
            update_spreadsheet(sheets_handler, output_spreadsheet_id, tender_info, folder_name)
        else:
            logger.error("案件の分析に失敗しました")
            
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()