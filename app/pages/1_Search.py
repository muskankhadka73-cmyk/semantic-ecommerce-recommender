import streamlit as st
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predict import semantic_search, has_strong_matches

st.set_page_config(
    page_title="Search — NovaBuy AI",
    page_icon="🔍", layout="wide",
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
n1,n2,n3,n4,n5,n6,n7 = st.columns([2,1,1,1,1,1,2])
with n1:
    st.markdown("<div style='display:flex;align-items:center;gap:8px;padding:14px 0;'><div style='width:8px;height:8px;background:#1e3a5f;border-radius:50%;'></div><span style='font-size:15px;font-weight:600;color:#111827;'>NovaBuy AI</span></div>", unsafe_allow_html=True)
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
with n7:
    st.markdown("<div style='font-size:12px;color:#9ca3af;padding:18px 0;text-align:right;'>8,000 products · 248 categories</div>", unsafe_allow_html=True)
st.markdown("<hr style='margin:0;border-color:#e5e7eb;'>", unsafe_allow_html=True)

# ── SEARCH BAR ───────────────────────────────────────────────────────────────
st.markdown("<div style='background:#f8fafc;border-bottom:1px solid #e5e7eb;padding:24px 40px;'>", unsafe_allow_html=True)
st.markdown("<div style='font-size:11px;font-weight:500;color:#1e3a5f;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;'>Product search</div>", unsafe_allow_html=True)

default_q = st.session_state.get('home_query', '')
sc1, sc2, sc3 = st.columns([4, 1, 1])
with sc1:
    query = st.text_input("q", value=default_q,
        placeholder="e.g. noise cancelling headphones under $100",
        label_visibility="collapsed")
with sc2:
    search_btn = st.button("Search", type="primary")
with sc3:
    if st.button("Clear"):
        st.session_state['home_query'] = ''
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ── LAYOUT ───────────────────────────────────────────────────────────────────
main_col, filter_col = st.columns([4, 1])

with filter_col:
    st.markdown("<div style='padding:20px 16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;font-weight:500;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;margin-bottom:14px;'>Filters</div>", unsafe_allow_html=True)
    min_rating = st.slider("Min rating ⭐", 1.0, 5.0, 3.0, 0.5)
    max_price  = st.number_input("Max price ($)", 1, 10000, 500)
    top_n      = st.slider("Results", 3, 12, 6)
    min_conf   = st.slider("Min confidence (%)", 0, 100, 20)
    sort_by    = st.selectbox("Sort by", ["Best match","Rating ↓","Price ↑","Price ↓"])

    st.markdown("<div style='margin-top:20px;padding:14px;background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;'>Quick searches</div>", unsafe_allow_html=True)
    for q in ["wireless headphones","laptop under $500","running shoes","coffee maker","yoga mat","mechanical keyboard"]:
        if st.button(q, key=f"qs_{q}"):
            st.session_state['home_query'] = q
            st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

with main_col:
    st.markdown("<div style='padding:20px 0 20px 40px;'>", unsafe_allow_html=True)
    active_query = query or default_q
    if search_btn or default_q:
        if not active_query or len(active_query.strip()) < 3:
            st.warning("Enter at least 3 characters.")
        else:
            with st.spinner("Searching..."):
                time.sleep(0.2)
                try:
                    results = semantic_search(active_query, top_n=top_n, min_score=min_conf/100)
                    if not results.empty:
                        results = results[(results['stars'] >= min_rating) & (results['price'] <= max_price)]
                    if not has_strong_matches(results):
                        st.markdown(f"""
                        <div style='text-align:center;padding:60px 20px;'>
                            <div style='font-size:32px;margin-bottom:12px;'>🔍</div>
                            <div style='font-size:14px;font-weight:500;color:#374151;'>No strong matches found</div>
                            <div style='font-size:12px;color:#9ca3af;margin-top:8px;line-height:1.8;'>
                                No products closely match "<strong>{active_query}</strong>".<br>
                                Try a broader term or lower the confidence threshold.
                            </div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        if sort_by == "Rating ↓": results = results.sort_values('stars', ascending=False)
                        elif sort_by == "Price ↑": results = results.sort_values('price')
                        elif sort_by == "Price ↓": results = results.sort_values('price', ascending=False)

                        st.markdown(f"<div style='font-size:12px;color:#6b7280;margin-bottom:16px;'><span style='color:#16a34a;'>✓</span> &nbsp;{len(results)} results for <strong style='color:#111827;'>\"{active_query}\"</strong></div>", unsafe_allow_html=True)

                        for row_start in range(0, len(results), 3):
                            row_results = results.iloc[row_start:row_start+3]
                            card_cols = st.columns(3)
                            for ci, (_, row) in enumerate(row_results.iterrows()):
                                with card_cols[ci]:
                                    fscore = row['final_score']
                                    rank = row_start + ci + 1
                                    bc = "#16a34a" if fscore>=0.6 else "#d97706" if fscore>=0.35 else "#9ca3af"
                                    bb = "#f0fdf4" if fscore>=0.6 else "#fffbeb" if fscore>=0.35 else "#f9fafb"
                                    be = "#bbf7d0" if fscore>=0.6 else "#fde68a" if fscore>=0.35 else "#e5e7eb"
                                    bt = "Strong" if fscore>=0.6 else "Partial" if fscore>=0.35 else "Weak"
                                    st.markdown(f"""
                                    <div style='background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px;margin-bottom:16px;'>
                                        <div style='background:#f8fafc;border-radius:6px;height:150px;display:flex;align-items:center;justify-content:center;margin-bottom:12px;overflow:hidden;'>
                                            <img src='{row["imgUrl"]}' style='max-height:140px;max-width:100%;object-fit:contain;' onerror="this.style.display='none'">
                                        </div>
                                        <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;'>
                                            <span style='font-size:10px;color:{bc};background:{bb};border:1px solid {be};border-radius:4px;padding:2px 7px;font-weight:500;'>{bt} match</span>
                                            <span style='font-size:10px;color:#9ca3af;'>#{rank}</span>
                                        </div>
                                        <div style='font-size:11px;color:#1e3a5f;margin-bottom:5px;'>{row["category_name"]}</div>
                                        <div style='font-size:13px;font-weight:500;color:#111827;line-height:1.4;margin-bottom:10px;min-height:52px;'>
                                            {str(row["title"])[:80]}{"..." if len(str(row["title"]))>80 else ""}
                                        </div>
                                        <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;'>
                                            <div>
                                                <span style='font-size:14px;font-weight:600;color:#1e3a5f;'>${row["price"]}</span>
                                                <span style='font-size:11px;color:#9ca3af;margin-left:6px;'>⭐ {row["stars"]}</span>
                                            </div>
                                            <span style='font-size:10px;color:#9ca3af;'>{fscore*100:.0f}% conf.</span>
                                        </div>
                                        <a href='{row["productURL"]}' target='_blank' style='display:block;text-align:center;font-size:12px;color:#1e3a5f;font-weight:500;text-decoration:none;border:1px solid #1e3a5f;border-radius:5px;padding:6px 0;'>View on Amazon ↗</a>
                                    </div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.markdown("""
        <div style='text-align:center;padding:80px 20px;'>
            <div style='font-size:36px;margin-bottom:12px;'>🔍</div>
            <div style='font-size:14px;font-weight:500;color:#374151;'>Search for any product</div>
            <div style='font-size:12px;color:#9ca3af;margin-top:6px;'>Results ranked by semantic similarity + keyword matching + quality</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)