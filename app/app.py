import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from predict import load_data, get_trending, get_top_categories

st.set_page_config(
    page_title="NovaBuy AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #ffffff; }
section[data-testid="stSidebar"] { display: none !important; }
.stButton > button {
    background: #1e3a5f !important; color: white !important;
    border: none !important; border-radius: 6px !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important;
}
.stButton > button:hover { background: #162d4a !important; }
</style>
""", unsafe_allow_html=True)

# ── NAV ──────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6, c7 = st.columns([2,1,1,1,1,1,2])
with c1:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:8px;padding:14px 0;'>
        <div style='width:8px;height:8px;background:#1e3a5f;border-radius:50%;'></div>
        <span style='font-size:15px;font-weight:600;color:#111827;'>NovaBuy AI</span>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Home", key="nav_home"):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Search", key="nav_search"):
        st.switch_page("pages/1_Search.py")
    st.markdown("</div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("AI Assistant", key="nav_ai"):
        st.switch_page("pages/2_AI_Assistant.py")
    st.markdown("</div>", unsafe_allow_html=True)
with c5:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Compare", key="nav_compare"):
        st.switch_page("pages/3_Compare.py")
    st.markdown("</div>", unsafe_allow_html=True)
with c6:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Insights", key="nav_insights"):
        st.switch_page("pages/4_Insights.py")
    st.markdown("</div>", unsafe_allow_html=True)
with c7:
    st.markdown("""
    <div style='font-size:12px;color:#9ca3af;padding:18px 0;text-align:right;'>
        8,000 products · 248 categories</div>""",
    unsafe_allow_html=True)

st.markdown("<hr style='margin:0;border-color:#e5e7eb;'>",
            unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#0f1e33;padding:72px 40px;text-align:center;'>
    <div style='font-size:11px;font-weight:500;color:#60a5fa;
                text-transform:uppercase;letter-spacing:.1em;
                margin-bottom:14px;'>AI-Powered Product Discovery</div>
    <h1 style='font-size:38px;font-weight:600;color:#fff;
               line-height:1.25;margin:0 0 14px;'>
        Find exactly what you need<br>
        <span style='color:#60a5fa;'>using natural language</span>
    </h1>
    <p style='font-size:14px;color:#94a3b8;margin:0 auto 32px;
              max-width:500px;line-height:1.8;'>
        Semantic search powered by sentence embeddings,
        FAISS vector search, and Groq LLM.
    </p>
</div>
""", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 3, 1])
with mid:
    st.markdown("<div style='margin-top:-20px;'>", unsafe_allow_html=True)
    hero_q = st.text_input(
        "h", placeholder="🔍  Try: wireless headphones for gym under $50",
        label_visibility="collapsed"
    )
    if st.button("Search with AI →", type="primary"):
        if hero_q:
            st.session_state['home_query'] = hero_q
            st.switch_page("pages/1_Search.py")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#f8fafc;border-top:1px solid #e5e7eb;
            border-bottom:1px solid #e5e7eb;padding:20px 40px;
            display:flex;justify-content:center;gap:60px;'>
""" + "".join([
    f"<div style='text-align:center;'>"
    f"<div style='font-size:20px;font-weight:600;color:#1e3a5f;'>{v}</div>"
    f"<div style='font-size:11px;color:#9ca3af;margin-top:3px;'>{l}</div>"
    f"</div>"
    for v, l in [
        ("8,000+","Products"), ("248","Categories"),
        ("384-dim","Embeddings"), ("<1s","Query time"),
        ("3-stage","Reranking"), ("Groq LLM","AI Engine"),
    ]
]) + "</div>", unsafe_allow_html=True)

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:52px 40px;'>
    <div style='text-align:center;margin-bottom:36px;'>
        <div style='font-size:11px;font-weight:500;color:#1e3a5f;
                    text-transform:uppercase;letter-spacing:.1em;
                    margin-bottom:6px;'>How it works</div>
        <div style='font-size:22px;font-weight:600;color:#111827;'>
            3-stage recommendation pipeline</div>
    </div>
    <div style='display:grid;grid-template-columns:repeat(3,1fr);
                gap:20px;max-width:900px;margin:0 auto;'>
        <div style='background:#f8fafc;border:1px solid #e5e7eb;
                    border-radius:10px;padding:24px;'>
            <div style='font-size:24px;margin-bottom:12px;'>🔢</div>
            <div style='font-size:13px;font-weight:500;color:#111827;
                        margin-bottom:6px;'>Stage 1 · Semantic retrieval</div>
            <div style='font-size:12px;color:#6b7280;line-height:1.7;'>
                Query embedded into 384-dim vector using MiniLM-L6-v2.
                FAISS searches 8,000 products in milliseconds using
                cosine similarity.
            </div>
        </div>
        <div style='background:#f8fafc;border:1px solid #e5e7eb;
                    border-radius:10px;padding:24px;'>
            <div style='font-size:24px;margin-bottom:12px;'>🎯</div>
            <div style='font-size:13px;font-weight:500;color:#111827;
                        margin-bottom:6px;'>Stage 2 · Keyword reranking</div>
            <div style='font-size:12px;color:#6b7280;line-height:1.7;'>
                Candidates reranked combining semantic score (55%),
                keyword match (35%), and product quality signals
                like ratings (10%).
            </div>
        </div>
        <div style='background:#f8fafc;border:1px solid #e5e7eb;
                    border-radius:10px;padding:24px;'>
            <div style='font-size:24px;margin-bottom:12px;'>🤖</div>
            <div style='font-size:13px;font-weight:500;color:#111827;
                        margin-bottom:6px;'>Stage 3 · LLM explanation</div>
            <div style='font-size:12px;color:#6b7280;line-height:1.7;'>
                Groq LLM reads top results and generates a plain-English
                explanation of why each product matches your query.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TRENDING ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:0 40px 52px;'>
    <div style='margin-bottom:20px;'>
        <div style='font-size:11px;font-weight:500;color:#1e3a5f;
                    text-transform:uppercase;letter-spacing:.1em;
                    margin-bottom:4px;'>Trending now</div>
        <div style='font-size:18px;font-weight:600;color:#111827;'>
            Top rated products</div>
    </div>
""", unsafe_allow_html=True)

