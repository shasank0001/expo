---
subject: dwdm
unit: 5
topic: graph-mining-approaches
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Graph Mining Approaches

## Overview

A graph represents objects as vertices and relationships as edges. Graph mining studies structure in networks such as social links, transactions, citations, roads, proteins, and computer systems. For cluster analysis, a common task is **graph clustering**: divide vertices into groups with many internal edges and few edges between groups. The same graph can also support frequent subgraph, motif, path, and anomaly mining.

## Explanation

### 1. Graph representation

A graph \(G=(V,E)\) has a vertex set \(V\) and edge set \(E\). Edges may be directed or undirected, weighted or unweighted, and labeled or unlabeled. A neighbor of \(v\) is a vertex joined to \(v\). **Degree** is the number of incident edges; degree can be separated into in-degree and out-degree for directed graphs. A path is a sequence of connected vertices; a cycle returns to its start. A connected component has no path to another component.

A graph is weighted when an edge carries strength, such as transaction value or similarity. Multigraphs allow multiple edges between the same pair. A directed edge can model “follows,” “cites,” or “purchases,” where the relationship is not symmetric.

### 2. Graph clustering

Graph clustering searches for communities or modules. A common objective is modularity:

\[
Q=\frac1{2m}\sum_{ij}
\left(A_{ij}-\frac{k_i k_j}{2m}\right)\delta(c_i,c_j),
\]

where \(A_{ij}\) is the adjacency value, \(k_i\) and \(k_j\) are degrees, \(m\) is the number of edges, and \(c_i,c_j\) are cluster labels. High modularity means much of the edge mass lies within communities relative to a degree-preserving random graph. Modularity has a resolution limit: a broad true community can be split into smaller high-modularity pieces, so parameter and scale must be considered.

Other objectives minimize cut edges, maximize conductance, or use correlation clustering with positive and negative relationships. The choice reflects whether a small dense group, a balanced community, or overlapping membership is desired.

### 3. Spectral and structural approaches

A graph Laplacian is \(L=D-A\), where \(D\) is the degree matrix and \(A\) is adjacency. Eigenvectors of \(L\) can provide a geometric representation; low-frequency eigenvectors change slowly across connected vertices, so discretizing them can produce communities. Spectral methods are mathematically useful but can be costly for a very large graph and sensitive to weighting.

**Label propagation** assigns a label to a vertex based on its neighbors' labels, updating randomly or asynchronously. It is fast but can depend on initialization and may collapse to one label. **Clique-based methods** search for highly connected complete subgraphs; cliques can overlap, so the selected cliques need reconciliation.

### 4. Frequent graph patterns

A frequent subgraph occurs in many labeled graphs or transactions. A **motif** is a small connected pattern that recurs more often than expected in a network. Mining is expensive because even small graph fragments have many possible adjacency patterns. Typical methods use anti-monotonicity: if a pattern is infrequent, no supergraph containing it can be frequent under a downward-closed count. Node and edge labels, support thresholds, and isomorphism determine what “same pattern” means.

### 5. Link and path analysis

Similarity of vertices can be based on common neighbors (Jaccard or Adamic–Adar), random-walk closeness, shortest paths, or personalized PageRank. A link-prediction method scores a possible edge from node features and graph structure. It is used for recommendations and network completion, but missing links may be false or unavailable; evaluation must be time-aware and avoid using future edges.

### 6. Graph construction and quality

A graph is a model of a relationship, not a neutral container. Edges need a definition: common login, co-purchase, similarity, or physical contact. A threshold changes the network and can create communities. Direction, weights, missing ties, and privacy must be documented. A graph-based cluster is meaningful only if the edge definition matches the question.

### 7. Advantages and limitations

Graphs capture relationships that ordinary feature vectors miss and can reveal communities without labels. However, graph construction may be expensive, dense graphs have few clear communities, sparse graphs have unstable degrees, overlapping communities are hard for hard partitions, and modularity or clique results depend on resolution. Transitivity is not causation: friends of friends need not be direct friends, and network association cannot establish a causal claim.

## Worked examples

### Example 1: Components and degree

Graph edges are A–B, B–C, C–D, and E–F. There are two connected components: `{A,B,C,D}` and `{E,F}`. Degrees are A=1, B=2, C=2, D=1, E=1, F=1. A graph clustering that cuts the B–C edge produces two dense groups, but whether that is useful depends on the application.

### Example 2: Modularity intuition

A group has 20 of its 25 edges inside and only a few edges to the rest of the graph. Its degree mass is much larger than expected under a random degree-preserving model, so the edge density is evidence for a community. A group with 100 of 105 edges inside can still be less useful than a smaller, more balanced community because of the resolution limit.

### Example 3: Common-neighbor similarity

Two candidate users A and B share 3 friends out of 5 A-friends and 4 B-friends. Jaccard similarity is

\[
3/|F_A\cup F_B|=3/(5+4-3)=3/6=0.5.
\]

This is a heuristic similarity, not proof that the users should be in the same community.

### Example 4: Antimonotonic graph mining

If pattern P is an infrequent subgraph, any supergraph Q containing P cannot be frequent in a database where every occurrence of Q would also contain P. This allows pruning in graph-pattern search, just as Apriori prunes itemset candidates. Edge-label and node-label support can alter the argument, so the task definition must be explicit.

## Key terms & formulas

- **Graph:** \(G=(V,E)\).
- **Vertex/node:** object; **edge:** relationship.
- **Degree:** number of incident edges.
- **Connected component:** maximal connected subgraph.
- **Community:** dense within-group and sparse between-group structure.
- **Modularity:** edge/community objective relative to a null model.
- **Graph Laplacian:** \(L=D-A\).
- **Motif:** recurring small graph pattern.
- **Frequent subgraph:** pattern meeting support threshold.
- **Clique:** complete subgraph.
- **Link prediction:** score for a missing or future edge.
- **Anti-monotonicity:** infrequent pattern implies infrequent supergraphs.

## Common mistakes

1. **Treating an edge as proof of similarity or causation:** it is a modeled relation.
2. **Ignoring the edge-construction threshold:** changing it changes communities.
3. **Confusing connected components with meaningful clusters:** components are only connectivity, not modularity.
4. **Using modularity without checking resolution:** large communities can split.
5. **Applying directed-graph degree to an undirected graph:** distinguish in/out degree.
6. **Evaluating link prediction with future edges in training:** time leakage.

## Exam prep

**Likely 2-mark questions**
1. Define a graph and a graph cluster. *Hint: vertices/edges and a community with internal density.*
2. What is graph modularity? *Hint: objective comparing within-community edges with a degree-preserving null model.*
3. Give two graph mining tasks. *Hint: clustering, frequent subgraphs, motifs, paths, or link prediction.*

**Likely long-answer questions**
1. Explain graph construction and graph-clustering methods. *Hint: relation definition, adjacency, modularity, spectral, label propagation, resolution.*
2. Compare a graph cluster with a feature-space cluster. *Hint: pairwise relationships versus attribute geometry.*
3. Describe frequent subgraph mining and anti-monotonic pruning. *Hint: support, isomorphism, supergraph implication.*
