import streamlit as st
import pandas as pd
import numpy as np
import faiss
import joblib
import os
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')   
# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'amazon_featured.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
EMBEDDINGS_PATH = os.path.join(MODELS_DIR, 'product_embeddings.npy')
FAISS_PATH = os.path.join(MODELS_DIR, 'faiss_index.bin')
RF_MODEL_PATH = os.path.join(MODELS_DIR, 'rf_optimized.pkl')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

# Load embedding model
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# Load or build FAISS index
@st.cache_resource
def load_index():
    embedding_model = load_embedding_model()
    df = load_data()
    
    if os.path.exists(FAISS_PATH) and os.path.exists(EMBEDDINGS_PATH):
        embeddings = np.load(EMBEDDINGS_PATH).astype('float32')
        index = faiss.read_index(FAISS_PATH)
    else:
        # Build from scratch (for cloud deployment)
        df['product_text'] = df.apply(
            lambda row: f"{row['title']} | Category: {row['category_name']} | Rating: {row['stars']} stars | Price: ${row['price']}",
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

# Load RF model
@st.cache_resource
def load_rf_model():
    return joblib.load(RF_MODEL_PATH)

@st.cache_resource
def load_scaler():
    return joblib.load(SCALER_PATH)

# Groq client
@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

def semantic_search(query, top_n=5):
    df = load_data()
    embedding_model = load_embedding_model()
    index, _ = load_index()
    
    query_embedding = embedding_model.encode([query]).astype('float32')
    faiss.normalize_L2(query_embedding)
    scores, indices = index.search(query_embedding, top_n)
    
    results = df.iloc[indices[0]].copy()
    results['semantic_score'] = scores[0].round(4)
    return results[['title', 'category_name', 'stars', 'price',
                     'imgUrl', 'productURL', 'semantic_score']]

def generate_llm_response(query, results):
    client = get_groq_client()
    context = ""
    for i, (_, row) in enumerate(results.iterrows(), 1):
        context += f"{i}. {row['title']}\n"
        context += f"   Category: {row['category_name']} | "
        context += f"Rating: {row['stars']} stars | Price: ${row['price']}\n\n"

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful e-commerce shopping assistant. Provide a 3-4 sentence recommendation response that highlights the best product and price range."},
            {"role": "user", "content": f'User query: "{query}"\n\nProducts:\n{context}'}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def get_feature_importance():
    rf_model = load_rf_model()
    feature_cols = ['stars', 'price', 'reviews', 'boughtInLastMonth',
                    'discount_pct', 'popularity_score', 'value_score', 'title_length']
    return pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

def get_correlation_data():
    df = load_data()
    numeric_cols = ['stars', 'price', 'reviews', 'boughtInLastMonth',
                    'discount_pct', 'popularity_score', 'value_score']
    return df[numeric_cols].corr()