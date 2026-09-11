import streamlit as st
import pandas as pd
import numpy as np
import faiss
import joblib
import os
import re
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'amazon_featured.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
EMBEDDINGS_PATH = os.path.join(MODELS_DIR, 'product_embeddings.npy')
FAISS_PATH = os.path.join(MODELS_DIR, 'faiss_index.bin')
RF_MODEL_PATH = os.path.join(MODELS_DIR, 'rf_optimized.pkl')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')


@st.cache_resource
def load_index():
    embedding_model = load_embedding_model()
    df = load_data()
    if os.path.exists(FAISS_PATH) and os.path.exists(EMBEDDINGS_PATH):
        embeddings = np.load(EMBEDDINGS_PATH).astype('float32')
        index = faiss.read_index(FAISS_PATH)
    else:
        df['product_text'] = df.apply(
            lambda r: f"{r['title']} | Category: {r['category_name']} "
                      f"| Rating: {r['stars']} stars | Price: ${r['price']}",
            axis=1
        )
        embeddings = embedding_model.encode(
            df['product_text'].tolist(),
            batch_size=64,
            show_progress_bar=False
        ).astype('float32')
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        os.makedirs(MODELS_DIR, exist_ok=True)
        np.save(EMBEDDINGS_PATH, embeddings)
        faiss.write_index(index, FAISS_PATH)
    return index, embeddings


@st.cache_resource
def load_rf_model():
    return joblib.load(RF_MODEL_PATH)


@st.cache_resource
def load_scaler():
    return joblib.load(SCALER_PATH)


@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)


def keyword_score(query: str, title: str, category: str) -> float:
    """Score how many query keywords appear in title or category."""
    stop_words = {
        'a','an','the','for','with','and','or','of','to','in',
        'on','at','is','it','i','need','want','buy','get','find',
        'best','good','cheap','nice','great','some','any','under',
        'over','around','about','my','me','please','looking'
    }
    query_words = set(re.findall(r'\b\w+\b', query.lower())) - stop_words
    if not query_words:
        return 0.0
    text = (str(title) + ' ' + str(category)).lower()
    matches = sum(1 for w in query_words if w in text)
    return matches / len(query_words)


def rerank(query: str, results: pd.DataFrame) -> pd.DataFrame:
    """
    Combine semantic score + keyword match + quality signal.
    Weights: semantic 55%, keyword 35%, quality 10%.
    """
    df_r = results.copy()
    df_r['kw_score'] = df_r.apply(
        lambda r: keyword_score(
            query, str(r['title']), str(r['category_name'])),
        axis=1
    )
    df_r['quality'] = (df_r['stars'] - 1) / 4.0
    df_r['final_score'] = (
        0.55 * df_r['semantic_score'] +
        0.35 * df_r['kw_score'] +
        0.10 * df_r['quality']
    ).round(4)
    return df_r.sort_values('final_score', ascending=False)


def semantic_search(query: str, top_n: int = 5,
                    min_score: float = 0.0) -> pd.DataFrame:
    """
    Full 3-stage pipeline:
    1. FAISS semantic retrieval
    2. Keyword + quality reranking
    3. Score threshold filter
    """
    df = load_data()
    embedding_model = load_embedding_model()
    index, _ = load_index()

    # Retrieve more candidates than needed for reranking
    candidates = min(top_n * 8, len(df))
    query_embedding = embedding_model.encode([query]).astype('float32')
    faiss.normalize_L2(query_embedding)
    scores, indices = index.search(query_embedding, candidates)

    results = df.iloc[indices[0]].copy()
    results['semantic_score'] = scores[0].round(4)

    # Rerank
    results = rerank(query, results)

    # Filter by minimum confidence score
    results = results[results['final_score'] >= min_score]

    # Return top N with relevant columns only
    cols = ['title', 'category_name', 'stars', 'price',
            'imgUrl', 'productURL', 'semantic_score',
            'kw_score', 'final_score']
    return results[cols].head(top_n).reset_index(drop=True)


def has_strong_matches(results: pd.DataFrame,
                       threshold: float = 0.25) -> bool:
    """Return True only when results contain meaningful matches."""
    if results is None or results.empty:
        return False
    return float(results['final_score'].max()) >= threshold


def generate_llm_response(query: str, results: pd.DataFrame) -> str:
    """Generate a plain-English recommendation summary via Groq LLM."""
    client = get_groq_client()
    context = ""
    for i, (_, row) in enumerate(results.iterrows(), 1):
        context += (
            f"{i}. {row['title']}\n"
            f"   Category: {row['category_name']} | "
            f"Rating: {row['stars']} stars | "
            f"Price: ${row['price']}\n\n"
        )
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful e-commerce shopping assistant. "
                    "Given a user query and a list of matching products, "
                    "write a concise 2-3 sentence recommendation. "
                    "Name the top pick, explain why it fits the query, "
                    "and mention the price range available. "
                    "Be specific, friendly, and helpful."
                )
            },
            {
                "role": "user",
                "content": f'Query: "{query}"\n\nProducts:\n{context}'
            }
        ],
        max_tokens=250
    )
    return response.choices[0].message.content


def generate_comparison(product_a: dict, product_b: dict) -> str:
    """Generate AI comparison between two products."""
    client = get_groq_client()
    prompt = (
        f"Compare these two products and give a verdict:\n\n"
        f"Product A: {product_a['title']}\n"
        f"Price: ${product_a['price']} | "
        f"Rating: {product_a['stars']} stars | "
        f"Category: {product_a['category_name']}\n\n"
        f"Product B: {product_b['title']}\n"
        f"Price: ${product_b['price']} | "
        f"Rating: {product_b['stars']} stars | "
        f"Category: {product_b['category_name']}\n\n"
        f"Give: 2 pros for each, 1 con for each, "
        f"and a one-sentence verdict on which to buy and why. "
        f"Keep it concise and practical."
    )
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a sharp product analyst. "
                    "Give practical, honest product comparisons."
                )
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=350
    )
    return response.choices[0].message.content


def get_feature_importance() -> pd.DataFrame:
    rf_model = load_rf_model()
    feature_cols = [
        'stars', 'price', 'reviews', 'boughtInLastMonth',
        'discount_pct', 'popularity_score',
        'value_score', 'title_length'
    ]
    return pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)


def get_correlation_data() -> pd.DataFrame:
    df = load_data()
    numeric_cols = [
        'stars', 'price', 'reviews', 'boughtInLastMonth',
        'discount_pct', 'popularity_score', 'value_score'
    ]
    return df[numeric_cols].corr()


def get_trending(n: int = 8) -> pd.DataFrame:
    """Top rated + most bought products."""
    df = load_data()
    return (
        df[df['stars'] >= 4.5]
        .sort_values('boughtInLastMonth', ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def get_top_categories(n: int = 12) -> pd.DataFrame:
    """Most popular categories by product count."""
    df = load_data()
    return (
        df.groupby('category_name')
        .agg(count=('title', 'count'),
             avg_rating=('stars', 'mean'),
             avg_price=('price', 'mean'))
        .sort_values('count', ascending=False)
        .head(n)
        .reset_index()
    )