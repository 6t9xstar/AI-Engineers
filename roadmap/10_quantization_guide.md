# 10: Model Quantization Formats & Trade-offs

Quantization compresses 16-bit floating-point weights (FP16/BF16) into 8-bit, 4-bit, or 2-bit representations.

## Format Breakdown

### 1. GGUF (llama.cpp)
- **Target**: CPU + GPU offloading, consumer hardware, edge devices.
- **K-quants**: Uses mixed precision across layers (`Q4_K_M`, `Q5_K_M`) to preserve attention weights while aggressively compressing feed-forward layers.

### 2. AWQ (Activation-aware Weight Quantization)
- **Target**: High-throughput GPU inference (vLLM, TensorRT-LLM).
- **Core Concept**: Protects the 1% salient weights based on activation magnitudes, yielding higher perplexity retention than uniform post-training quantization.

### 3. EXL2 (ExLlamaV2)
- **Target**: Fastest single/multi-GPU inference on NVIDIA hardware.
- **Features**: Fractional quantization (e.g. 4.25 bits/weight).
