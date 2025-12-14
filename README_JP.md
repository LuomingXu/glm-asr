[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">
<img src="resources/logo.svg" width="20%"/>

# GLM-ASR

[![Docker](https://img.shields.io/badge/Docker-neosun%2Fglm--asr-blue?logo=docker)](https://hub.docker.com/r/neosun/glm-asr)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)

**GLM-ASR-Nano ベースのオールインワン音声認識サービス**

Web UI • REST API • MCP サーバー • 長時間音声対応

</div>

---

## 🖥️ スクリーンショット

![Web UI](resources/ui-screenshot.png)

---

## ✨ 機能

- 🎯 **高精度認識** - GLM-ASR-Nano-2512 (1.5B) 搭載、Whisper V3 を上回る性能
- 🌍 **17言語対応** - 中国語、英語、広東語、日本語、韓国語など
- 🎤 **長時間音声** - チャンク処理で音声長制限なし
- 🖥️ **Web UI** - モダンなダークテーマ、4言語対応
- 🔌 **REST API** - 完全な API、Swagger ドキュメント
- 🤖 **MCP サーバー** - Claude Desktop 統合対応
- 💾 **GPU 管理** - モデルの手動ロード/アンロード
- 🐳 **Docker 対応** - ワンコマンドデプロイ

---

## 🚀 クイックスタート

### Docker（推奨）

```bash
docker run -d --gpus all -p 7860:7860 neosun/glm-asr:latest
```

アクセス：http://localhost:7860

### Docker Compose

```bash
git clone https://github.com/neosun100/glm-asr.git
cd glm-asr
docker compose up -d
```

---

## 📦 インストール

### 必要条件

- NVIDIA GPU（VRAM 6GB以上）
- Docker + NVIDIA Container Toolkit
- または：Python 3.10+、CUDA 12.x、FFmpeg

### 方法1：Docker

```bash
# イメージ取得
docker pull neosun/glm-asr:latest

# コンテナ起動
docker run -d \
  --name glm-asr \
  --gpus all \
  -p 7860:7860 \
  -v ./cache:/app/cache \
  neosun/glm-asr:latest

# ヘルスチェック
curl http://localhost:7860/health
```

### 方法2：ローカルインストール

```bash
# リポジトリクローン
git clone https://github.com/neosun100/glm-asr.git
cd glm-asr

# 依存関係インストール
pip install -r requirements.txt
sudo apt install ffmpeg

# サービス起動
python app.py
```

---

## ⚙️ 設定

### 環境変数

| 変数 | デフォルト | 説明 |
|------|------------|------|
| `MODEL_PATH` | `zai-org/GLM-ASR-Nano-2512` | HuggingFace モデルパス |
| `PORT` | `7860` | サービスポート |
| `HF_HOME` | `/app/cache` | モデルキャッシュディレクトリ |

### docker-compose.yml

```yaml
services:
  glm-asr:
    image: neosun/glm-asr:latest
    ports:
      - "7860:7860"
    volumes:
      - ./cache:/app/cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## 📖 使用方法

### Web UI

http://localhost:7860 を開く：
- 音声ファイルをアップロード（wav/mp3/flac/m4a/ogg）
- 「文字起こし」をクリック
- 結果をコピー

---

## 🔌 API リファレンス

### ベース URL
```
http://localhost:7860
```

### エンドポイント

#### ヘルスチェック
```http
GET /health
```
**レスポンス：**
```json
{"status": "ok", "model_loaded": true}
```

#### 音声文字起こし
```http
POST /api/transcribe
Content-Type: multipart/form-data
```
**パラメータ：**
| 名前 | 型 | 必須 | 説明 |
|------|------|------|------|
| file | File | はい | 音声ファイル（wav/mp3/flac/m4a/ogg） |
| max_new_tokens | int | いいえ | 最大出力トークン数（デフォルト：512） |

**例：**
```bash
curl -X POST http://localhost:7860/api/transcribe \
  -F "file=@audio.mp3"
```
**レスポンス：**
```json
{"status": "success", "text": "文字起こしされたテキスト..."}
```

#### GPU ステータス
```http
GET /gpu/status
```
**レスポンス：**
```json
{
  "model_loaded": true,
  "device": "cuda",
  "checkpoint": "zai-org/GLM-ASR-Nano-2512",
  "gpu_memory_used_mb": 4320.5,
  "gpu_memory_total_mb": 24576.0
}
```

#### モデルアンロード
```http
POST /gpu/unload
```
**レスポンス：**
```json
{"status": "unloaded"}
```

#### モデルロード
```http
POST /gpu/load
```
**レスポンス：**
```json
{"status": "loaded"}
```

### Swagger ドキュメント
インタラクティブ API ドキュメント：http://localhost:7860/docs

---

## 🤖 MCP サーバー（Claude Desktop）

`claude_desktop_config.json` に追加：

```json
{
  "mcpServers": {
    "glm-asr": {
      "command": "python",
      "args": ["/path/to/glm-asr/mcp_server.py"]
    }
  }
}
```

利用可能なツール：
- `transcribe` - 音声ファイルを文字起こし
- `gpu_status` - GPU/モデル状態を取得
- `gpu_load` - モデルを GPU にロード
- `gpu_unload` - GPU からモデルをアンロード

---

## 🏗️ 技術スタック

| コンポーネント | 技術 |
|----------------|------|
| モデル | GLM-ASR-Nano-2512 (1.5B) |
| バックエンド | Flask + Flask-SocketIO |
| フロントエンド | HTML5 + Vanilla JS |
| コンテナ | Docker + NVIDIA CUDA |
| API ドキュメント | Flasgger (Swagger) |
| MCP | FastMCP |

---

## 📊 ベンチマーク

GLM-ASR-Nano は同等モデル中最低のエラー率（4.10）を達成：

![Benchmark](resources/bench.png)

---

## 🤝 コントリビュート

1. リポジトリをフォーク
2. フィーチャーブランチ作成 (`git checkout -b feature/amazing`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing`)
5. Pull Request を作成

---

## 📝 変更履歴

### v1.1.0 (2024-12-15)
- ✅ VAD スマート分割（silero-vad）
- ✅ 自然な休止位置で分割、単語/文を切断しない
- ✅ 無制限の音声長をサポート（1.5時間テスト済み）
- ✅ 各セグメント ≤ 25秒、OOM 防止
- ✅ 短いセグメントを自動マージ（≥ 2秒）

### v1.0.2 (2024-12-14)
- ✅ 長時間音声保護（最大30分で切り捨て）
- ✅ エラー処理の改善

### v1.0.1 (2024-12-14)
- ✅ UI スクリーンショットを追加
- ✅ API ドキュメントを強化

### v1.0.0 (2024-12-14)
- ✅ 長時間音声チャンク文字起こし
- ✅ 4言語 Web UI
- ✅ REST API + Swagger ドキュメント
- ✅ MCP サーバー統合
- ✅ Docker オールインワンイメージ

---

## 📄 ライセンス

[Apache License 2.0](LICENSE)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/glm-asr&type=Date)](https://star-history.com/#neosun100/glm-asr)

## 📱 フォローする

<img src="https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png" width="300"/>
