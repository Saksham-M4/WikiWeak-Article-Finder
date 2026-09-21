# 📚 WikiWeak Article Finder

### Data-Driven Detection of Relatively Low Content-Richness Wikipedia Articles

**WikiWeak Article Finder** is an experimental data-analysis application that identifies Wikipedia articles with relatively low measured content richness using a transparent, multi-factor scoring system.

Instead of relying on subjective judgments, WikiWeak analyzes measurable article characteristics such as **word count, section count, references, infobox fields, and images**, converts them into relative percentile scores, and combines them into a single experimental **Content-Richness Score**.

> **Important:** WikiWeak is **not an official Wikimedia or Wikipedia quality-rating system**. Its score is an experimental metric designed for comparative analysis within the analyzed dataset.

---

## 🚀 Project Overview

Wikipedia contains millions of articles covering subjects of vastly different sizes and levels of detail.

WikiWeak explores a simple analytical question:

> **Which articles contain relatively less measurable content compared with other articles in the analyzed sample?**

The application processes structured Wikipedia data and creates a reproducible pipeline:

```text
Wikimedia Structured Contents Dataset
                ↓
        Data Extraction
                ↓
       Feature Calculation
                ↓
      Percentile Normalization
                ↓
        Weighted Scoring
                ↓
          Ranking / Filtering
                ↓
       Interactive Dashboard
                ↓
       Article-Level Analysis
```

This allows users to move from **raw article data → measurable features → score → ranking → explanation**.

---

# 🎯 Key Objectives

WikiWeak is designed to:

* Identify relatively low-content articles in a sample.
* Quantify measurable article characteristics.
* Combine multiple content signals into one transparent score.
* Allow users to filter articles interactively.
* Explain why an article received its relative score.
* Provide direct links to the corresponding Wikipedia articles.
* Support data-driven exploration rather than subjective classification.

---

# 📊 Current Dataset

The current application analyzes:

| Metric                   |      Value |
| ------------------------ | ---------: |
| Articles analyzed        | **10,000** |
| Scoring factors          |      **5** |
| Limited-content articles |    **502** |
| Current score threshold  |  **11.76** |
| Lowest displayed example |   **9.42** |

The dataset is a **10,000-article sample from the Wikimedia Wikipedia Structured Contents dataset**.

The project uses this sample as its comparison population. Therefore, the score represents an article's relative position **within the analyzed sample**, rather than an absolute measure of Wikipedia quality.

---

# 🧮 Content-Richness Scoring Model

WikiWeak evaluates five measurable factors.

| Factor         |  Weight | What it measures          |
| -------------- | ------: | ------------------------- |
| Word Count     | **40%** | Amount of textual content |
| Section Count  | **20%** | Structural organization   |
| References     | **20%** | Number of references      |
| Infobox Fields | **10%** | Structured metadata       |
| Images         | **10%** | Number of article images  |

### Formula

Each factor is converted into a relative percentile within the analyzed sample.

The weighted score is then calculated as:

```text
Content-Richness Score =
    (Word Count Percentile × 0.40)
  + (Section Count Percentile × 0.20)
  + (References Percentile × 0.20)
  + (Infobox Fields Percentile × 0.10)
  + (Images Percentile × 0.10)
```

The resulting weighted value is converted to a **0–100 scale**.

```text
Final Score = Weighted Score × 100
```

### Why percentile-based scoring?

Raw values can vary dramatically between Wikipedia articles.

For example:

```text
Article A → 100 words
Article B → 1,000 words
Article C → 10,000 words
```

Rather than treating these values in isolation, WikiWeak evaluates where an article falls **relative to the analyzed sample**.

This makes the five different measurements comparable before combining them.

---

# 🔍 Example Article Analysis

The dashboard can inspect individual articles.

### Tarao Naga

**Experimental Content-Richness Score: 9.42 / 100**

| Feature        | Measured Value |
| -------------- | -------------: |
| Word Count     |             95 |
| Sections       |              1 |
| Infobox Fields |              0 |
| Images         |              0 |
| References     |              0 |
| Final Score    |       **9.42** |

The application identifies the article's relatively lowest-performing measured factors and explains how they contribute to the overall score.

For this example, the three lowest relative factors are:

1. **Word count**
2. **References**
3. **Sections**

