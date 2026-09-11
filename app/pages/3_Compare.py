import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predict import semantic_search, generate_comparison, load_data

st.set_page_config(page_title="Compare — NovaBuy AI", page_icon="⚖️",
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
<div style='background:#0f1e33;padding:36px 40px;'>
    <div style='font-size:11px;font-weight:500;color:#60a5fa;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;'>AI Comparison Center</div>
    <div style='font-size:26px;font-weight:600;color:#fff;line-height:1.3;margin-bottom:8px;'>
        Compare products side by side.<br><span style='color:#60a5fa;'>AI picks the winner.</span>
    </div>
    <div style='font-size:13px;color:#94a3b8;'>Search for two products and let AI compare them with pros, cons, and a verdict.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding:32px 40px;'>", unsafe_allow_html=True)

# SEARCH FOR TWO PRODUCTS
col_a, col_vs, col_b = st.columns([5, 1, 5])

with col_a:
    st.markdown("<div style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Product A</div>", unsafe_allow_html=True)
    query_a = st.text_input("qa", placeholder="e.g. Sony WH-1000XM5 headphones",
                             label_visibility="collapsed")
    search_a = st.button("Search A", key="sa", type="primary")

with col_vs:
    st.markdown("<div style='text-align:center;padding-top:32px;font-size:18px;font-weight:600;color:#9ca3af;'>vs</div>", unsafe_allow_html=True)

with col_b:
    st.markdown("<div style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Product B</div>", unsafe_allow_html=True)
    query_b = st.text_input("qb", placeholder="e.g. Bose QuietComfort 45",
                             label_visibility="collapsed")
    search_b = st.button("Search B", key="sb", type="primary")

# Search and select product A
if search_a and query_a:
    results_a = semantic_search(query_a, top_n=5, min_score=0.1)
    if not results_a.empty:
        options_a = results_a['title'].str[:80].tolist()
        selected_a = st.selectbox("Select Product A", options_a, key="sel_a")
        st.session_state['product_a'] = results_a[results_a['title'].str[:80] == selected_a].iloc[0].to_dict()

# Search and select product B
if search_b and query_b:
    results_b = semantic_search(query_b, top_n=5, min_score=0.1)
    if not results_b.empty:
        options_b = results_b['title'].str[:80].tolist()
        selected_b = st.selectbox("Select Product B", options_b, key="sel_b")
        st.session_state['product_b'] = results_b[results_b['title'].str[:80] == selected_b].iloc[0].to_dict()

# Compare button
if 'product_a' in st.session_state and 'product_b' in st.session_state:
    pa = st.session_state['product_a']
    pb = st.session_state['product_b']

    # Side by side cards
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    ca, cb = st.columns(2)

    for col, prod, label in [(ca, pa, "A"), (cb, pb, "B")]:
        with col:
            st.markdown(f"""
            <div style='background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:20px;'>
                <div style='font-size:10px;font-weight:500;color:#1e3a5f;text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;'>Product {label}</div>
                <div style='background:#fff;border-radius:6px;height:160px;display:flex;align-items:center;justify-content:center;margin-bottom:14px;overflow:hidden;border:1px solid #e5e7eb;'>
                    <img src='{prod.get("imgUrl","")}' style='max-height:150px;max-width:100%;object-fit:contain;' onerror="this.style.display='none'">
                </div>
                <div style='font-size:13px;font-weight:500;color:#111827;line-height:1.4;margin-bottom:10px;'>
                    {str(prod["title"])[:100]}{"..." if len(str(prod["title"]))>100 else ""}
                </div>
                <div style='font-size:11px;color:#1e3a5f;margin-bottom:10px;'>{prod["category_name"]}</div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
                    <div style='background:#fff;border:1px solid #e5e7eb;border-radius:6px;padding:10px;text-align:center;'>
                        <div style='font-size:16px;font-weight:600;color:#1e3a5f;'>${prod["price"]}</div>
                        <div style='font-size:10px;color:#9ca3af;margin-top:2px;'>Price</div>
                    </div>
                    <div style='background:#fff;border:1px solid #e5e7eb;border-radius:6px;padding:10px;text-align:center;'>
                        <div style='font-size:16px;font-weight:600;color:#1e3a5f;'>{prod["stars"]} ⭐</div>
                        <div style='font-size:10px;color:#9ca3af;margin-top:2px;'>Rating</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # AI Compare button
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([2,1,2])
    with mid:
        compare_btn = st.button("⚖️  AI Compare →", type="primary")

    if compare_btn:
        with st.spinner("AI is comparing products..."):
            try:
                analysis = generate_comparison(pa, pb)
                st.markdown(f"""
                <div style='background:#f0f7ff;border-left:3px solid #1e3a5f;border-radius:0 8px 8px 0;padding:20px 24px;margin-top:20px;'>
                    <div style='display:flex;align-items:center;gap:8px;margin-bottom:12px;'>
                        <div style='width:24px;height:24px;background:#1e3a5f;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;'>⚖️</div>
                        <div style='font-size:11px;font-weight:500;color:#1e3a5f;text-transform:uppercase;letter-spacing:.07em;'>AI Comparison Analysis</div>
                    </div>
                    <div style='font-size:13px;color:#1e3a5f;line-height:1.9;white-space:pre-wrap;'>{analysis}</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)