---
subject: ml
unit: 2
topic: data-preprocessing
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Data Pre-Processing

## Overview

Data pre-processing transforms raw observations into a representation that is suitable, safe, and useful for a model. It includes cleaning, handling missing values, encoding categories, scaling numerical features, reducing or creating features, and constructing train/test pipelines. Pre-processing is not cosmetic: the representation determines what a model can learn.

The same transformation can help one algorithm and hurt another. Standardisation is often useful for distance-based or gradient-based models but may be unnecessary for a tree. Text normalisation can remove useful information. Every choice should be justified by the data and the learning method.

## Explanation

### A preprocessing pipeline

A common sequence is:

1. validate schema and types;
2. correct or quarantine invalid values;
3. handle duplicate records;
4. impute missing numerical values and encode missingness;
5. encode categorical, text, image, or time features;
6. scale or transform numerical features if needed;
7. select or create useful features;
8. fit the estimator and evaluate on held-out data.

The crucial rule is that parameters learned from data—means, standard deviations, vocabularies, category levels, imputation values, feature-selection choices—must be fitted on the training portion and then applied unchanged to validation, test, and production data.

### Cleaning and missing-value handling

Use domain validation before generic algorithms. A missing value may mean unknown, not applicable, not collected, or a failed sensor. Numeric imputation can use the training mean or median:

\[
x'_{ij}=\begin{cases}
x_{ij},&x_{ij}\text{ observed},\\
\bar x_j,&x_{ij}\text{ missing},
\end{cases}
\]

with an optional missing indicator \(m_{ij}\). Median imputation is robust to skew. Model-based imputation can use other features but may create circular assumptions. Categorical imputation may use a special “unknown” level rather than the mode.

### Encoding categorical variables

- **One-hot encoding** creates a binary column for each level and suits nominal data.
- **Ordinal encoding** maps ordered levels to integers and suits genuinely ordered categories.
- **Target encoding** replaces a category with an average target, but it must be calculated out-of-fold in training to avoid leakage and can encode target bias.
- **Hashing** maps many values to a fixed number of features and controls memory, but collisions are possible.
- **Embedding** learns a vector representation, useful for high-cardinality categories, text, and neural models.

For an unseen category, choose an explicit unknown policy. Never let an accidental integer code imply an order.

### Scaling and transformation

**Standardisation (z-score):**

\[
z=\frac{x-\mu}{\sigma}.
\]

It centres features around zero and gives unit variance. **Min–max scaling** maps to a chosen interval but is sensitive to outliers:

\[
x'=\frac{x-\min x}{\max x-\min x}.
\]

**Robust scaling** uses median and interquartile range. **Log or power transforms** reduce right skew, but require non-negative values and domain interpretation. Quantile or rank transformations can reduce distributional sensitivity but change interpretability. Fit each transform using training data only.

### Text and image preprocessing

Text preprocessing can include lowercasing, tokenisation, removing punctuation, stop-word filtering, stemming or lemmatisation, n-grams, TF–IDF, and sequence truncation. The correct choice depends on language and task; negation and rare words may be important in sentiment or safety tasks.

Image preprocessing can include resizing, cropping, normalisation, colour conversion, augmentation, and format handling. Augmentation should represent plausible deployment variation and must not create leakage or unrealistic images. Objects may be lost by an overly aggressive crop.

### Feature engineering

Feature engineering creates signals from domain knowledge. Examples include:

- ratios such as spend per order;
- counts or rates per month;
- lag and rolling summaries for time series;
- interactions such as product × region;
- text lengths, keyword counts, or embeddings;
- cyclical encodings for hour and season;
- differences, slopes, and temporal changes.

A derived feature is valid only if it is available at prediction time. A feature such as “final score” calculated after the decision is leakage even if it improves validation.

### Feature selection and reduction

Filter methods score features using statistics, distance, or model-independent criteria. Wrapper methods search subsets using model performance. Embedded methods select features during training, as with L1 regularisation or tree importance. Dimensionality reduction such as PCA creates components rather than selecting original features. All methods need validation and a rationale; a high number of features can cause overfitting, latency, and interpretability problems.

### Data splitting and leakage

A typical classification split is stratified so class proportions are roughly preserved. Time data require chronological splits. Repeated subjects or devices require group splits. A pipeline should be fitted inside each training fold:

\[
\text{fit preprocessing on }D_{\text{train}},\qquad
\text{apply to }D_{\text{valid/test}}.
\]

