import streamlit as st
import pandas as pd

def count_words(text):
    """Return a simple whitespace-delimited word count."""
    if not isinstance(text, str):
        return 0
    return len(text.split())



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="WikiWeak Article Finder",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("wikiweak_results.csv")

    numeric_columns = [
        "rank",
        "content_richness_score",
        "article_length",
        "section_count",
        "infobox_field_count",
        "image_count",
        "reference_count"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "wikiweak_results.csv was not found. "
        "Place it in the same folder as app.py."
    )
    st.stop()


# ============================================================
# PROJECT CONSTANTS
# ============================================================

TOTAL_ARTICLES = len(df)

limited_df = df[df["limited_content"] == True].copy()

LIMITED_ARTICLES = len(limited_df)

SCORE_THRESHOLD = (
    limited_df["content_richness_score"].max()
    if len(limited_df) > 0
    else df["content_richness_score"].quantile(0.05)
)

# Percentile ranks are the same type of relative normalization used
# when the submitted content-richness score was created.
FACTOR_COLUMNS = {
    "Word Count": "article_length",
    "Section Count": "section_count",
    "Infobox Fields": "infobox_field_count",
    "Images": "image_count",
    "References": "reference_count",
}

FACTOR_WEIGHTS = {
    "Word Count": 0.40,
    "Section Count": 0.20,
    "Infobox Fields": 0.10,
    "Images": 0.10,
    "References": 0.20,
}

FACTOR_LABELS = {
    "Word Count": "Word count (words)",
    "Section Count": "Sections",
    "Infobox Fields": "Infobox fields",
    "Images": "Images",
    "References": "References",
}

def score_evidence(article_row):
    """Return the factor values, relative percentiles, weights and contributions
    for one article. This explains the experimental score; it does not
    judge the correctness or quality of the article's information.
    """
    rows = []
    for factor, column in FACTOR_COLUMNS.items():
        values = pd.to_numeric(df[column], errors="coerce")
        value = float(article_row[column])
        # pandas rank(pct=True) is equivalent to the percentile-rank method
        # used in the analysis notebook for the submitted sample.
        percentile = float(values.rank(pct=True).loc[article_row.name])
        weight = FACTOR_WEIGHTS[factor]
        rows.append({
            "Factor": FACTOR_LABELS[factor],
            "Actual value": int(value),
            "Relative percentile": percentile * 100,
            "Weight": f"{weight * 100:.0f}%",
            "Weighted contribution": percentile * weight * 100,
        })
    return pd.DataFrame(rows)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 650;
        margin-top: 20px;
    }

    .info-box {
        padding: 18px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Dashboard")

    st.write("Use the controls below to explore the analyzed articles.")

    st.divider()

    # Search
    search_text = st.text_input(
        "🔎 Search article",
        placeholder="Type an article name..."
    )

    # Score filter
    st.subheader("Score Filter")

    selected_score = st.slider(
        "Maximum content-richness score",
        min_value=0.0,
        max_value=100.0,
        value=float(round(SCORE_THRESHOLD, 2)),
        step=0.1
    )

    st.divider()

    st.subheader("🧮 Scoring Weights")

    st.write("Word Count — **40%**")
    st.write("Section Count — **20%**")
    st.write("References — **20%**")
    st.write("Infobox Fields — **10%**")
    st.write("Images — **10%**")

    st.divider()

    st.caption(
        "Experimental project score. "
        "Not an official Wikimedia quality rating."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📚 WikiWeak Article Finder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "A data-driven approach to identifying Wikipedia articles "
    "with relatively low content-richness scores."
    "</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">

    <b>Project Overview</b><br><br>

    WikiWeak analyzes measurable article-content factors from
    Wikimedia's Wikipedia Structured Contents dataset.

    The system extracts word count, sections, infobox fields,
    images and references, then combines their percentile ranks
    into an experimental content-richness score.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KEY METRICS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Dataset Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Articles Analyzed",
        f"{TOTAL_ARTICLES:,}"
    )

with c2:
    st.metric(
        "Limited-Content Articles",
        f"{LIMITED_ARTICLES:,}"
    )

with c3:
    st.metric(
        "Score Threshold",
        f"{SCORE_THRESHOLD:.2f}"
    )

with c4:
    st.metric(
        "Scoring Factors",
        "5"
    )


st.divider()


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["content_richness_score"] <= selected_score
].copy()

