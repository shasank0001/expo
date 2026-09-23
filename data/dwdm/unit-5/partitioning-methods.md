---
subject: dwdm
unit: 5
topic: partitioning-methods
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Partitioning Methods

## Overview

Partitioning clustering directly divides the data into a chosen number of clusters. Objects are assigned to groups and representatives or centers are updated until the assignment stabilizes. **K-means** is the standard method for numeric data; **k-medoids/PAM** uses an actual representative and can use arbitrary dissimilarities. These methods are simple and scalable, but they are sensitive to initialization, outliers, feature scale, cluster shape, and the choice of \(k\).

## Explanation

### 1. K-means objective

For \(k\) clusters with centroids \(\mu_1,\ldots,\mu_k\), K-means minimizes within-cluster squared Euclidean error:

\[
J=\sum_{r=1}^{k}\sum_{x\in C_r}\|x-\mu_r\|^2
=\sum_{r=1}^{k}\sum_{x\in C_r}\|x\|^2-\sum_{r=1}^{k}n_r\|\mu_r\|^2.
\]

The second expression is useful for implementation because it avoids explicitly forming every squared distance in the objective. K-means assumes numeric features, a suitable squared-Euclidean geometry, and roughly convex clusters.

### 2. Algorithm

1. Choose \(k\).
2. Initialize \(k\) centers, often with random distinct observations.
3. Assign each object to the closest center.
4. Recompute each center as the mean of its assigned objects.
5. Repeat 3–4 until assignments or centers change negligibly or a maximum iteration is reached.
6. Run several initializations and retain the lowest \(J\).

An empty cluster must be handled, commonly by reseeding it or choosing the point farthest from its current center. The algorithm is a local optimization: it can stop at a local minimum, not necessarily a global one.

### 3. Initialization

Random points can be unlucky and produce poor or empty clusters. **K-means++** chooses initial centers with probabilities favoring points far from existing centers, while still allowing the data to determine candidates. **Forgy** initializes centers randomly from the data. Multiple restarts or a smarter seeding strategy improve stability. The initialization should never use test labels.

### 4. Choosing \(k\)

There is no universally correct \(k\). Use domain requirements, cross-validation, the elbow method, silhouette, gap statistic, stability, and interpretability. The elbow method plots \(J(k)\); a bend can suggest a compactness benefit. A very small \(k\) hides structure; a very large \(k\) can split a real group into arbitrary pieces. Report the rationale and sensitivity.

### 5. K-medoids and PAM

K-medoids chooses a medoid, an actual data object, as the representative of each cluster and minimizes total dissimilarity. It tolerates non-Euclidean distances and is less sensitive to extreme values because a medoid cannot be pulled outside the observed data. **PAM (Partitioning Around Medoids)** alternates a BUILD phase, which constructs an initial set of medoids, and a SWAP phase, which tests whether exchanging a medoid improves the objective. PAM is more robust but generally costs more than K-means, especially for large \(n\).

### 6. K-modes and categorical variants

For categorical data, the mode replaces the mean and a simple mismatch dissimilarity replaces Euclidean distance. K-modes minimizes total mismatch, choosing the most frequent category in each cluster. Mixed versions such as k-prototypes combine numeric means and categorical modes.

### 7. Strengths and limitations

**Strengths:** simple, fast for large numeric data, easy to implement, and scalable with parallel computation.

**Limitations:** initialization sensitivity, outliers, spherical/convex cluster assumption, hard assignments, difficulty with elongated or irregular groups, sensitivity to \(k\), and the need to scale features. Mini-batch K-means speeds computation but can reduce solution quality and stability.

## Worked examples

### Example 1: One complete K-means iteration

Points: \(A=(1,1),B=(2,1),C=(1,2),D=(8,8),E=(9,8)\). Let \(k=2\), initial centers \(m_1=(1,1)\), \(m_2=(8,8)\).

Distances assign \(A,B,C\) to cluster 1 and \(D,E\) to cluster 2. New means:

\[
m_1=(4/3,4/3),\quad m_2=(8.5,8).
\]

Reassigning leaves the same partition. The within-cluster squared error is

\[
J=\frac{4}{3}+\frac12=\frac{11}{6}\approx1.83.
\]

The final labels and centers are stable for this initialization.

### Example 2: Bad initialization

For the same points, if centers are initially \(A=(1,1)\) and \(B=(2,1)\), both lie in the left group and one may attract both \(D,E\), producing a poor partition. K-means++ or multiple random restarts reduces this risk. Compare final \(J\) across runs, not just the first result.

### Example 3: K-means versus K-medoids

Add a far point \(F=(100,100)\). A centroid of a cluster containing \(D,E,F\) is pulled toward \(F\); a medoid remains one of \(D,E,F\), and the mismatch/total distance criterion can keep the center near the ordinary points. The exact effect depends on the distance and initialization, but k-medoids is generally more outlier-resistant.

### Example 4: K-modes

Objects are \((A,A,B)\), \((A,B,B)\), and \((B,B,C)\). The mode of each column is A, B, B, so the center is `(A,B,B)`. The algorithm minimizes category mismatches rather than treating category labels as numeric magnitudes.

### Example 5: Choose \(k\) by silhouette

For k values 2 through 5, calculate average silhouette \(s(i)=(b(i)-a(i))/\max(a(i),b(i))\), where \(a(i)\) is mean within-cluster dissimilarity and \(b(i)\) is the mean dissimilarity to the nearest other cluster. Select a value with good separation and stability, not automatically the largest silhouette if the resulting groups are operationally meaningless.

## Key terms & formulas

- **Partitioning:** directly assign objects to \(k\) clusters.
- **Centroid:** mean vector of a cluster.
- **Medoid:** actual object representing a cluster.
- **K-means objective:** \(J=\sum_r\sum_{x\in C_r}\|x-\mu_r\|^2\).
- **Assignment:** choose the nearest centroid.
- **Update:** recompute centroid means.
- **K-means++:** spread-out initialization strategy.
- **PAM:** BUILD plus SWAP medoid optimization.
- **K-modes:** mode-based categorical clustering.
- **Elbow method:** inspect within-cluster error versus \(k\).
- **Mini-batch K-means:** approximate/scalable assignment using batches.

## Common mistakes

1. **Forgetting to standardize numeric features:** larger-scale attributes dominate Euclidean distance.
2. **Assuming convergence means a global optimum:** K-means reaches a local solution.
3. **Using one random initialization:** use restarts and k-means++.
4. **Ignoring empty clusters:** a special case must be handled.
5. **Applying K-means to categorical labels:** use a mismatch or k-modes method.
6. **Selecting k without validation:** compactness alone does not establish usefulness.
7. **Ignoring arbitrary cluster shapes:** K-means favors convex clouds.
8. **Using a medoid without saying the distance:** k-medoids depends on the dissimilarity.

## Exam prep

**Likely 2-mark questions**
1. State the K-means objective. *Hint: minimize within-cluster squared distance.*
2. Name the K-means assignment and update steps. *Hint: nearest centroid; recompute means.*
3. Differentiate k-means and k-medoids. *Hint: mean versus actual representative.*

**Likely long-answer questions**
1. Run K-means for several iterations on a supplied table. *Hint: initial centers, distances, assignments, means, objective, convergence.*
2. Compare K-means, k-medoids, and k-modes. *Hint: numeric, arbitrary-distance robust, and categorical variants.*
3. Explain ways to choose k and diagnose a poor initialization. *Hint: elbow, silhouette, stability, domain meaning, k-means++ and restarts.*
