# 財政ナビ-AIひろこ先生　デプロイ手順

## Vercelへのデプロイ（5分で完了）

### 1. GitHubにアップロード
- GitHubで新しいリポジトリを作成（例：`ai-hiroko`）
- このフォルダの中身をすべてアップロード

### 2. Vercelと連携
- https://vercel.com にログイン
- 「Add New Project」→GitHubのリポジトリを選択
- 「Import」をクリック

### 3. 環境変数を設定（重要）
- Vercelの設定画面で「Environment Variables」を開く
- 以下を追加：
  - Name: `ANTHROPIC_API_KEY`
  - Value: `sk-ant-...`（あなたのAPIキー）

### 4. デプロイ
- 「Deploy」をクリック
- 1〜2分でURLが発行される

### 完成
`https://ai-hiroko-xxxx.vercel.app` のようなURLが発行され、
誰でもアクセスできるようになります。