if search_text.strip():

    filtered_df = filtered_df[
        filtered_df["name"]
        .astype(str)
        .str.contains(
            search_text.strip(),
            case=False,
            na=False
        )
    ]


# ============================================================
# ARTICLE RESULTS
# ============================================================

st.markdown(
    '<div class="section-title">📋 Article Results</div>',
    unsafe_allow_html=True
)

st.caption(
    f"{len(filtered_df):,} articles match the current filters."
)

# Show only the first 20 for a clean interface
display_df = (
    filtered_df
    .sort_values("content_richness_score")
    .head(20)
    .copy()
)

display_columns = [
    "rank",
    "name",
    "content_richness_score",
    "article_length",
    "section_count",
    "infobox_field_count",
    "image_count",
    "reference_count"
]

st.dataframe(
    display_df[display_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "rank": st.column_config.NumberColumn(
            "Rank",
            format="%d"
        ),
        "name": st.column_config.TextColumn(
            "Article"
        ),
        "content_richness_score": st.column_config.NumberColumn(
            "Score",
            format="%.2f"
        ),
        "article_length": st.column_config.NumberColumn(
            "Length (words)",
            format="%d"
        ),
        "section_count": st.column_config.NumberColumn(
            "Sections",
            format="%d"
        ),
        "infobox_field_count": st.column_config.NumberColumn(
            "Infobox Fields",
            format="%d"
        ),
        "image_count": st.column_config.NumberColumn(
            "Images",
            format="%d"
        ),
        "reference_count": st.column_config.NumberColumn(
            "References",
            format="%d"
        )
    }
)


# ============================================================
# SCORE DISTRIBUTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Score Distribution</div>',
    unsafe_allow_html=True
)

bins = [
    0, 10, 20, 30, 40,
    50, 60, 70, 80, 90, 100
]

groups = pd.cut(
    df["content_richness_score"],
    bins=bins,
    include_lowest=True
)

distribution = (
    groups
    .value_counts()
    .sort_index()
)

distribution_df = pd.DataFrame(
    {
        "Score Range": distribution.index.astype(str),
        "Articles": distribution.values
    }
)

st.bar_chart(
    distribution_df.set_index("Score Range")
)


# ============================================================
# LOWEST SCORES
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    "📉 Lowest Content-Richness Scores"
    "</div>",
    unsafe_allow_html=True
)

lowest_15 = (
    df
    .sort_values("content_richness_score")
    .head(15)
)

chart_df = lowest_15[
    ["name", "content_richness_score"]
].set_index("name")

st.bar_chart(chart_df)


# ============================================================
# ARTICLE INSPECTOR
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    "🔍 Article Score Breakdown"
    "</div>",
    unsafe_allow_html=True
)

