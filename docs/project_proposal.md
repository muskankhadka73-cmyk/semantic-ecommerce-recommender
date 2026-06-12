\# Project Proposal: Semantic E-Commerce Product Recommender



\## Intern Details

\- Name: \[Muskan Khadka]

\- Program: Techaxis Remote Data Science Internship

\- Week: 1



\## Business Problem

E-commerce platforms lose revenue when users cannot find products 

using natural language queries like "laptop for video editing under $1000". 

Traditional keyword search fails to understand user intent. This tool uses 

semantic similarity and RAG to match natural language queries to relevant products.



\## Success Metrics

\- Top-3 retrieved results are semantically relevant to the query

\- Query response time under 3 seconds on Streamlit Cloud

\- RAG chatbot answers 80%+ of product-related questions correctly



\## Dataset

\- Source: Amazon Products Dataset (Kaggle)

\- Original size: 1,426,337 rows × 11 columns

\- Sampled size: 8,000 rows (stratified by category, 248 categories)

\- Key fields: title, category\_name, stars, price, reviews



\## Tech Stack

\- ML: Scikit-Learn, FAISS, SentenceTransformers

\- AI/RAG: LangChain, ChromaDB

\- App: Streamlit

\- MLOps: GitHub Actions, Streamlit Cloud



\## Week 1 Scope

\- \[x] Project selected and defined

\- \[x] Dataset sourced from Kaggle

\- \[x] Dataset sampled (1.4M → 8,000 rows)

\- \[x] Data dictionary documented

\- \[x] GitHub repository initialized

