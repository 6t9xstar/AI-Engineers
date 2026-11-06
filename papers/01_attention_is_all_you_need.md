# Attention Is All You Need (Vaswani et al., 2017)
- **Core Breakthrough**: Replaced recurrent (RNN/LSTM) and convolutional layers with Scaled Dot-Product Multi-Head Self-Attention.
- **Formula**: $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$.
- **Impact**: Enabled massive parallel training across GPUs, unlocking modern LLMs.
