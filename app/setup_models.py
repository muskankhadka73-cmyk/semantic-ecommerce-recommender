import pandas as pd
import numpy as np
import faiss
import os
from sentence_transformers import SentenceTransformer

def build_index(data_path, save_dir):
    """Build FAISS index from scratch — used on cloud deployment."""
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Creating product texts...")
    df['product_text'] = df.apply(
        lambda row: f"{row['title']} | Category: {row['category_name']} | Rating: {row['stars']} stars | Price: ${row['price']}",
        axis=1
    )
    
    print("Generating embeddings...")
    embeddings = model.encode(
        df['product_text'].tolist(),
        batch_size=64,
        show_progress_bar=True
    ).astype('float32')
    
    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    os.makedirs(save_dir, exist_ok=True)
    np.save(os.path.join(save_dir, 'product_embeddings.npy'), embeddings)
    faiss.write_index(index, os.path.join(save_dir, 'faiss_index.bin'))
    print("Done!")
    return df, embeddings, index