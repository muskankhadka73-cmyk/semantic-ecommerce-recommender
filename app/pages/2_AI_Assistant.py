import streamlit as st
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predict import semantic_search, has_strong_matches, generate_llm_response

st.set_page_config(page_title="AI Assistant — NovaBuy AI", page_icon="🤖",
    layout="wide", initial_sidebar_state="collapsed")

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

# NAV
n1,n2,n3,n4,n5,n6,n7 = st.columns([2,1,1,1,1,1,2])
with n1: st.markdown("<div style='display:flex;align-items:center;gap:8px;padding:14px 0;'><div style='width:8px;height:8px;background:#1e3a5f;border-radius:50%;'></div><span style='font-size:15px;font-weight:600;color:#111827;'>NovaBuy AI</span></div>", unsafe_allow_html=True)
with n2:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Home", key="n_home"): st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
with n3:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Search", key="n_search"): st.switch_page("pages/1_Search.py")
    st.markdown("</div>", unsafe_allow_html=True)
with n4:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("AI Assistant", key="n_ai"): st.switch_page("pages/2_AI_Assistant.py")
    st.markdown("</div>", unsafe_allow_html=True)
with n5:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Compare", key="n_compare"): st.switch_page("pages/3_Compare.py")
    st.markdown("</div>", unsafe_allow_html=True)
with n6:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    if st.button("Insights", key="n_insights"): st.switch_page("pages/4_Insights.py")
    st.markdown("</div>", unsafe_allow_html=True)
