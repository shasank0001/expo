---
subject: ml
unit: 5
topic: deep-learning
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Deep Learning

## Overview

Deep learning uses multi-layer neural networks to learn increasingly abstract representations from data. A deep network transforms raw inputs through several nonlinear layers: edges become shapes, shapes become parts, and parts become objects in an image; tokens become contextual features in text. This reduces the need for hand-designed features, but it requires data, computation, careful optimisation, and responsible evaluation.

Deep learning is an approach, not a guarantee of accuracy. It is useful for computer vision, natural-language processing, speech, recommendation, time series, and generative tasks when there is enough representative data and a clear deployment need. On small tabular data, a simpler model may be better.

## Explanation

### What makes learning “deep”?

Depth refers to the number of learned transformations between input and output. A network with several hidden layers learns a hierarchy of representations. A single hidden layer can already be universal under suitable assumptions, but deep architectures exploit useful compositional structure and make representation learning efficient for tasks such as vision and language.

### Representation learning

Traditional pipelines might calculate edges, corners, and textures by hand before classification. A CNN learns filters that respond to useful local patterns and combines them through deeper layers. A transformer learns contextual relationships among tokens. Learned representations can be reused for transfer or fine-tuning.

The representation is learned from the objective and data. It may encode irrelevant or sensitive information, and its apparent hierarchy is not automatically human-interpretable.

### Common architectures and tasks

- **CNNs:** image classification, detection, segmentation, medical imaging, and some audio.
- **RNN/LSTM/GRU:** sequences, time series, speech, and text.
- **Transformers:** language, vision, multimodal data, and long-range relationships.
- **Graph neural networks:** molecular, social, and network data.
- **Autoencoders/VAEs:** representation learning, compression, and anomaly detection.
- **GANs and diffusion models:** generation and editing.
- **Deep reinforcement-learning networks:** policies from high-dimensional state/action inputs.

### Data and transfer learning

Deep networks often need more data than classical models. Transfer learning starts from a pretrained model and adapts it using a smaller target data set. Options include freezing the backbone, fine-tuning all layers, using discriminative learning rates, or adding a task-specific head. The source domain, licence, privacy, and demographic coverage matter.

Self-supervised learning creates targets from data—for example, masked-token prediction or image contrastive objectives—so large unlabelled corpora can be used. Semi-supervised learning combines labels and unlabelled examples. These strategies do not remove the need for representative evaluation.

### Training challenges

Deep optimisation is non-convex and sensitive to initialisation, learning rate, batch size, normalisation, and data scaling. Gradients can vanish or explode. Overfitting can occur even with large models. Common controls include \(L_2\)/weight decay, dropout where appropriate, data augmentation, early stopping, and checkpointing. Residual connections, normalisation, and adaptive optimisers help optimisation but do not guarantee accuracy.

### Data representation and leakage

Images should be split by subject or capture session rather than by near-duplicate frames. Text and time series need temporal or group-aware splits. Labels and preprocessing must be available at prediction time. A high result on a random split can be meaningless.

### Evaluation and deployment

Use task-specific metrics, calibration, uncertainty, subgroup analysis, robustness tests, and an untouched test set. Compare against a simple baseline. In production, monitor input drift, prediction drift, latency, failures, and delayed task outcomes. Model updates need versioning, approval, rollback, and a fallback.

### Interpretability and fairness

Saliency, integrated gradients, concept-based tests, attention analyses, and surrogate models can provide partial explanations. They are not guaranteed causal or faithful explanations. Deep models can amplify historical bias, privacy leakage, or adversarial vulnerabilities. High-stakes uses require human review, documentation, access controls, and a way to contest outcomes.

### Limitations and cost

Training and inference can require GPUs, substantial memory, and energy. Large models may be difficult to reproduce, explain, update, or deploy on edge devices. Data licensing and the environmental cost of computation matter. Quantisation, pruning, distillation, caching, and smaller architectures can reduce cost, but should be validated for accuracy and fairness.

### When not to use deep learning

Prefer rules, optimisation, or classical models when data are scarce, the target is exact, the task is simple tabular prediction, latency is strict, or a short audit trail is more valuable than a small accuracy gain. A hybrid system can use a deep model for perception and deterministic rules for safety or policy.

### Data, evaluation, and responsible deployment

Deep models are especially sensitive to the boundary between training and deployment. For images, group by person, device, or time; for video, split before near-duplicate frames; for text and time series, use chronological or source-aware splits. Fit every transformation on training data. A random split that mixes highly similar examples can produce a score that looks excellent but cannot occur in production.

