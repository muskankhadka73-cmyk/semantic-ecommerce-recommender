
# Prompt Engineering Documentation
## Week 5 - Semantic E-Commerce Recommender

## Model Used
- Provider: Groq
- Model: llama-3.1-8b-instant
- Reason: Free tier, fast inference, strong instruction following

## Prompts Designed

### 1. Product Summary Generator
- Purpose: Explain why recommendations match the user query
- Approach: System prompt sets assistant as shopping helper,
  user prompt passes query + product list
- Output: 2-3 sentence natural language summary

### 2. Value Analysis Advisor  
- Purpose: Identify best value product from recommendations
- Approach: System prompt sets assistant as value advisor,
  user prompt passes products with price/rating data
- Output: 2-3 sentence value recommendation

### 3. Shopping Tip Generator
- Purpose: Give practical category-specific shopping advice
- Approach: System prompt sets assistant as practical advisor,
  user prompt passes category and price statistics
- Output: 1-2 sentence actionable tip

## Key Prompt Engineering Principles Applied
- Clear role definition in system prompt
- Specific output format requested (2-3 sentences)
- Relevant context passed (prices, ratings, categories)
- Temperature kept at default for consistent outputs
