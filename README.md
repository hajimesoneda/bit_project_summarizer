# 入札案件分析システム

入札案件の文書を自動で分析し、重要な情報を抽出してスプレッドシートに整理するシステムです。
（pythonとOpenAI APIの勉強用）

## セキュリティ上の重要な注意

以下のファイルは機密情報を含むため、**絶対にGitリポジトリにコミットしないでください**：

1. `.env`
   - OpenAI APIキー
   - Google Drive フォルダID
   - スプレッドシートID
   - その他の環境設定

2. `credentials/credentials.json`
   - Google Cloud Platformの認証情報
   - サービスアカウントの秘密鍵

3. `token.pickle`
   - Google APIのアクセストークン
   - 認証セッション情報

## 対応ファイル形式

システムは以下のファイル形式に対応しています：

1. PDF文書 (`.pdf`)
2. Microsoft Word文書 (`.docx`)
3. Microsoft Excel (`.xlsx`)
4. Google Documents
5. Google Spreadsheets
6. プレーンテキスト (`.txt`)

## セットアップ手順

1. リポジトリのクローン
```bash
git clone https://github.com/hajimesoneda/bit_project_summarizer.git
cd bit_project_summarizer
```

2. 必要なPythonパッケージをインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
   - `.env.example`を`.env`にコピー
   - 各項目に適切な値を設定
```bash
cp .env.example .env
```

4. Google Cloud Platformの設定
   - [Google Cloud Console](https://console.cloud.google.com/)で新しいプロジェクトを作成
   - Google Drive APIとGoogle Sheets APIを有効化
   - サービスアカウントを作成し、認証情報をダウンロード
   - ダウンロードした認証情報を`credentials/credentials.json`として保存

5. 実行
```bash
python main.py
```

## トラブルシューティング

### キャッシュのクリア
問題が発生した場合、以下のコマンドでPythonのキャッシュをクリアできます：
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete
```

### PDF解析の問題
PDFの解析に問題がある場合：
1. PyPDF2が正しくインストールされているか確認
2. PDFファイルが破損していないか確認
3. ログを確認して具体的なエラーを特定
