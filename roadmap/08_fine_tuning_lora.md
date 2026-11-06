# 08: Parameter-Efficient Fine-Tuning: LoRA & QLoRA

Fine-tuning full weights of modern 7B–70B models requires multi-node GPU clusters. Parameter-Efficient Fine-Tuning (PEFT) freezes the base model and adapts small low-rank matrices.

## Mathematical Formulation of LoRA
For a pre-trained weight matrix $W_0 \in \mathbb{R}^{d 	imes k}$, LoRA decomposes the update $\Delta W$ into two low-rank matrices $A$ and $B$:

$$W = W_0 + \Delta W = W_0 + rac{lpha}{r} (B \cdot A)$$

Where:
- $B \in \mathbb{R}^{d 	imes r}$ (initialized to zero)
- $A \in \mathbb{R}^{r 	imes k}$ (initialized with Gaussian noise)
- $r \ll \min(d, k)$ is the rank (typically $r \in [8, 64]$)
- $lpha$ is a scaling hyperparameter (typically $lpha = 2r$)

## QLoRA (Quantized LoRA)
QLoRA reduces VRAM requirements by 65% through three innovations:
1. **NF4 (NormalFloat 4)**: Information-theoretically optimal quantile quantization for normal distribution weights.
2. **Double Quantization**: Quantizes quantization constants to save an additional 0.37 bits/param.
3. **Paged Optimizers**: Uses CUDA Unified Memory to prevent out-of-memory spikes during gradient checkpointing.