This does **not** mean the article is inaccurate, unimportant, or necessarily poor quality.

It means that, according to the project's selected measurable features, it contains relatively little measured content compared with the analyzed sample.

---

# 🖥️ Interactive Dashboard

The dashboard provides several ways to explore the dataset.

### 🔎 Article Search

Users can search the analyzed articles and inspect individual results.

### 🎚️ Score Filter

A maximum-score filter allows users to focus on articles below a selected content-richness threshold.

### 📋 Article Results

Filtered articles are presented as an interactive result set.

### 📈 Score Distribution

A distribution chart shows how the analyzed articles are spread across different score ranges.

### 📉 Lowest-Scoring Articles

The dashboard highlights articles with comparatively low experimental scores.

### 🔍 Article Score Breakdown

Selecting an article provides:

* Article name
* Wikipedia link
* Overall score
* Word count
* Section count
* Infobox fields
* Image count
* Reference count
* Lowest relative factors
* Explanation of the scoring methodology

---

# 🧠 Explainability

A major design principle of WikiWeak is **transparent scoring**.

The application does not simply output:

```text
Score = 9.42
```

It also explains the underlying measurements.

The analysis follows:

```text
Article
   ↓
Five measurable features
   ↓
Percentile position
   ↓
Weighted contribution
   ↓
Final score
   ↓
Human-readable explanation
```

This makes the result easier to inspect and reproduce.

---

# ⚙️ Technical Architecture

```text
                 ┌──────────────────────────┐
                 │ Wikimedia Structured     │
                 │ Contents Dataset         │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Data Processing          │
                 │ & Feature Extraction     │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Feature Engineering      │
                 │                          │
                 │ • Word Count             │
                 │ • Sections               │
                 │ • References             │
                 │ • Infobox Fields         │
                 │ • Images                 │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Percentile Normalization │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Weighted Score Engine    │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Ranking & Filtering      │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Interactive Dashboard    │
                 └──────────────────────────┘
```

---

# 🧩 Feature Engineering

WikiWeak extracts five measurable article characteristics.

### 1. Word Count

Measures the amount of textual content available in the analyzed article representation.

**Weight: 40%**

Because textual content represents a substantial portion of an article, it receives the highest weighting.

### 2. Section Count

Measures the structural organization of article content.

**Weight: 20%**

### 3. References

Measures the number of references represented in the analyzed data.

**Weight: 20%**

References provide a measurable indication of how extensively an article's content is accompanied by cited sources.

### 4. Infobox Fields

Measures the amount of structured information represented in the article's infobox.

**Weight: 10%**

### 5. Images

Measures the number of images represented in the analyzed article data.

**Weight: 10%**

---

# 📐 Why Use Multiple Factors?

A single metric can be misleading.

For example:

```text
Low word count ≠ automatically low content richness
```

An article could be short but contain useful structured information.

Similarly:

```text
Many images ≠ automatically high-quality article
```

Therefore, WikiWeak combines five measurable characteristics instead of relying on one signal.

This creates a broader **content-richness indicator**.

---

# 🏆 Ranking Philosophy

WikiWeak does not attempt to determine whether an article is:

* Good or bad
* Important or unimportant
* Accurate or inaccurate
* Notable or non-notable
* Complete or incomplete

Instead, it answers a narrower analytical question:

> **How does this article compare with the analyzed sample across the selected measurable content features?**

This distinction is fundamental to the project.

---

# ⚠️ Limitations

WikiWeak's score should be interpreted carefully.

### Sample Dependency

Percentiles depend on the analyzed population.

Changing the dataset can change an article's percentile and therefore its final score.

### Feature Dependency

The system measures only five selected characteristics:

* Word count
* Sections
* References
* Infobox fields
* Images

Other important characteristics are not directly represented.

### Quality ≠ Quantity

A larger article is not automatically a better article.

Likewise, a shorter article is not automatically deficient.

### Domain Differences

Different subjects naturally require different amounts of content.

A short article about one topic may be entirely appropriate, while another subject may require substantially more detail.

### Experimental Metric

The Content-Richness Score is a project-defined analytical metric and should not be interpreted as an official Wikimedia quality assessment.

---

# 🔬 Possible Future Improvements

WikiWeak can be extended beyond its current five-factor model.

