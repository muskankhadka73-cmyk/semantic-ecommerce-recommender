import streamlit as st
import sys, os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predict import load_data, get_feature_importance, get_correlation_data

st.set_page_config(page_title="Insights — NovaBuy AI", page_icon="📊",
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
    <div style='font-size:11px;font-weight:500;color:#60a5fa;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;'>Analytics Dashboard</div>
    <div style='font-size:26px;font-weight:600;color:#fff;line-height:1.3;margin-bottom:8px;'>
        Insights & model explainability
    </div>
    <div style='font-size:13px;color:#94a3b8;'>
        Understanding the dataset and what drives recommendations
    </div>
</div>
""", unsafe_allow_html=True)

df = load_data()

st.markdown("<div style='padding:32px 40px;'>", unsafe_allow_html=True)

# METRIC CARDS
c1,c2,c3,c4,c5 = st.columns(5)
for col, val, lbl in [
    (c1, "8,000",   "Products"),
    (c2, "248",     "Categories"),
    (c3, f"{df['stars'].mean():.2f} ⭐", "Avg rating"),
    (c4, f"${df['price'].mean():.2f}", "Avg price"),
    (c5, f"{df['isBestSeller'].sum()}", "Best sellers"),
]:
    col.markdown(f"""
    <div style='background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;padding:16px;text-align:center;margin-bottom:16px;'>
        <div style='font-size:20px;font-weight:600;color:#1e3a5f;'>{val}</div>
        <div style='font-size:11px;color:#9ca3af;margin-top:4px;'>{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ROW 1: Price distribution + Rating distribution
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.markdown("<p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Price distribution</p>", unsafe_allow_html=True)
    df_price = df[df['price'] <= 300]
    fig = px.histogram(df_price, x='price', nbins=40,
                       color_discrete_sequence=['#1e3a5f'])
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0,r=0,t=10,b=0), height=260,
        xaxis_title="Price ($)", yaxis_title="Count",
        font=dict(family='Inter', size=11, color='#6b7280'),
        xaxis=dict(gridcolor='#f3f4f6'),
        yaxis=dict(gridcolor='#f3f4f6'),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.markdown("<p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Rating distribution</p>", unsafe_allow_html=True)
    rating_counts = df['stars'].value_counts().sort_index().reset_index()
    rating_counts.columns = ['stars', 'count']
    fig2 = px.bar(rating_counts, x='stars', y='count',
                  color_discrete_sequence=['#1e3a5f'])
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0,r=0,t=10,b=0), height=260,
        xaxis_title="Stars", yaxis_title="Count",
        font=dict(family='Inter', size=11, color='#6b7280'),
        xaxis=dict(gridcolor='#f3f4f6'),
        yaxis=dict(gridcolor='#f3f4f6'),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# ROW 2: Top categories + Feature importance
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown("<p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Top 10 categories by product count</p>", unsafe_allow_html=True)
    top_cats = (df.groupby('category_name')
                  .size()
                  .reset_index(name='count')
                  .sort_values('count', ascending=True)
                  .tail(10))
    fig3 = px.bar(top_cats, x='count', y='category_name',
                  orientation='h',
                  color_discrete_sequence=['#1e3a5f'])
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0,r=0,t=10,b=0), height=300,
        xaxis_title="Products", yaxis_title="",
        font=dict(family='Inter', size=11, color='#6b7280'),
        xaxis=dict(gridcolor='#f3f4f6'),
        yaxis=dict(gridcolor='#f3f4f6'),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.markdown("<p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Feature importance (Random Forest model)</p>", unsafe_allow_html=True)
    fi = get_feature_importance()
    colors = ['#1e3a5f' if i == 0 else '#93c5fd' for i in range(len(fi))]
    fig4 = go.Figure(go.Bar(
        x=fi['importance'], y=fi['feature'],
        orientation='h', marker_color=colors
    ))
    fig4.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0,r=0,t=10,b=0), height=300,
        xaxis_title="Importance score", yaxis_title="",
        font=dict(family='Inter', size=11, color='#6b7280'),
        xaxis=dict(gridcolor='#f3f4f6'),
        yaxis=dict(gridcolor='#f3f4f6'),
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

# ROW 3: Price vs Rating scatter + Best seller breakdown
r3c1, r3c2 = st.columns(2)

with r3c1:
    st.markdown("<p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Price vs rating (sample)</p>", unsafe_allow_html=True)
    sample = df[df['price'] <= 300].sample(min(500, len(df)), random_state=42)
    fig5 = px.scatter(sample, x='price', y='stars',
                      color='category_name',
                      hover_data=['title'],
                      opacity=0.5)
    fig5.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0,r=0,t=10,b=0), height=300,
        xaxis_title="Price ($)", yaxis_title="Stars",
        font=dict(family='Inter', size=11, color='#6b7280'),
        xaxis=dict(gridcolor='#f3f4f6'),
        yaxis=dict(gridcolor='#f3f4f6'),
        showlegend=False
    )
    st.plotly_chart(fig5, use_container_width=True)

with r3c2:
    st.markdown("<p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:8px;'>Correlation heatmap</p>", unsafe_allow_html=True)
    corr = get_correlation_data()
    fig6 = px.imshow(
        corr, text_auto='.2f',
        color_continuous_scale=[
            [0, '#dbeafe'], [0.5, '#93c5fd'], [1, '#1e3a5f']
        ]
    )
    fig6.update_layout(
        margin=dict(l=0,r=0,t=10,b=0), height=300,
        font=dict(family='Inter', size=10, color='#374151'),
        paper_bgcolor='white',
        coloraxis_showscale=False
    )
    st.plotly_chart(fig6, use_container_width=True)

# Architecture block
st.markdown("""
<div style='background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;padding:20px;margin-top:8px;'>
    <p style='font-size:12px;font-weight:500;color:#374151;margin-bottom:12px;'>System architecture</p>
    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px;font-size:11px;color:#9ca3af;'>
        <div><strong style='color:#1e3a5f;'>Embedding</strong><br>all-MiniLM-L6-v2 · 384 dimensions</div>
        <div><strong style='color:#1e3a5f;'>Vector store</strong><br>FAISS IndexFlatIP · cosine similarity</div>
        <div><strong style='color:#1e3a5f;'>Reranking</strong><br>Semantic 55% + Keyword 35% + Quality 10%</div>
        <div><strong style='color:#1e3a5f;'>ML model</strong><br>Random Forest · optimized with Optuna</div>
        <div><strong style='color:#1e3a5f;'>LLM</strong><br>Groq API · openai/gpt-oss-20b</div>
        <div><strong style='color:#1e3a5f;'>Dataset</strong><br>Amazon Products · 1.4M → 8K sampled</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)