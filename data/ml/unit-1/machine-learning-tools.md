---
subject: ml
unit: 1
topic: machine-learning-tools
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Tools in Machine Learning

## Overview

ML tools help people store, clean, explore, train, evaluate, and deploy models. They range from general-purpose languages such as Python and R to libraries for data handling, visualisation, traditional algorithms, and deep-learning frameworks. A tool is useful only when it supports the problem, team skills, reproducibility, and deployment requirements.

The right tool choice is therefore part of an engineering decision. A notebook is excellent for exploration but may be an unsafe production service; a framework can make a model powerful while making its assumptions easy to overlook. Tools should support—not replace—understanding of the data and the method.

## Explanation

### Programming environments

**Python** is widely used because it has a large scientific ecosystem, readable syntax, and broad adoption in web and deployment systems. It is a good default for end-to-end ML. **R** is particularly strong for statistical analysis, visualisation, and domain work in biostatistics and social science. **Jupyter** and similar notebook environments allow code, equations, plots, and narrative together. Scripts, modules, tests, and version control are still needed for reliable production work.

### Data manipulation and numerical computing

- **pandas** provides data frames, filtering, grouping, joins, reshaping, and basic missing-value handling.
- **NumPy** provides efficient arrays and vectorised numerical operations.
- **polars** is a high-performance alternative for large in-memory data.
- **Spark** and **Dask** help scale data processing when a single machine is insufficient.

A table operation must be checked. A join can duplicate rows, a mean can hide heavy-tailed values, and a date filter can leak future information. Tool convenience does not guarantee data correctness.

### Visualisation and exploratory analysis

**Matplotlib** provides fine control over plots. **Seaborn** offers convenient statistical views. Plotly and similar packages create interactive charts. Visualisation helps reveal skew, missingness, outliers, correlations, class overlap, and drift. A plot is evidence about a data-generating process, not proof of causality.

### Classical machine learning

**scikit-learn** supplies estimators for preprocessing, regression, classification, clustering, dimensionality reduction, model selection, pipelines, and metrics. Its `Pipeline` and `ColumnTransformer` objects help keep preprocessing inside a train-only workflow. It is a strong first choice for classical baselines and many production systems.

Other ecosystems include **xgboost** and **LightGBM** for gradient-boosted trees, **statsmodels** for statistical models and inference, and **PyMC** or similar packages for Bayesian modelling. A model should be chosen because it matches the data and objective, not because a library is popular.

### Deep-learning frameworks

- **TensorFlow** and **Keras** provide general tensor computation and high-level neural-network APIs.
- **PyTorch** provides flexible tensor operations, autograd, and a large research ecosystem.
- **JAX** focuses on differentiable numerical computation and composable transformations.
- **ONNX** and related tools provide portable representations of trained models.
- **Hugging Face** tools host and adapt many pretrained models, subject to licence and data terms.

Frameworks automate differentiation and GPU kernels, but the user must still define the data, architecture, loss, regularisation, and evaluation. A high-level API cannot repair leakage or a mistaken target.

### Experiment, deployment, and monitoring

Version control tracks code. **DVC**, **MLflow**, **Weights & Biases**, or a comparable system can track parameters, metrics, artefacts, and model versions. Containers such as Docker package dependencies. REST/gRPC services, serverless functions, mobile runtimes, or edge devices serve models. Monitoring tools track latency, errors, data drift, prediction drift, and business outcomes.

A model registry should store the exact artefact, preprocessing state, schema, training-data version, metric report, and approval status. “Latest model” is not a sufficient deployment identifier.

### A tool-aware workflow

1. **Explore:** notebook, pandas, NumPy, and plots.
2. **Prototype:** scikit-learn, a clear pipeline, and a simple baseline.
3. **Scale:** Spark/Dask for data, a suitable model library, and distributed training if justified.
4. **Deep learn:** PyTorch/TensorFlow/Keras with checkpoints and reproducible seeds.
5. **Package:** versioned environment, container, model artefact, and schema.
6. **Serve:** API or batch service with authentication, limits, and fallback.
7. **Operate:** dashboards, alerts, incident playbooks, retraining, and rollback.