if len(filtered_df) > 0:

    article_list = (
        filtered_df
        .sort_values("content_richness_score")["name"]
        .astype(str)
        .tolist()
    )

    selected_article = st.selectbox(
        "Select an article to inspect",
        article_list
    )

    article = filtered_df[
        filtered_df["name"].astype(str)
        == selected_article
    ].iloc[0]

    st.markdown(f"### 📄 {article['name']}")

    if pd.notna(article["url"]):

        st.markdown(
            f"[🔗 Open Wikipedia article]({article['url']})"
        )

    st.write("")

    score = float(article["content_richness_score"])

    if score <= SCORE_THRESHOLD:

        st.warning(
            f"Relatively low content-richness score: "
            f"**{score:.2f}/100**"
        )

    else:

        st.success(
            f"Content-richness score: "
            f"**{score:.2f}/100**"
        )

    a, b, c = st.columns(3)

    with a:

        st.metric(
            "Word Count",
            f"{int(article['article_length']):,}"
        )

        st.metric(
            "Sections",
            int(article["section_count"])
        )

    with b:

        st.metric(
            "Infobox Fields",
            int(article["infobox_field_count"])
        )

        st.metric(
            "Images",
            int(article["image_count"])
        )

    with c:

        st.metric(
            "References",
            int(article["reference_count"])
        )

        st.metric(
            "Final Score",
            f"{score:.2f}"
        )

    # --------------------------------------------------------
    # WHY THIS SCORE?
    # --------------------------------------------------------
    st.markdown("### 🔎 Why is this article relatively limited-content?")

    evidence = score_evidence(article)

    low_factors = evidence.sort_values(
        "Relative percentile"
    ).head(3)

    if score <= SCORE_THRESHOLD:
        st.write(
            "This article falls within the lowest-scoring group of the "
            "analyzed sample. The result is based on the combined behavior "
            "of five content factors — not on any single factor alone."
        )
    else:
        st.write(
            "This article is not in the lowest-scoring group. The table below "
            "shows how its five content factors contribute to the experimental "
            "content-richness score."
        )

    st.dataframe(
        evidence,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Relative percentile": st.column_config.NumberColumn(
                "Relative percentile",
                format="%.1f"
            ),
            "Weighted contribution": st.column_config.NumberColumn(
                "Weighted contribution",
                format="%.2f"
            )
        }
    )

    st.caption(
        "A lower relative percentile means the article has less of that "
        "measured factor than more articles in this analyzed sample. "
        "The factors are combined using the displayed weights."
    )

    if score <= SCORE_THRESHOLD:
        factor_text = ", ".join(
            low_factors["Factor"].tolist()
        )
        st.info(
            f"The three lowest relative factors for this article are: "
            f"**{factor_text}**. These factors contribute less to the "
            f"overall score relative to the analyzed sample. This is an "
            f"experimental content-richness indicator, not an official "
            f"Wikimedia quality judgment."
        )

else:

    st.warning(
        "No articles match the current filters."
    )


# ============================================================
# SCORING METHOD
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    "🧮 How the Score Is Calculated"
    "</div>",
    unsafe_allow_html=True
)

st.write(
    "Each of the five measurable content factors is converted into a "
    "relative percentile within the analyzed sample. The five weighted "
    "percentiles are then combined into one experimental content-richness "
    "score. This means an article is not identified from word count, "
    "images, or any other single factor alone."
)

st.code(
    """
Content-Richness Score =
    (Word Count Percentile × 0.40)
  + (Section Count Percentile × 0.20)
  + (Infobox Fields Percentile × 0.10)
  + (Images Percentile × 0.10)
  + (References Percentile × 0.20)

Final Score = Weighted Score × 100
""",
    language="text"
)


# ============================================================
# FACTOR TABLE
# ============================================================

st.markdown(
    '<div class="section-title">'
    "📌 Factors Used for Scoring"
    "</div>",
    unsafe_allow_html=True
)

factor_df = pd.DataFrame(
    {
        "Factor": [
            "Word Count",
            "Section Count",
            "Infobox Fields",
            "Images",
            "References"
        ],
        "Weight": [
            "40%",
            "20%",
            "10%",
            "10%",
            "20%"
        ],
        "Purpose": [
            "Measures word count in words; it is one factor among five.",
            "Measures article structure.",
            "Measures structured information.",
            "Measures available visual content.",
            "Measures available references."
        ]
    }
)

st.dataframe(
    factor_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    "📥 Export Results"
    "</div>",
    unsafe_allow_html=True
)

download_csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Results",
    data=download_csv,
    file_name="wikiweak_filtered_results.csv",
    mime="text/csv"
)


# ============================================================
# FINAL NOTE
# ============================================================

st.divider()

st.info(
    """
    **Important:** The content-richness score is an experimental
    relative measure created for this project. It is based on
    percentile ranks within the analyzed sample and is not an
    official Wikimedia quality rating.

    The analyzed data consists of a 10,000-article sample from
    the Wikimedia Wikipedia Structured Contents dataset.
    """
)

st.caption(
    "WikiWeak Article Finder • Data → Features → Score → Rank → Inspect"
)