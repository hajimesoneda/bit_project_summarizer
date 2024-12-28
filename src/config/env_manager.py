"""Environment configuration manager"""
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class EnvManager:
    _instance = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._is_initialized:
            self._is_initialized = True
            self.reload_env()
    
    def reload_env(self):
        """環境変数を再読み込み"""
        try:
            # 既存の環境変数をクリア
            self._clear_existing_vars()
            
            # .envファイルを再読み込み
            load_dotenv(override=True)
            
            # 必須の環境変数をチェック
            self._validate_required_vars()
            
            logger.info("環境変数を再読み込みしました")
        except Exception as e:
            logger.error(f"環境変数の読み込み中にエラー: {str(e)}")
            raise
    
    def _clear_existing_vars(self):
        """既存の環境変数をクリア"""
        vars_to_clear = [
            'DRIVE_FOLDER_ID',
            'FOLDER_NAME',
            'SPREADSHEET_ID',
            'OPENAI_API_KEY',
            'GPT_MODEL'
        ]
        for var in vars_to_clear:
            if var in os.environ:
                del os.environ[var]
    
    def _validate_required_vars(self):
        """必須の環境変数をチェック"""
        required_vars = {
            'DRIVE_FOLDER_ID': '対象のGoogle DriveフォルダID',
            'SPREADSHEET_ID': '出力先のスプレッドシートID',
            'OPENAI_API_KEY': 'OpenAI APIキー'
        }
        
        missing_vars = []
        for var, description in required_vars.items():
            if not os.getenv(var):
                missing_vars.append(f"{var} ({description})")
        
        if missing_vars:
            raise ValueError(f"必須の環境変数が設定されていません: {', '.join(missing_vars)}")
    
    def get_env(self, key: str, default: str = None) -> str:
        """
        環境変数を取得
        
        Args:
            key: 環境変数名
            default: デフォルト値
        
        Returns:
            str: 環境変数の値
        """
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"環境変数 {key} が設定されていません")
        return value