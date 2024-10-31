from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import json
from config import OPENAI_API_KEY

def get_query_embedding(query, embeddings_model):
    return embeddings_model.embed_query(query)

def select_top_n(embeddings, query_embedding, top_n):
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    return top_indices

def get_urls_for_query(query, embeddings_model, data, top_n=5):
    embeddings = [item['embedding'] for item in data]
    query_emb = get_query_embedding(query, embeddings_model)
    top_indices = select_top_n(embeddings, query_emb, top_n)
    top_urls = [data[i]['url'] for i in top_indices]
    return top_urls

def main():
    query = input("Enter your query: ")
    embeddings_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    with open('site_titles_urls.json', 'r') as f:
        data = json.load(f)
    
    top_urls = get_urls_for_query(query, embeddings_model, data)
    
    print(top_urls)

    # with open('selected_urls.txt', 'w') as f:
    #     for url in top_urls:
    #         f.write(f"{url}\n")
    
    # print(f"Selected top {NUM_URLS_TO_SELECT} relevant URLs saved to selected_urls.txt.")

if __name__ == "__main__":
    main()