### Reproducibility and governance

Pin package versions, record random seeds where possible, keep data lineage, and report the exact evaluation protocol. Use licences that permit the intended use. Sensitive data needs access control, encryption, anonymisation, retention rules, and deletion procedures. A notebook copied without its data and environment is not a reproducible experiment.

## Worked examples

### Example 1: a scikit-learn pipeline

A preprocessing step imputes missing numeric values and scales them; a second step one-hot encodes categories; a logistic-regression estimator predicts the class. Wrapping these steps in a pipeline makes cross-validation correct: each fold fits its transformations only on its training portion.

### Example 2: model version record

A registry stores `model-v7`, the training commit, dataset snapshot, feature schema, `accuracy=0.84` on a defined test set, calibration report, and approval by a reviewer. If a new release has 0.86 average accuracy but poor performance for a small group, it is not automatically better.

### Example 3: deployment fallback

A fraud API can score transactions immediately, but if the model service is unavailable, a rules engine can apply a conservative limit and queue review. A fallback preserves safety while making the system resilient.

### Example 4: scale decision

A dataset that fits comfortably in memory should not be moved to a distributed framework simply because distributed tools exist. Measure memory, latency, cost, and operational complexity first.

## Key terms & formulas

- **IDE/notebook:** an interactive programming and documentation environment.
- **Data frame:** a tabular structure with named columns and rows.
- **Pipeline:** a sequence of transformations plus an estimator fitted as one unit.
- **Tensor:** a multidimensional numeric array.
- **Automatic differentiation:** software that computes derivatives from a computation graph.
- **GPU:** parallel hardware useful for dense matrix operations.
- **Container:** a packaged runtime with dependencies.
- **Model artefact:** the serialised model and required preprocessing state.
- **Experiment tracking:** recording code, parameters, metrics, and outputs.
- **Feature store:** a managed feature data service.
- **Serving:** exposing a trained model to users or systems.
- **Observability:** measurements that show whether a service behaves as expected.
- **Fallback:** an alternative behaviour when a model or service fails.
- **Dependency pinning:** recording exact compatible package versions.

## Common mistakes

1. **Installing a deep-learning framework before checking a simple baseline.** Start with the simplest adequate method.
2. **Doing preprocessing outside a pipeline.** Information from validation/test folds can leak into training.
3. **Calling a notebook production software.** Refactor tested, monitored, and versioned components.
4. **Recording only the final metric.** Save the split, seeds, parameters, and artefacts.
5. **Ignoring licence and privacy terms of pretrained data.** A technically available model may not be legally or ethically deployable.
6. **Scaling before measuring.** Distributed tools add cost and failure modes.
7. **Treating a dashboard as monitoring.** It needs thresholds, alerts, ownership, and a response plan.

## Exam prep

### Likely 2-mark questions

- **Name two common ML tools.** Examples: scikit-learn, pandas, NumPy, PyTorch, TensorFlow, or Jupyter.
- **What is a pipeline?** A sequence of preprocessing and modelling steps fitted and evaluated together.
- **Why is version control important?** It records changes and makes experiments and deployments traceable.
- **What is model monitoring?** Continuous measurement of service health and data/model behaviour after deployment.

### Long-answer prompts

- **Describe tools used at different stages of an ML project.** Cover storage, exploration, modelling, deep learning, deployment, and monitoring.
- **How can an ML experiment be made reproducible?** Discuss code/data versions, environments, seeds, metrics, artefacts, and documentation.
- **Compare a notebook workflow with a production workflow.** Discuss iteration, testing, security, scalability, and monitoring.
- **Explain why a simple baseline is important when choosing tools or algorithms.** Use interpretability, cost, latency, and data size.
