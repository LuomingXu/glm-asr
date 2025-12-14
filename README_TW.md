[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">
<img src="resources/logo.svg" width="20%"/>

# GLM-ASR

[![Docker](https://img.shields.io/badge/Docker-neosun%2Fglm--asr-blue?logo=docker)](https://hub.docker.com/r/neosun/glm-asr)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)

**基於 GLM-ASR-Nano 的一站式語音識別服務**

Web 介面 • REST API • MCP 服務 • 長音訊支援

</div>

---

## 🖥️ 介面截圖

![Web UI](resources/ui-screenshot.png)

---

## ✨ 功能特性

- 🎯 **高精度識別** - 基於 GLM-ASR-Nano-2512 (1.5B)，效能超越 Whisper V3
- 🌍 **17 種語言** - 支援中文、英語、粵語、日語、韓語等
- 🎤 **長音訊支援** - 分段處理，無音訊長度限制
- 🖥️ **Web 介面** - 現代暗色主題，支援 4 種語言切換
- 🔌 **REST API** - 完整 API 介面，Swagger 文件
- 🤖 **MCP 服務** - 支援 Claude Desktop 整合
- 💾 **顯存管理** - 手動載入/卸載模型，靈活控制顯存
- 🐳 **Docker 部署** - 一鍵啟動

---

## 🚀 快速開始

### Docker 方式（推薦）

```bash
docker run -d --gpus all -p 7860:7860 neosun/glm-asr:latest
```

存取：http://localhost:7860

### Docker Compose

```bash
git clone https://github.com/neosun100/glm-asr.git
cd glm-asr
docker compose up -d
```

---

## 📦 安裝部署

### 環境要求

- NVIDIA GPU（顯存 6GB+）
- Docker + NVIDIA Container Toolkit
- 或：Python 3.10+、CUDA 12.x、FFmpeg

### 方式一：Docker 部署

```bash
# 拉取映像
docker pull neosun/glm-asr:latest

# 啟動容器
docker run -d \
  --name glm-asr \
  --gpus all \
  -p 7860:7860 \
  -v ./cache:/app/cache \
  neosun/glm-asr:latest

# 健康檢查
curl http://localhost:7860/health
```

### 方式二：本地安裝

```bash
# 複製儲存庫
git clone https://github.com/neosun100/glm-asr.git
cd glm-asr

# 安裝依賴
pip install -r requirements.txt
sudo apt install ffmpeg

# 啟動服務
python app.py
```

---

## ⚙️ 配置說明

### 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `MODEL_PATH` | `zai-org/GLM-ASR-Nano-2512` | HuggingFace 模型路徑 |
| `PORT` | `7860` | 服務埠號 |
| `HF_HOME` | `/app/cache` | 模型快取目錄 |

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

## 📖 使用說明

### Web 介面

開啟 http://localhost:7860：
- 上傳音訊檔案（wav/mp3/flac/m4a/ogg）
- 點擊「轉錄」
- 複製結果

---

## 🔌 API 文件

### 基礎位址
```
http://localhost:7860
```

### 介面列表

#### 健康檢查
```http
GET /health
```
**回應：**
```json
{"status": "ok", "model_loaded": true}
```

#### 音訊轉錄
```http
POST /api/transcribe
Content-Type: multipart/form-data
```
**參數：**
| 名稱 | 類型 | 必填 | 說明 |
|------|------|------|------|
| file | File | 是 | 音訊檔案（wav/mp3/flac/m4a/ogg） |
| max_new_tokens | int | 否 | 最大輸出 token 數（預設：512） |

**範例：**
```bash
curl -X POST http://localhost:7860/api/transcribe \
  -F "file=@audio.mp3"
```
**回應：**
```json
{"status": "success", "text": "轉錄的文字內容..."}
```

#### GPU 狀態
```http
GET /gpu/status
```
**回應：**
```json
{
  "model_loaded": true,
  "device": "cuda",
  "checkpoint": "zai-org/GLM-ASR-Nano-2512",
  "gpu_memory_used_mb": 4320.5,
  "gpu_memory_total_mb": 24576.0
}
```

#### 卸載模型
```http
POST /gpu/unload
```
**回應：**
```json
{"status": "unloaded"}
```

#### 載入模型
```http
POST /gpu/load
```
**回應：**
```json
{"status": "loaded"}
```

### Swagger 文件
互動式 API 文件：http://localhost:7860/docs

---

## 🤖 MCP 服務（Claude Desktop）

在 `claude_desktop_config.json` 中新增：

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

可用工具：
- `transcribe` - 轉錄音訊檔案
- `gpu_status` - 取得 GPU/模型狀態
- `gpu_load` - 載入模型到 GPU
- `gpu_unload` - 從 GPU 卸載模型

---

## 🏗️ 技術棧

| 元件 | 技術 |
|------|------|
| 模型 | GLM-ASR-Nano-2512 (1.5B) |
| 後端 | Flask + Flask-SocketIO |
| 前端 | HTML5 + Vanilla JS |
| 容器 | Docker + NVIDIA CUDA |
| API 文件 | Flasgger (Swagger) |
| MCP | FastMCP |

---

## 📊 效能對比

GLM-ASR-Nano 在同類模型中錯誤率最低（4.10）：

![Benchmark](resources/bench.png)

---

## 🤝 參與貢獻

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/amazing`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing`)
5. 提交 Pull Request

---

## 📝 更新日誌

### v1.1.0 (2024-12-15)
- ✅ VAD 智慧分段（silero-vad）
- ✅ 在自然停頓處切分，不切斷詞句
- ✅ 支援任意長度音訊（已測試 1.5 小時）
- ✅ 每段 ≤ 25秒，防止 OOM
- ✅ 自動合併過短片段（≥ 2秒）

### v1.0.2 (2024-12-14)
- ✅ 長音訊保護（最大 30 分鐘截斷）
- ✅ 改進錯誤處理

### v1.0.1 (2024-12-14)
- ✅ 新增 UI 介面截圖
- ✅ 完善 API 文件

### v1.0.0 (2024-12-14)
- ✅ 長音訊分段轉錄
- ✅ 4 語言 Web 介面
- ✅ REST API + Swagger 文件
- ✅ MCP 服務整合
- ✅ Docker 一體化映像

---

## 📄 開源協議

[Apache License 2.0](LICENSE)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/glm-asr&type=Date)](https://star-history.com/#neosun100/glm-asr)

## 📱 關注公眾號

<img src="https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png" width="300"/>
