[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

<div align="center">
<img src="resources/logo.svg" width="20%"/>

# GLM-ASR

[![Docker](https://img.shields.io/badge/Docker-neosun%2Fglm--asr-blue?logo=docker)](https://hub.docker.com/r/neosun/glm-asr)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)](https://fastapi.tiangolo.com)

**All-in-One Speech Recognition Service based on GLM-ASR-Nano**

Web UI • REST API • SSE Streaming • Swagger Docs

</div>

---

## 🖥️ Screenshot

![Web UI](resources/ui-screenshot.png)

---

## ✨ Features

- 🎯 **High Accuracy** - Based on GLM-ASR-Nano-2512 (1.5B), outperforms Whisper V3
- 🌍 **17 Languages** - Chinese, English, Cantonese, Japanese, Korean, and more
- 🎤 **Long Audio** - VAD smart segmentation for unlimited audio length
- 🚀 **SSE Streaming** - Real-time progress and results for long audio
- 🖥️ **Web UI** - Modern dark-mode interface with 4 language support
- 🔌 **REST API** - Full API with Swagger documentation
- 💾 **GPU Management** - Manual load/unload for memory control
- 🐳 **Docker Ready** - One-command deployment with pre-loaded model

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
docker run -d --gpus all -p 7860:7860 neosun/glm-asr:v2.0.1
```

Access:
- Web UI: http://localhost:7860
- Swagger Docs: http://localhost:7860/docs
- ReDoc: http://localhost:7860/redoc

### Docker Compose

```bash
git clone https://github.com/neosun100/glm-asr.git
cd glm-asr
docker compose up -d
```

---

## 📖 API Reference

### Base URL
```
http://localhost:7860
```

### Endpoints

#### Health Check
```http
GET /health
```
```json
{"status": "ok", "model_loaded": true}
```

#### Transcribe (Sync) - For short audio
```http
POST /api/transcribe
Content-Type: multipart/form-data
```
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file | File | required | Audio file (wav/mp3/flac/m4a/ogg/webm) |
| max_new_tokens | int | 512 | Max output tokens (1-2048) |

```bash
curl -X POST http://localhost:7860/api/transcribe \
  -F "file=@audio.mp3" \
  -F "max_new_tokens=512"
```
```json
{"status": "success", "text": "Transcribed text here..."}
```

#### Transcribe (SSE Stream) - For long audio
```http
POST /api/transcribe/stream
Content-Type: multipart/form-data
```

Returns Server-Sent Events with real-time progress:

| Event Type | Description | Example |
|------------|-------------|---------|
| `start` | Processing started | `{"type": "start"}` |
| `progress` | Segment progress | `{"type": "progress", "current": 3, "total": 10, "duration": 22.5}` |
| `partial` | Segment result | `{"type": "partial", "text": "Segment text..."}` |
| `done` | Complete | `{"type": "done", "text": "Full transcription..."}` |
| `error` | Error occurred | `{"type": "error", "message": "Error details"}` |

```bash
curl -X POST http://localhost:7860/api/transcribe/stream \
  -F "file=@long_audio.mp3"
```

#### GPU Status
```http
GET /gpu/status
```
```json
{
  "model_loaded": true,
  "device": "cuda",
  "gpu_memory_used_mb": 4320.5,
  "gpu_memory_total_mb": 24576.0
}
```

#### Load/Unload Model
```http
POST /gpu/load
POST /gpu/unload
```

### Interactive Documentation

- **Swagger UI**: http://localhost:7860/docs
- **ReDoc**: http://localhost:7860/redoc

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_CHECKPOINT` | `zai-org/GLM-ASR-Nano-2512` | HuggingFace model path |
| `PORT` | `7860` | Service port |
| `HF_HOME` | `/app/cache` | Model cache directory |

### docker-compose.yml

```yaml
services:
  glm-asr:
    image: neosun/glm-asr:v2.0.1
    container_name: glm-asr
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

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| Model | GLM-ASR-Nano-2512 (1.5B) |
| Backend | FastAPI + Uvicorn |
| Streaming | Server-Sent Events (SSE) |
| Frontend | HTML5 + Vanilla JS |
| Container | Docker + NVIDIA CUDA |
| API Docs | Swagger / ReDoc |

---

## 📊 Benchmark

GLM-ASR-Nano achieves the lowest average error rate (4.10) among comparable models:

![Benchmark](resources/bench.png)

---

## 📝 Changelog

### v2.0.1 (2024-12-28)
- ✅ Migrated to FastAPI async framework
- ✅ SSE streaming for real-time progress
- ✅ Complete Swagger API documentation
- ✅ Dual API mode: sync + streaming
- ✅ Fixed browser timeout for long audio
- ✅ Modern dark UI with progress display

### v1.1.0 (2024-12-15)
- ✅ VAD smart segmentation (silero-vad)
- ✅ Support unlimited audio length

### v1.0.0 (2024-12-14)
- ✅ Initial release
- ✅ Web UI with 4 language support
- ✅ REST API with Swagger docs
- ✅ Docker all-in-one image

---

## 📄 License

[Apache License 2.0](LICENSE)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/glm-asr&type=Date)](https://star-history.com/#neosun100/glm-asr)