Potential future directions include:

### Semantic Analysis

Use NLP to examine:

* Topic coverage
* Semantic completeness
* Repeated content
* Missing contextual information

### Citation Analysis

Extend reference analysis to examine:

* Citation density
* Citation placement
* Source diversity
* Citation-to-content ratios

### Temporal Analysis

Track how article content changes over time:

```text
Article
   ↓
Historical snapshots
   ↓
Feature extraction
   ↓
Score over time
   ↓
Content-growth visualization
```

### Topic-Aware Comparison

Compare articles against similar articles rather than only the complete sample.

For example:

```text
Historical articles → historical peers
Scientific articles → scientific peers
Geographical articles → geographical peers
```

This could reduce distortions caused by comparing fundamentally different article types.

### Larger Datasets

The current implementation uses a 10,000-article sample.

Future versions could process substantially larger datasets for broader analysis.

---

# 💡 Potential Applications

The underlying methodology could support research and exploratory analysis in areas such as:

* Wikipedia content analysis
* Open-knowledge research
* Data journalism
* Educational data projects
* Knowledge-gap exploration
* Article improvement workflows
* NLP and information-retrieval research
* Wikimedia ecosystem analysis

The output should be treated as a **discovery and analysis aid**, not as an automated replacement for human editorial judgment.

---

# 🛠️ Technology Stack

The application is designed around a data-processing and interactive-dashboard workflow.

Core components include:

* **Wikimedia Structured Contents data**
* **Data processing / feature extraction**
* **Percentile-based statistical normalization**
* **Weighted scoring**
* **Interactive visualization**
* **Article-level inspection**
* **Wikipedia article linking**

The deployed dashboard is powered by **Streamlit**.

---

# 📌 Project Workflow

```text
DATA
  │
  ▼
Extract article metadata
  │
  ▼
Calculate five measurable features
  │
  ▼
Normalize features using percentiles
  │
  ▼
Apply scoring weights
  │
  ▼
Generate 0–100 experimental score
  │
  ▼
Rank and filter articles
  │
  ▼
Visualize results
  │
  ▼
Inspect individual articles
```

---

# 📊 Dashboard Philosophy

WikiWeak follows a simple principle:

> **Data → Features → Score → Rank → Inspect**

Every result should be traceable back to measurable article characteristics.

The dashboard therefore combines:

* **Data transparency**
* **Quantitative scoring**
* **Interactive exploration**
* **Explainability**
* **Human interpretation**

---

# 🌐 Wikipedia

Each analyzed result can be opened directly on Wikipedia for further human inspection.

The dashboard should be treated as a starting point for investigation rather than the final authority on an article.

---

# 📜 Responsible Interpretation

A low WikiWeak score should **never** be interpreted as proof that an article needs improvement.

It only indicates that the article has relatively low values across the selected measurable features within the analyzed sample.

Human reviewers should consider:

* Article topic
* Subject complexity
* Existing reliable sources
* Historical context
* Notability
* Editorial guidelines
* Accuracy
* Completeness
* Appropriate article length

before drawing conclusions about an article.

---

# 🔮 Vision

WikiWeak aims to demonstrate how structured open-knowledge data can be transformed into an **interpretable analytical system**.

The long-term idea is not simply to find short Wikipedia articles.

It is to build tools that help researchers and contributors discover **where measurable knowledge-content gaps may exist**, understand the signals behind those gaps, and investigate them using reliable human judgment.

```text
Open Data
    ↓
Data Engineering
    ↓
Feature Engineering
    ↓
Statistical Analysis
    ↓
Explainable Scoring
    ↓
Interactive Exploration
    ↓
Human Knowledge Improvement
```

---

## ⭐ Final Note

**WikiWeak Article Finder is an experimental research-oriented project.**

Its Content-Richness Score is a **relative, data-driven indicator**, not an official Wikipedia or Wikimedia quality score.

The project's primary contribution is the methodology:

> **Transform structured Wikipedia data into measurable features, normalize them statistically, combine them transparently, and make the resulting analysis explorable through an interactive dashboard.**

---

### WikiWeak Article Finder

**Data → Features → Score → Rank → Inspect**

*An experimental approach to discovering relatively low content-richness articles through measurable open-knowledge data.*