Leakage can come from target values, future timestamps, duplicate records, global normalisation, feature selection, vocabulary construction, or preprocessing performed before the split.

### Choosing transformations

Use cross-validation and domain knowledge. A preprocessing choice that improves a single test score but harms interpretability, fairness, or production compatibility may be a bad choice. Record the reason, parameters, and any categories handled as unknown.

### Preprocessing as a controlled experiment

Every transformation should have a reason and an evaluation. A scaler may help distance-based or gradient-based models but may not help a tree. One-hot encoding may add many columns for a high-cardinality field, while target encoding can be efficient but must be computed out-of-fold. A feature that is convenient in a notebook can be expensive or unstable online. Record the fitted transformation, memory footprint, latency, and behaviour on unseen categories.

Validate preprocessing choices as part of the model pipeline. If a transformation improves a score only when fitted on the full data, the improvement is likely leakage. If it changes subgroup performance, report that trade-off. A robust pipeline can be reproduced at training and serving time and can be rolled back with the model version.

## Worked examples

### Example 1: numeric preprocessing

Training ages have mean 40 and standard deviation 12. A new age of 52 becomes

\[
z=(52-40)/12=1.
\]

A model using distance or gradient optimisation can then work with a more comparable scale. The mean and standard deviation must be reused for every later age.

### Example 2: one-hot encoding

A product colour has `red`, `blue`, and `green`. One-hot columns are

\[
[\text{red}=1,\text{blue}=0,\text{green}=0]
\]

for a red item. An unseen `purple` item maps all three to zero, or to an explicit unknown feature if the pipeline supports it.

### Example 3: time-series lag

For daily sales, yesterday's sales can be a feature for tomorrow's forecast:

\[
\hat y_{t+1}=f(y_t,y_{t-1},\text{promotion}_t,\text{weather}_t).
\]

A value from after \(t+1\) cannot be used. The split and lag construction must respect time.

### Example 4: leakage through scaling

A scaler is fitted on all rows before splitting. The validation mean and standard deviation influence the training transformation. Although no target is used, the representation has seen validation distribution. Fit the scaler within each training fold instead.

## Key terms & formulas

- **Pre-processing:** transformations before model fitting.
- **Imputation:** replacing missing values.
- **One-hot encoding:** binary indicator for each category.
- **Ordinal encoding:** integer mapping of ordered categories.
- **Standardisation:** \(z=(x-\mu)/\sigma\).
- **Min–max scaling:** \(x'=(x-\min)/(\max-\min)\).
- **Robust scaling:** transformation using median and IQR.
- **Feature engineering:** creation of informative derived features.
- **Feature selection:** choosing a subset of original features.
- **Dimensionality reduction:** representation with fewer dimensions.
- **Pipeline:** preprocessing and estimator fitted together.
- **Leakage:** information unavailable at prediction time influencing training.
- **Out-of-fold encoding:** target or category statistics computed on training folds other than the current row.
- **Augmentation:** label-preserving training transformation for images or sequences.

## Common mistakes

1. **Fitting a scaler before splitting.** This leaks validation distribution.
2. **Using one-hot encoding for a naturally ordered ordinal variable.** A numeric distance may be meaningful, so choose deliberately.
3. **Dropping rare categories silently.** Keep unknown/other handling and monitor new levels.
4. **Using all text words equally.** TF–IDF or domain-specific tokenisation may be needed.
5. **Creating features from future values.** This is target or temporal leakage.
6. **Assuming preprocessing fixes a bad target.** It cannot repair a biased or undefined label.
7. **Ignoring the production input distribution.** A transform that works offline may fail on new values.

## Exam prep

### Likely 2-mark questions

- **Define data pre-processing.** Transforming raw data into a suitable, safe representation for learning.
- **State the z-score formula.** \(z=(x-\mu)/\sigma\).
- **When is one-hot encoding suitable?** For nominal categories with no natural numerical order.
- **What is leakage?** Use of information not available at prediction time, making evaluation optimistic.

### Long-answer prompts

- **Explain a complete pre-processing pipeline for a classification data set.** Cover cleaning, missingness, encoding, scaling, features, splitting, and leakage prevention.
- **Compare one-hot, ordinal, target, and embedding representations.** Discuss assumptions, advantages, leakage, and suitable models.
- **How would you preprocess text data?** Discuss cleaning, tokenisation, vectors, n-grams, TF–IDF, sequence length, and validation.
- **Why is fitting a pipeline important?** Explain how it preserves the train/test boundary and makes deployment reproducible.