with n7: st.markdown("<div style='font-size:12px;color:#9ca3af;padding:18px 0;text-align:right;'>8,000 products · 248 categories</div>", unsafe_allow_html=True)
st.markdown("<hr style='margin:0;border-color:#e5e7eb;'>", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div style='background:#0f1e33;padding:40px;'>
    <div style='max-width:700px;'>
        <div style='font-size:11px;font-weight:500;color:#60a5fa;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;'>AI Shopping Assistant</div>
        <div style='font-size:26px;font-weight:600;color:#fff;line-height:1.3;margin-bottom:10px;'>
            Tell me what you need.<br><span style='color:#60a5fa;'>I'll find the best match.</span>
        </div>
        <div style='font-size:13px;color:#94a3b8;line-height:1.7;'>
            Describe your budget, use case, and preferences in plain language.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# EXAMPLES
st.markdown("<div style='background:#f8fafc;border-bottom:1px solid #e5e7eb;padding:16px 40px;'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;'>Try asking</div>", unsafe_allow_html=True)
examples = [
    "Headphones for gym under $50",
    "Laptop for college student $600",
    "Waterproof trail running shoes",
    "Fast coffee maker for busy mornings",
    "Yoga mat for beginners",
    "Keyboard for programming",
]
ex_cols = st.columns(6)
for i, ex in enumerate(examples):
    with ex_cols[i]:
        if st.button(ex, key=f"ex_{i}"):
            st.session_state['ai_query'] = ex
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# INPUT
st.markdown("<div style='padding:32px 40px 0;'>", unsafe_allow_html=True)
default_ai = st.session_state.get('ai_query', '')
ai_query = st.text_area("q", value=default_ai,
    placeholder="Describe what you're looking for...\n\ne.g. I need a laptop for video editing under $800 with good battery life.",
    height=100, label_visibility="collapsed")
c1, c2 = st.columns([1, 5])
with c1:
    ask_btn = st.button("Ask AI →", type="primary")
with c2:
    st.markdown("<p style='font-size:11px;color:#9ca3af;margin-top:12px;'>Powered by FAISS semantic search + Groq LLM</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# RESULTS
if ask_btn or default_ai:
    active = ai_query or default_ai
    if not active or len(active.strip()) < 5:
        st.warning("Please describe what you're looking for.")
    else:
        st.markdown("<div style='padding:24px 40px;'>", unsafe_allow_html=True)
        with st.spinner("AI is analyzing your request..."):
            time.sleep(0.3)
            try:
                results = semantic_search(active, top_n=5, min_score=0.15)
                if not has_strong_matches(results):
                    st.markdown("""
                    <div style='background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:16px 20px;'>
                        <div style='font-size:13px;font-weight:500;color:#92400e;margin-bottom:4px;'>No strong matches found</div>
                        <div style='font-size:12px;color:#78350f;line-height:1.7;'>Try rephrasing with different keywords or be more specific about the product type.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    llm = generate_llm_response(active, results)
                    st.markdown(f"""
                    <div style='background:#f0f7ff;border-left:3px solid #1e3a5f;border-radius:0 8px 8px 0;padding:18px 20px;margin-bottom:24px;'>
                        <div style='display:flex;align-items:center;gap:8px;margin-bottom:10px;'>
                            <div style='width:24px;height:24px;background:#1e3a5f;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;'>🤖</div>
                            <div style='font-size:11px;font-weight:500;color:#1e3a5f;text-transform:uppercase;letter-spacing:.07em;'>NovaBuy AI recommendation</div>
                        </div>
                        <div style='font-size:14px;color:#1e3a5f;line-height:1.8;'>{llm}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<div style='font-size:12px;font-weight:500;color:#374151;margin-bottom:16px;'>Matched products</div>", unsafe_allow_html=True)

                    for i, (_, row) in enumerate(results.iterrows(), 1):
                        fscore = row['final_score']
                        sem = row['semantic_score']
                        kw = row['kw_score']
                        bc = "#16a34a" if fscore>=0.6 else "#d97706" if fscore>=0.35 else "#9ca3af"
                        label = "Strong match" if fscore>=0.6 else "Partial match" if fscore>=0.35 else "Weak match"

                        img_col, info_col = st.columns([1, 5])
                        with img_col:
                            if row.get('imgUrl'):
                                st.image(row['imgUrl'], width=90)
                        with info_col:
                            st.markdown(f"""
                            <div style='background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px 16px;margin-bottom:12px;'>
                                <div style='display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:6px;'>
                                    <div style='font-size:13px;font-weight:500;color:#111827;line-height:1.5;flex:1;'>
                                        {str(row["title"])[:110]}{"..." if len(str(row["title"]))>110 else ""}
                                    </div>
                                    <span style='font-size:10px;background:#eff6ff;color:#1e3a5f;border-radius:4px;padding:2px 8px;font-weight:500;white-space:nowrap;'>#{i}</span>
                                </div>
                                <div style='font-size:11px;color:#1e3a5f;margin-bottom:10px;'>{row["category_name"]}</div>
                                <div style='margin-bottom:10px;'>
                                    <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
                                        <span style='font-size:11px;color:#6b7280;'>Confidence · {label}</span>
                                        <span style='font-size:11px;color:#6b7280;'>{fscore*100:.0f}%</span>
                                    </div>
                                    <div style='background:#f3f4f6;border-radius:4px;height:4px;'>
                                        <div style='background:{bc};height:4px;border-radius:4px;width:{fscore*100:.0f}%;'></div>
                                    </div>
                                    <div style='display:flex;gap:16px;margin-top:6px;'>
                                        <span style='font-size:10px;color:#9ca3af;'>Semantic {sem*100:.0f}%</span>
                                        <span style='font-size:10px;color:#9ca3af;'>Keyword {kw*100:.0f}%</span>
                                    </div>
                                </div>
                                <div style='display:flex;align-items:center;justify-content:space-between;'>
                                    <div>
                                        <span style='font-size:14px;font-weight:600;color:#1e3a5f;'>${row["price"]}</span>
                                        <span style='font-size:11px;color:#9ca3af;margin-left:8px;'>⭐ {row["stars"]}</span>
                                    </div>
                                    <a href='{row["productURL"]}' target='_blank' style='font-size:12px;color:#1e3a5f;font-weight:500;text-decoration:none;border:1px solid #1e3a5f;border-radius:5px;padding:5px 12px;'>View on Amazon ↗</a>
                                </div>
                            </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)