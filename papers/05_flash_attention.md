# FlashAttention: Fast and Memory-Efficient Exact Attention (Dao et al., 2022)
- **Core Breakthrough**: IO-aware tiling algorithm that computes exact softmax attention without materializing the $N \times N$ attention matrix in GPU HBM.
- **Impact**: 3x speedup in attention runtime and linear memory scaling.
