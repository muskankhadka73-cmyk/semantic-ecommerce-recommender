# Semantic E-Commerce Product Recommender 

A production-ready AI-powered product recommendation system built with 
semantic search and RAG (Retrieval-Augmented Generation). Users can search 
for products using natural language queries like "laptop for video editing 
under $1000" and get semantically relevant results.

## Live Demo
Coming in Week 7 — Streamlit Cloud URL will be added here.

##  Project Overview
- **Type:** Unsupervised / Semantic Search
- **Dataset:** Amazon Products Dataset (Kaggle) — 1.4M rows sampled to 8,000
- **Categories:** 248 product categories
- **Internship:** Techaxis Remote Data Science Internship — 8-Week Capstone

##  Tech Stack
| Layer | Tools |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| ML Models | Scikit-Learn, Random Forest, KNN |
| Semantic Search | SentenceTransformers, FAISS |
| LLM/RAG | LangChain, ChromaDB, OpenAI API |
| Deployment | Streamlit, Streamlit Cloud |
| MLOps | GitHub Actions, Joblib |

##  Project Structure
├── data/
│ ├── raw/ ← Original sampled dataset
│ └── processed/ ← Cleaned and feature-engineered datasets
├── docs/ ← EDA charts, reports, proposals
├── models/ ← Saved .pkl model files
├── notebooks/ ← Weekly Jupyter notebooks
├── .gitignore
├── README.md
└── requirements.txt
## Weekly Progress
| Week | Topic | Status |
|---|---|---|
| 1 | Problem Definition & Data Collection | Done |
| 2 | Data Cleaning & EDA |  Done |
| 3 | Feature Engineering & Baseline Model | Done |
| 4 | Advanced ML & Hyperparameter Tuning | Done |
| 5 | Generative AI & LLM Integration | In Progress |
| 6 | RAG System | Upcoming |
| 7 | MLOps & Streamlit Deployment | Upcoming |
| 8 | Final Capstone | ⏳ Upcoming |

## Model Performance
| Model | Accuracy |
|---|---|
| TF-IDF Baseline (Week 3) | Cosine similarity based |
| Random Forest Baseline | 6.63% |
| Optimized Random Forest | 9.69% |

## Key Findings (EDA)
- Average product rating: 4.40 stars
- Average price: $41.19
- Price and listPrice correlation: 0.45
- Star rating shows negligible correlation with price or popularity
- Best Sellers represent only 0.54% of products

## Author
Muskan Khadka
Techaxis Remote Data Science Internship 2026