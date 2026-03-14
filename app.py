import streamlit as st
import pandas as pd
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeScan · Similarity Engine",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;600;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #09090f;
    color: #e8e8f0;
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #1a1040 0%, #09090f 50%),
                radial-gradient(ellipse at 80% 100%, #001a2c 0%, transparent 60%);
    background-attachment: fixed;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1300px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0e1c 0%, #0a0a14 100%);
    border-right: 1px solid #1e1e3a;
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* ── Header ── */
.hero-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e1e3a;
}
.hero-icon {
    font-size: 2.8rem;
    line-height: 1;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 60%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #4a4a6a;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── Code editor panels ── */
.editor-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6060a0;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.editor-label::before {
    content: '';
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
}
.label-1::before { background: #a78bfa; box-shadow: 0 0 8px #a78bfa88; }
.label-2::before { background: #38bdf8; box-shadow: 0 0 8px #38bdf888; }

textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    background: #0d0d1a !important;
    border: 1px solid #1e1e3a !important;
    border-radius: 10px !important;
    color: #c8c8e8 !important;
    caret-color: #a78bfa !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px #a78bfa22 !important;
}

/* ── Divider ── */
hr { border-color: #1e1e3a; margin: 2rem 0; }

/* ── Analyze button ── */
.stButton > button {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.08em;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2.5rem;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 24px #7c3aed44;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px #7c3aed66;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6);
}
.stButton > button:active { transform: translateY(0); }

/* ── Score cards ── */
.score-card {
    background: linear-gradient(135deg, #0f0f22, #12122a);
    border: 1px solid #1e1e3a;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.score-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent 60%, #7c3aed0a);
    pointer-events: none;
}
.score-card:hover { border-color: #3a3a5a; }
.card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4a4a6a;
    margin-bottom: 0.6rem;
}
.card-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.card-value.purple { color: #a78bfa; }
.card-value.blue   { color: #38bdf8; }
.card-value.green  { color: #34d399; }
.card-value.orange { color: #fb923c; }
.card-value.red    { color: #f87171; }

/* ── Verdict banner ── */
.verdict-high {
    background: linear-gradient(135deg, #052e16, #064e3b);
    border: 1px solid #059669;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #34d399;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
}
.verdict-mid {
    background: linear-gradient(135deg, #1c1003, #292107);
    border: 1px solid #d97706;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #fbbf24;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
}
.verdict-low {
    background: linear-gradient(135deg, #1c0505, #2a0a0a);
    border: 1px solid #dc2626;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #f87171;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
}

/* ── Section headers ── */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #5050a0;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e1e3a, transparent);
}

/* ── Progress bar override ── */
.stProgress > div > div {
    border-radius: 999px;
    background: linear-gradient(90deg, #7c3aed, #38bdf8, #34d399) !important;
}
.stProgress > div {
    background: #1e1e3a !important;
    border-radius: 999px;
    height: 8px !important;
}

/* ── Metric widget ── */
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    color: #a78bfa;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: #5050a0;
    text-transform: uppercase;
}

/* ── Dataframe ── */
.dataframe-container [data-testid="stDataFrame"] {
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    overflow: hidden;
}

/* ── Sidebar content ── */
.sidebar-badge {
    background: #12122a;
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #8080c0;
}
.sidebar-badge strong { color: #a78bfa; display: block; margin-bottom: 0.25rem; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; }

/* ── Warning / error overrides ── */
[data-testid="stAlert"] {
    border-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
}

/* ── Bar chart ── */
.vega-embed { border-radius: 10px; }

/* ── Spinner ── */
.stSpinner { color: #a78bfa !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:2rem;">
        <div style="font-size:2.5rem; margin-bottom:.5rem;">⬡</div>
        <div style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.1rem; 
                    background:linear-gradient(135deg,#a78bfa,#38bdf8);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            CodeScan
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#4a4a6a; 
                    letter-spacing:.15em; text-transform:uppercase; margin-top:.25rem;">
            Similarity Engine v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Engine Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-badge"><strong>Vectorizer</strong>TF-IDF (Term Frequency–Inverse Document Frequency)</div>
    <div class="sidebar-badge"><strong>Distance Metric</strong>Cosine Similarity · Range [0, 1]</div>
    <div class="sidebar-badge"><strong>Interface</strong>Streamlit · Python 3.x</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Thresholds</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-badge">
        <strong>High Similarity</strong>
        <span style="color:#34d399">▶ score &gt; 0.70</span>
    </div>
    <div class="sidebar-badge">
        <strong>Moderate Similarity</strong>
        <span style="color:#fbbf24">▶ 0.40 – 0.70</span>
    </div>
    <div class="sidebar-badge">
        <strong>Low Similarity</strong>
        <span style="color:#f87171">▶ score &lt; 0.40</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#4a4a6a; line-height:1.8;">
    Paste two code snippets and run analysis to measure structural & lexical overlap using cosine similarity on TF-IDF vectors.
    </div>
    """, unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-icon">⬡</div>
    <div>
        <div class="hero-title">Code Similarity Engine</div>
        <div class="hero-sub">TF-IDF · Cosine Similarity · Real-time Analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input columns ──────────────────────────────────────────────────────────────
col1, gap, col2 = st.columns([5, 0.3, 5])

with col1:
    st.markdown('<div class="editor-label label-1">Snippet α — Primary</div>', unsafe_allow_html=True)
    code1 = st.text_area(
        label="code1",
        placeholder="# Paste your first code snippet here...\ndef hello_world():\n    print('Hello, World!')",
        height=280,
        label_visibility="collapsed",
        key="snippet_a",
    )

with gap:
    st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; height:280px; 
                font-size:1.4rem; color:#2a2a4a; margin-top:1.6rem;">⇄</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="editor-label label-2">Snippet β — Compare</div>', unsafe_allow_html=True)
    code2 = st.text_area(
        label="code2",
        placeholder="# Paste your second code snippet here...\ndef greet():\n    print('Hello, World!')",
        height=280,
        label_visibility="collapsed",
        key="snippet_b",
    )

st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

btn_col, _, info_col = st.columns([3, 0.5, 6.5])
with btn_col:
    analyze = st.button("⬡  Run Similarity Analysis", use_container_width=True)
with info_col:
    if not (code1 and code2):
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#3a3a5a; 
                    padding:.75rem 0; display:flex; align-items:center; gap:.5rem;">
            <span style="color:#2a2a4a">●</span> Enter both snippets above to enable analysis
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ── Results ────────────────────────────────────────────────────────────────────
if analyze:
    if code1 and code2:
        with st.spinner("Computing similarity vectors..."):
            time.sleep(0.4)  # brief UX pause
            try:
                from src.similarity import compute_similarity
                score = compute_similarity(code1, code2)
            except ImportError:
                # Demo fallback when src.similarity not available
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.metrics.pairwise import cosine_similarity as cos_sim
                vec = TfidfVectorizer()
                tfidf = vec.fit_transform([code1, code2])
                score = float(cos_sim(tfidf[0], tfidf[1])[0][0])

        percentage = round(score * 100, 2)
        diff       = round(100 - percentage, 2)

        # ── Verdict ──────────────────────────────────────────────────────────
        st.markdown('<div class="section-header">Verdict</div>', unsafe_allow_html=True)
        if score > 0.7:
            st.markdown(f"""
            <div class="verdict-high">
                ✓ HIGHLY SIMILAR &nbsp;·&nbsp; {percentage}% overlap detected — these snippets share significant structural and lexical patterns.
            </div>""", unsafe_allow_html=True)
        elif score > 0.4:
            st.markdown(f"""
            <div class="verdict-mid">
                ⚠ MODERATELY SIMILAR &nbsp;·&nbsp; {percentage}% overlap — partial commonality found. May share logic patterns.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="verdict-low">
                ✕ LOW SIMILARITY &nbsp;·&nbsp; {percentage}% overlap — snippets appear structurally distinct.
            </div>""", unsafe_allow_html=True)

        # ── Score cards ───────────────────────────────────────────────────────
        st.markdown('<div class="section-header">Metrics</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        val_color = "green" if score > 0.7 else ("orange" if score > 0.4 else "red")

        with c1:
            st.markdown(f"""
            <div class="score-card">
                <div class="card-label">Cosine Score</div>
                <div class="card-value purple">{score:.4f}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="score-card">
                <div class="card-label">Similarity %</div>
                <div class="card-value blue">{percentage}%</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="score-card">
                <div class="card-label">Difference %</div>
                <div class="card-value {val_color}">{diff}%</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            tokens_a = len(code1.split())
            tokens_b = len(code2.split())
            st.markdown(f"""
            <div class="score-card">
                <div class="card-label">Token Δ</div>
                <div class="card-value purple">{abs(tokens_a - tokens_b)}</div>
            </div>""", unsafe_allow_html=True)

        # ── Progress bar ─────────────────────────────────────────────────────
        st.markdown('<div class="section-header">Similarity Meter</div>', unsafe_allow_html=True)
        col_prog, _ = st.columns([8, 2])
        with col_prog:
            st.progress(score)
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#4a4a6a; 
                        text-align:right; margin-top:.3rem;">
                {percentage}% match
            </div>""", unsafe_allow_html=True)

        # ── Chart + Table ─────────────────────────────────────────────────────
        st.markdown('<div class="section-header">Breakdown</div>', unsafe_allow_html=True)
        chart_col, table_col = st.columns([6, 4])

        data = pd.DataFrame({
            "Category": ["Similar", "Different"],
            "Value":    [percentage, diff],
        })

        with chart_col:
            st.bar_chart(
                data.set_index("Category"),
                color="#7c3aed",
                use_container_width=True,
                height=260,
            )

        with table_col:
            detail = pd.DataFrame({
                "Metric": [
                    "Cosine Score",
                    "Similarity %",
                    "Difference %",
                    "Tokens · Snippet α",
                    "Tokens · Snippet β",
                    "Token Delta",
                    "Verdict",
                ],
                "Value": [
                    f"{score:.6f}",
                    f"{percentage}%",
                    f"{diff}%",
                    str(tokens_a),
                    str(tokens_b),
                    str(abs(tokens_a - tokens_b)),
                    "High" if score > 0.7 else ("Moderate" if score > 0.4 else "Low"),
                ],
            })
            st.dataframe(detail, use_container_width=True, hide_index=True, height=280)

    else:
        st.markdown("""
        <div style="background:#0f0f22; border:1px dashed #2a2a4a; border-radius:12px; 
                    padding:2rem; text-align:center; font-family:'JetBrains Mono',monospace; 
                    font-size:0.82rem; color:#3a3a6a;">
            ⚠ &nbsp; Both snippets are required to run the analysis.
        </div>""", unsafe_allow_html=True)