trending = get_trending(8)
cols = st.columns(4)
for i, (_, row) in enumerate(trending.iterrows()):
    with cols[i % 4]:
        st.markdown(f"""
        <div style='background:#fff;border:1px solid #e5e7eb;
                    border-radius:10px;padding:14px;margin-bottom:16px;'>
            <div style='background:#f8fafc;border-radius:6px;height:140px;
                        display:flex;align-items:center;justify-content:center;
                        margin-bottom:12px;overflow:hidden;'>
                <img src='{row["imgUrl"]}' style='max-height:130px;
                     max-width:100%;object-fit:contain;'
                     onerror="this.style.display='none'">
            </div>
            <div style='font-size:11px;color:#1e3a5f;margin-bottom:4px;'>
                {row["category_name"]}</div>
            <div style='font-size:13px;font-weight:500;color:#111827;
                        line-height:1.4;margin-bottom:10px;min-height:40px;'>
                {str(row["title"])[:65]}{"..." if len(str(row["title"]))>65 else ""}
            </div>
            <div style='display:flex;align-items:center;
                        justify-content:space-between;'>
                <div>
                    <span style='font-size:13px;font-weight:600;
                                 color:#1e3a5f;'>${row["price"]}</span>
                    <span style='font-size:11px;color:#9ca3af;
                                 margin-left:6px;'>⭐ {row["stars"]}</span>
                </div>
                <a href='{row["productURL"]}' target='_blank'
                   style='font-size:11px;color:#1e3a5f;text-decoration:none;
                          border:1px solid #1e3a5f;border-radius:4px;
                          padding:3px 8px;'>View ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── CATEGORIES ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#f8fafc;border-top:1px solid #e5e7eb;
            border-bottom:1px solid #e5e7eb;padding:48px 40px;'>
    <div style='text-align:center;margin-bottom:28px;'>
        <div style='font-size:11px;font-weight:500;color:#1e3a5f;
                    text-transform:uppercase;letter-spacing:.1em;
                    margin-bottom:6px;'>Browse by</div>
        <div style='font-size:22px;font-weight:600;color:#111827;'>
            Popular categories</div>
    </div>
""", unsafe_allow_html=True)

cat_icons = {
    'headphone':'🎧','laptop':'💻','phone':'📱','camera':'📷',
    'clothing':'👗','shoe':'👟','kitchen':'🍳','toy':'🧸',
    'book':'📚','sport':'⚽','beauty':'💄','home':'🏠',
    'computer':'🖥️','gaming':'🎮','fitness':'💪','jewelry':'💍',
    'pet':'🐾','garden':'🌿','electronic':'⚡','office':'📎',
}

def get_icon(name):
    n = name.lower()
    for k, v in cat_icons.items():
        if k in n:
            return v
    return '📦'

top_cats = get_top_categories(12)
cat_cols = st.columns(6)
for i, (_, row) in enumerate(top_cats.iterrows()):
    with cat_cols[i % 6]:
        st.markdown(f"""
        <div style='background:#fff;border:1px solid #e5e7eb;
                    border-radius:10px;padding:16px 12px;
                    text-align:center;margin-bottom:12px;'>
            <div style='font-size:28px;margin-bottom:8px;'>
                {get_icon(row["category_name"])}</div>
            <div style='font-size:11px;font-weight:500;color:#111827;
                        line-height:1.4;margin-bottom:4px;'>
                {row["category_name"][:22]}
                {"..." if len(row["category_name"])>22 else ""}
            </div>
            <div style='font-size:10px;color:#9ca3af;'>
                {row["count"]} products</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#0f1e33;padding:28px 40px;
            display:flex;align-items:center;justify-content:space-between;'>
    <div style='display:flex;align-items:center;gap:8px;'>
        <div style='width:6px;height:6px;background:#60a5fa;
                    border-radius:50%;'></div>
        <span style='font-size:13px;font-weight:500;color:#fff;'>
            NovaBuy AI</span>
    </div>
    <div style='font-size:11px;color:#475569;'>
        SentenceTransformers · FAISS · Groq LLM · Streamlit ·
        Techaxis Internship 2026
    </div>
    <div style='font-size:11px;color:#475569;'>Muskan Khadka</div>
</div>
""", unsafe_allow_html=True)