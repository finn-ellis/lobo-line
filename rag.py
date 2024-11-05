import json
import os
import bs4
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
from langchain import hub
from langchain_chroma import Chroma
# from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import JSONLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import OPENAI_API_KEY
from tqdm import tqdm

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

DB_PERSIST_DIR = "./chroma_db"

async def load_documents(loader):
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)
    return docs

def load_db():
	loader = JSONLoader(
		file_path='links_pages.json',
		jq_schema='.[]',
		content_key=".page",
		is_content_key_jq_parsable=True,
		metadata_func=lambda record, metadata: {**metadata, "source": record.get("link")}
	)
	
	print('loading documents')
	docs = asyncio.run(load_documents(loader))
	text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
	splits = text_splitter.split_documents(docs)

	print("embedding documents")
	vectorstore = Chroma.from_documents(
		documents=splits, 
		embedding=OpenAIEmbeddings(),
		persist_directory=DB_PERSIST_DIR
	)
	# Persist the database to disk
	vectorstore.persist()
	return vectorstore

def run_query(query):
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Define persist_directory for Chroma
    
    # Check if we already have a persisted database
    if os.path.exists(DB_PERSIST_DIR):
        # Load existing vectorstore
        print("Loading existing db")
        vectorstore = Chroma(
            persist_directory=DB_PERSIST_DIR,
            embedding_function=OpenAIEmbeddings()
        )
    else:
        # Create new vectorstore if it doesn't exist
        print("Creating new db")
        vectorstore = load_db()

    print("Prompting")
    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    prompt.messages[0].prompt.template = "You are an assistant for information retrieval tasks related to the University of New Mexico. Use the following pieces of retrieved context to respond to the prompt. Only include true information. Use three sentences maximum and keep the answer concise. Include relevant links in your answer.\nPrompt: {question} \nContext: {context} \nAnswer:"

    def format_docs(docs):
        return "\n\n".join(doc.page_content.strip() for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = rag_chain.invoke(query)
    print(response)

if __name__ == "__main__":
    # load_db()
    while True:
        query = input("Enter your query: ")
        run_query(query)