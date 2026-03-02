# 🚀 Real-Time Vision Platform

A production-oriented real-time computer vision platform for processing video streams and performing object detection using YOLO with optimized inference backends.

This project is designed as a **reference implementation** of how real-world camera AI systems are architected, focusing on performance, modularity, and deployability rather than business-specific logic.


## 📌 Overview

The Real-Time Vision Platform ingests live video streams (webcam, video file, or RTSP), performs real-time object detection, and exposes detection results through REST and WebSocket APIs.

Key goals of this project:
- Demonstrate end-to-end real-time CV system design
- Compare inference backends (PyTorch vs ONNX Runtime)
- Showcase performance-aware engineering decisions
- Provide a clean, extensible architecture suitable for production systems


## 🧠 System Architecture
```mermaid
flowchart TD
    A["Video Source 
    (Webcam - RTSP)"]
    B["Frame Capture 
    (OpenCV)"]
    C["Preprocessing
    (Resize, Normalize)"]
    D["YOLO
    (Inference PyTorch, ONNX Runtime)"]
    E["Tracker 
    (SORT / ByteTrack)"]
    F["Tracked objects 
    (ID, bbox, class)"]
    G["Post-processing 
    (NMS, Threshold)"]
    H["FastAPI 
    (REST, WebSocket)"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
  ```

The system is modular by design, allowing individual components (video input, inference backend, API layer) to be swapped or extended independently.


## ✨ Key Features

- Real-time video ingestion using OpenCV
- YOLO-based object detection
- Dual inference backends:
  - PyTorch (baseline, flexible)
  - ONNX Runtime (optimized, low latency)
- REST API for image-based inference
- WebSocket API for real-time streaming results
- Configurable inference backend and parameters
- Dockerized for consistent deployment

---

## ⚡ Inference Optimization

This project intentionally supports multiple inference backends to highlight performance tradeoffs:

### PyTorch
- Easier experimentation and debugging
- Flexible model manipulation
- Higher latency for real-time workloads

### ONNX Runtime
- Faster inference on CPU
- Lower and more stable latency
- Better suited for real-time and edge deployments

Model export to ONNX is handled via a dedicated script.


## 📊 Benchmarks

Basic latency and FPS benchmarks are included to compare inference backends.

| Backend   | FPS (CPU) | Avg Latency |
|---------- |-----------|-------------|
| PyTorch   | ~12 FPS   | ~80 ms      |
| ONNX      | ~25–30 FPS| ~35 ms      |

> ⚠️ Benchmark results depend on hardware and configuration.  
> These numbers are provided to illustrate relative performance trends.

Detailed results can be found in:  
`benchmarks/latency_results.md`


## 🧪 Supported Inputs

- Webcam (default)
- Video files
- RTSP streams (mock / configurable)

Input source can be changed via configuration.


## 🌐 API Interface

### REST API
- Image-based object detection
- Returns bounding boxes, labels, and confidence scores

### WebSocket API
- Real-time streaming inference
- Suitable for dashboards or monitoring tools

The API layer is built with FastAPI and designed for async, non-blocking workloads.


## 🐳 Running with Docker

### Build image
```bash
docker build -t real-time-vision-platform .
```
### Run container

```bash
docker run --rm -p 8000:8000 real-time-vision-platform
```

Once running, the API will be available at:

http://localhost:8000

## ⚙️ Configuration

- Model and inference behavior can be configured via `configs/model.yaml`, including:

- Inference backend selection

- Confidence thresholds

- Input resolution

This enables easy experimentation without code changes.

## 🧩 Design Decisions

Some notable engineering decisions:
- **Frame skipping** is used to balance throughput and latency
- **Async APIs** prevent blocking inference calls
- **ONNX Runtime** is preferred for real-time CPU inference
- **Modular layout** allows easy extension to tracking, anomaly detection, or multi-camera setups

These patterns mirror real-world production CV systems.

## 🚧 Limitations & Future Work

Add object tracking (e.g. SORT / DeepSORT)

Multi-camera orchestration

Hardware-specific optimizations (GPU, TensorRT)

Metrics export (Prometheus / Grafana)

## 📜 Disclaimer

This repository is a **generalized, open reference project**.
It does not contain proprietary code, datasets, or business logic from any previous employer or client.

## 👤 Author

AI Engineer focused on real-time computer vision systems, ML optimization, and production deployment.

If you’re a recruiter or engineer reviewing this project, feel free to reach out via GitHub or LinkedIn.



