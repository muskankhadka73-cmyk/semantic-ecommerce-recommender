import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from predict import semantic_search, generate_llm_response, get_feature_importance, get_correlation_data
# Page config
st.set_page_config(
    page_title="Semantic E-Commerce Recommender",
    page_icon="🛍️",
    layout="wide"
)

# Sidebar
st.sidebar.title("🛍️ Search Settings")
st.sidebar.markdown("---")

query = st.sidebar.text_input(
    "🔍 What are you looking for?",
    placeholder="e.g. wireless headphones noise cancelling"
)

top_n = st.sidebar.slider(
    "Number of recommendations",
    min_value=3,
    max_value=10,
    value=5
)

min_rating = st.sidebar.slider(
    "Minimum star rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.5
)

max_price = st.sidebar.number_input(
    "Maximum price ($)",
    min_value=1,
    max_value=10000,
    value=500
)

search_btn = st.sidebar.button("🔍 Search", type="primary")
st.sidebar.markdown("---")
st.sidebar.markdown("**Built with:** SentenceTransformers + FAISS + Groq LLM")

# Main content
st.title("🛍️ Semantic E-Commerce Product Recommender")
st.markdown("Search for products using **natural language** — powered by semantic AI")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Search", "🤖 AI Assistant", "📊 Insights"])

# ---- TAB 1: SEARCH ----
with tab1:
    if search_btn:
        # Input validation
        if not query or len(query.strip()) < 3:
            st.warning("⚠️ Please enter a search query with at least 3 characters.")
        elif max_price < 1:
            st.warning("⚠️ Please enter a valid maximum price.")
        else:
            with st.spinner("🔍 Searching for products..."):
                try:
                    results = semantic_search(query, top_n=top_n)

                    # Filter by rating and price
                    results = results[
                        (results['stars'] >= min_rating) &
                        (results['price'] <= max_price)
                    ]

                    if len(results) == 0:
                        st.warning("No products found matching your filters. Try adjusting the price or rating filters.")
                    else:
                        st.success(f"Found {len(results)} products matching '{query}'")

                        for i, (_, row) in enumerate(results.iterrows(), 1):
                            with st.expander(f"#{i} — {row['title'][:80]}...", expanded=(i==1)):
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    if row['imgUrl']:
                                        st.image(row['imgUrl'], width=150)
                                with col2:
                                    st.markdown(f"**Category:** {row['category_name']}")
                                    st.markdown(f"**Rating:** {'⭐' * int(row['stars'])} ({row['stars']})")
                                    st.markdown(f"**Price:** ${row['price']}")
                                    st.markdown(f"**Semantic Match:** {row['semantic_score']:.2%}")
                                    st.markdown(f"[View on Amazon]({row['productURL']})")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("👈 Enter your search query in the sidebar and click **Search**")

# ---- TAB 2: AI ASSISTANT ----
with tab2:
    st.subheader("🤖 AI Shopping Assistant")
    st.markdown("Get AI-powered recommendations and insights")

    ai_query = st.text_input(
        "Ask the AI assistant:",
        placeholder="e.g. I need a laptop for video editing under $1000"
    )

    if st.button("Get AI Recommendation", type="primary"):
        if not ai_query or len(ai_query.strip()) < 3:
            st.warning("⚠️ Please enter a valid query.")
        else:
            with st.spinner("🤖 AI is thinking..."):
                try:
                    results = semantic_search(ai_query, top_n=5)
                    llm_response = generate_llm_response(ai_query, results)

                    st.markdown("### 🤖 AI Response")
                    st.info(llm_response)

                    st.markdown("### 📦 Recommended Products")
                    st.dataframe(
                        results[['title', 'category_name', 'stars', 'price', 'semantic_score']],
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# ---- TAB 3: INSIGHTS ----
with tab3:
    st.subheader("📊 Model Insights")
    st.markdown("Understanding how the recommendation system works")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Correlation Heatmap")
        corr = get_correlation_data()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm',
                    center=0, fmt='.2f', ax=ax)
        ax.set_title('Feature Correlation Matrix')
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("#### Feature Importance (Random Forest)")
        feat_imp = get_feature_importance()
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.barplot(data=feat_imp, x='importance',
                    y='feature', palette='viridis', ax=ax2)
        ax2.set_title('Feature Importance Score')
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("---")
    st.markdown("#### 📈 Dataset Statistics")
    col3, col4, col5, col6 = st.columns(4)
    col3.metric("Total Products", "8,000")
    col4.metric("Categories", "248")
    col5.metric("Avg Rating", "4.40 ⭐")
    col6.metric("Avg Price", "$41.19")