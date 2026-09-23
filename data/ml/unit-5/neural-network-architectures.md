---
subject: ml
unit: 5
topic: neural-network-architectures
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Architectures of Neural Networks

## Overview

An architecture specifies how neurons are arranged and connected: input and output types, hidden layers, recurrence, convolution, attention, skip connections, and parameter-sharing patterns. Architecture determines what kinds of patterns a network can learn, how parameters are shared, and how efficiently it processes data.

The syllabus treats architectures as a progression from basic feed-forward networks to networks suited to images, sequences, and complex representations. The right architecture follows the data and task; depth is not automatically better.

## Explanation

### Feed-forward multilayer perceptron

A multilayer perceptron (MLP) connects every unit in one layer to every unit in the next:

\[
Z^{(\ell)}=W^{(\ell)}A^{(\ell-1)}+b^{(\ell)},\quad
A^{(\ell)}=\phi(Z^{(\ell)}).
\]

It is appropriate for tabular numerical/categorical data and fixed-size vectors. It does not naturally preserve spatial, temporal, or set structure, and it can be expensive when the input is large. Hidden width and depth control capacity.

### Convolutional neural networks

A CNN uses convolutional filters that slide across an image or other grid. For a kernel \(K\),

\[
Y_{i,j,k}=b_k+\sum_{u,v,c}K_{u,v,c,k}X_{i+u,j+v,c}.
\]

Weight sharing means the same filter detects a feature at every location. Pooling or strided convolutions reduce spatial size. CNNs exploit local connectivity and translation-related patterns, making them effective for image classification, detection, segmentation, and some audio tasks.

### Recurrent neural networks

An RNN carries a hidden state:

\[
h_t=\phi(W_xx_t+W_hh_{t-1}+b),\qquad y_t=g(W_yh_t).
\]

The state gives context from earlier time steps. Basic RNNs can have difficulty retaining long histories because gradients vanish or explode. Long short-term memory (LSTM) and gated recurrent unit (GRU) networks use gates to control information flow. They are used for sequences, time series, speech, and text.

### Attention and transformers

Attention computes a weighted combination of values:

\[
\operatorname{Attention}(Q,K,V)
=\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
\]

Self-attention lets each position incorporate information from other positions. Transformers stack self-attention, position representations, feed-forward layers, and residual/normalisation blocks. They support parallel training and long-range relationships, but self-attention can be costly for long sequences. Positional information must be supplied because attention alone is permutation-equivariant.

### Residual and skip connections

A residual block learns

\[
y=F(x)+x
\]

(or a learned projection when shapes differ). The shortcut gives gradients a direct path and makes very deep optimisation easier. It does not eliminate all degradation or overfitting; architecture and training still need validation.

### Graph and set architectures

Graph neural networks aggregate information from neighbours using a permutation-invariant operation. Set networks use pooling or attention so that input order does not define the output. They are appropriate when observations are graphs, molecules, or unordered sets rather than fixed vectors.

### Autoencoders and generative architectures

An autoencoder encodes \(x\) to a latent code \(z\) and reconstructs it:

\[
z=E(x),\qquad \hat x=D(z).
\]

The bottleneck encourages a useful representation. Variational autoencoders model a probability distribution over latent codes; GANs use a generator and discriminator with an adversarial objective. These architectures are useful for compression, anomaly detection, representation learning, and generation, but validation can be difficult.

### Architecture choice and inductive bias

MLPs assume a fixed vector; CNNs assume local grid structure; RNNs assume ordered sequence; attention represents relationships; graph networks respect connectivity; set networks ignore order. The architecture should match the data-generating process. Compare a simple baseline, monitor parameter count and latency, and test on an independent distribution.

### Width, depth, and capacity

More layers and units increase representational capacity and parameter count. They can improve performance on complex data but increase optimisation difficulty, memory, latency, and overfitting risk. Use validation curves, parameter-efficiency tests, early stopping, and a model-complexity budget rather than choosing depth by habit.

### Architecture selection in practice