Evaluate the complete system. This includes the model, preprocessing, output threshold, abstention, latency, memory, and fallback. For probabilities, check calibration; for recommendations, check diversity and exposure bias; for generative models, check memorisation, unsafe content, and data leakage. Run subgroup and stress tests, especially when the training population differs from the served population.

A deployment plan should include:

- a model card with intended use, data, metrics, and limitations;
- versioned weights, code, preprocessing, and schema;
- an offline and online monitoring dashboard;
- drift and delayed-label alerts with an owner;
- privacy, security, fairness, and human-review controls;
- a rollback or conservative fallback;
- a retraining schedule tied to new evidence, not a calendar alone.

Deep learning is a powerful engineering choice, not a substitute for problem definition. If a small tabular model meets the target, is more interpretable, and is easier to audit, it may be the responsible choice.

## Worked examples

### Example 1: image classification

A CNN receives a 224-by-224 image. Early filters detect edges; later layers detect textures and object parts; the final layer maps features to class probabilities. Images from the same patient are grouped in the split. A small ResNet or linear baseline is compared before a large model is accepted.

### Example 2: sentiment classification

A transformer tokenises a review, adds positional information, computes self-attention, and produces a sentiment logit. A labelled validation set chooses the checkpoint and threshold. High confidence on familiar language does not guarantee correctness on slang or new topics.

### Example 3: transfer learning

A pretrained image model is frozen and a new classifier head is trained for plant disease. If the target data are small, freezing reduces overfitting. If the new domain is very different, gradual fine-tuning may improve results. The team checks licences and subgroup performance before deployment.

### Example 4: drift

A demand model trained on pre-event data is deployed during a major event. Feature distributions and prediction entropy change. Monitoring flags the shift; the team obtains labelled recent data, retrains, and temporarily falls back to a conservative rule. It does not immediately trust an unvalidated update.

## Key terms & formulas

- **Deep learning:** learning with multi-layer neural representations.
- **Representation learning:** automatically learning useful features.
- **Feature hierarchy:** lower-level patterns composed into higher-level concepts.
- **Transfer learning:** reusing a pretrained model on a related task.
- **Fine-tuning:** updating pretrained parameters for a new task.
- **Self-supervised learning:** training with automatically constructed targets.
- **CNN/RNN/transformer:** common deep architectures.
- **Residual connection:** \(y=F(x)+x\).
- **Weight decay:** parameter shrinkage.
- **Data augmentation:** label-preserving training transformations.
- **Adversarial robustness:** resistance to deliberate input perturbations.
- **Quantisation:** representing parameters with lower precision.
- **Knowledge distillation:** training a smaller model to mimic a larger one.
- **Model drift:** degradation or change in model/data relationship over time.
- **Deep-learning pipeline:** data, architecture, loss, optimiser, evaluation, deployment, and monitoring.

## Common mistakes

1. **Using deep learning because it is fashionable.** A baseline and requirements decide suitability.
2. **Ignoring data scale and domain coverage.** Large models can memorise and fail on unseen groups.
3. **Using random image splits with duplicate frames.** This leaks near-identical information.
4. **Confusing a high score with generalisation.** Test on later, external, and subgroup data.
5. **Treating explanations as causal facts.** Saliency or attention is method-dependent.
6. **Ignoring deployment cost and licensing.** A model may be too large or legally unusable.
7. **Updating a live model without monitoring and rollback.** Drift can cause silent harm.
8. **Failing to report uncertainty and abstention.** Overconfident predictions are risky.

## Exam prep

### Likely 2-mark questions

- **Define deep learning.** Use of multi-layer neural networks to learn hierarchical representations.
- **Give two deep-learning architectures.** CNN, RNN/LSTM, transformer, autoencoder, GAN, or GNN.
- **What is transfer learning?** Reusing knowledge from a pretrained model for a new task.
- **Name one benefit and one cost of deep learning.** Benefit: rich representations; cost: data/compute/interpretability.

### Long-answer prompts

- **Explain representation learning in deep networks.** Compare handcrafted features, CNN hierarchy, and transformer context.
- **Describe a complete deep-learning project.** Include data, architecture, loss, optimisation, augmentation, evaluation, and monitoring.
- **Compare CNNs, RNNs, and transformers for sequential/image data.** Discuss assumptions, parallelism, locality, and tasks.
- **Why can deep learning fail despite high accuracy?** Discuss leakage, shift, bias, overfitting, robustness, data, and deployment.
- **How should a deep model be governed?** Cover documentation, privacy, fairness, explanation, human review, versioning, and rollback.
