## Mitigate the issue:

### 1. Multi-Scale Positional Encoding (Ms-PoE)
- an effective strategy to downscale positional information
- RoPE encodes position as f(x,m) = xe^imθ
    - this position is gets substituted with m/r -> this forces long-distance tokens to reside in shorted range, allevating the long-term decay effect by factor of r

### 2. Context Denoising in Attention
- model attention as a signal + noise decomposition where noise grows with context length
- reweight softmax(QK^T) to enhance high-confidence alignments and dampen diffuse ones (attention sharpening)
    - this reduces entropy of the attention distribution, filtering out low-SNR tokens that dominate in the middle of context regions
- this is applied progressively across layers, so each layer refines and denoises representations
    - results in increasing signal-to-noise ratio (SNR), enabling relevant middle tokens to remain dominant despite heavy context clutter