Begin with the data's invariances. If a label should not change when an image moves slightly, a CNN's local shared filters are a useful bias. If the order of a time series matters, a recurrent state or positional attention is needed. If a graph's topology defines the neighbourhood, a message-passing network is more appropriate than flattening the adjacency matrix. If a tabular row has no natural order, an MLP with carefully encoded features is often simpler.

Architecture changes should be justified with an experiment. A deeper residual network may improve long-range gradients, but it increases compute and can still overfit. Attention may improve a language task, but its quadratic memory behaviour may violate a latency budget. A larger embedding table may improve rare categories, but it increases memory and privacy risk. Record parameters, training time, inference latency, and test performance together.

Architecture and objective are coupled. A softmax output with cross-entropy suits mutually exclusive classes; independent sigmoids suit multilabel labels; a linear output suits an unrestricted regression target. A recurrent layer is not automatically a time-series solution if the evaluation split allows future information. A CNN is not automatically explainable because its filters are local.

## Worked examples

### Example 1: image convolution

A 3-by-3 filter detects a vertical edge at any location. Sharing the filter across the image avoids learning a separate edge detector for every pixel position. Multiple filters detect edges, textures, and parts; later layers combine them.

### Example 2: RNN memory

For a sequence of words, an RNN's hidden state summarises earlier words. An LSTM's gates decide what to store and forget, which helps with long dependencies. If the task is classification from the final state, only a summary may be needed.

### Example 3: attention

In self-attention, every token computes queries, keys, and values. A token assigns high weight to semantically relevant tokens regardless of distance, subject to position information and computational limits.

### Example 4: residual learning

If the desired mapping is close to the identity, a residual block starts from \(x\) and learns a correction \(F(x)\). This is easier to optimise than forcing the whole layer to reconstruct the identity. The shortcut is a structural inductive bias, not a guarantee of accuracy.

## Key terms & formulas

- **Architecture:** arrangement and connectivity of network components.
- **MLP:** fully connected feed-forward network.
- **CNN:** convolutional network with shared filters.
- **Convolution:** sliding local weighted sum.
- **Pooling:** spatial aggregation or downsampling.
- **RNN:** recurrent network with a hidden state.
- **LSTM/GRU:** gated recurrent architectures.
- **Self-attention:** attention over representations in the same sequence.
- **Attention:** weighted combination of values.
- **Transformer:** architecture built primarily from attention and feed-forward blocks.
- **Residual connection:** \(y=F(x)+x\).
- **Autoencoder:** encoder–decoder trained to reconstruct input.
- **GNN:** graph neural network using neighbourhood aggregation.
- **Inductive bias:** architectural preference for certain structures.
- **Parameter count:** number of learned weights and biases.
- **Perceptron:** early linear threshold network.

## Common mistakes

1. **Using an MLP for spatial data without a baseline.** It ignores useful locality and parameter sharing.
2. **Forgetting positional information in a transformer.** Self-attention alone does not encode order.
3. **Assuming recurrence is always better for sequences.** Transformers can parallelise long-context training.
4. **Adding depth without checking capacity and latency.** Optimisation and overfitting can worsen.
5. **Ignoring parameter sharing.** CNNs and other architectures gain efficiency from shared rules.
6. **Treating residual connections as a universal fix.** Optimisation and data still matter.
7. **Ignoring a simple baseline.** A simpler model may be more accurate, efficient, and fair.

## Exam prep

### Likely 2-mark questions

- **Name four neural architectures.** MLP, CNN, RNN/LSTM, transformer, autoencoder, GAN, or GNN.
- **Why do CNNs use weight sharing?** To detect a feature at different locations efficiently.
- **What is the main idea of residual learning?** Add the input to a learned transformation: \(y=F(x)+x\).
- **What does self-attention do?** Computes relationships between positions in a sequence.

### Long-answer prompts

- **Compare MLPs, CNNs, RNNs, and transformers.** Discuss data assumptions, connectivity, parameters, parallelism, and tasks.
- **Explain the convolutional operation.** Include a formula, local connectivity, weight sharing, pooling, and image use.
- **Why are residual connections useful in deep networks?** Discuss optimisation, gradients, identity mappings, and shape handling.
- **Select an architecture for a sequence task.** Justify recurrence/attention/MLP, positional information, data scale, and latency.
