import json
import os
import bs4
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from config import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

async def load_documents(loader):
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)
    return docs

def run_query(query):
    llm = ChatOpenAI(model="gpt-4o-mini")

    sites = json.load(open('site_titles_urls.json'))

	# TODO: use new sitemapper 'embedding_manifest.json' to find relevant sites for answer queries

    # Load, chunk and index the contents of the blog.
    # loader = WebBaseLoader(
    #     web_paths=[site['url'] for site in sites] + [
    #         f"{site['url']}/" + sublink for site in sites for sublink in site['sublinks']
    #     ],
    #     bs_kwargs=dict(
    #         parse_only=SoupStrainer(
    #             lambda tag, attrs: (
    #                 tag in ["p", "h1", "h2", "h3", "li", "span", "a"]
    #             )
    #         )
    #     ),
    # )
    # docs = asyncio.run(load_documents(loader))

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # splits = text_splitter.split_documents(docs)
    # vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # # Retrieve and generate using the relevant snippets of the blog.
    # retriever = vectorstore.as_retriever()
    # prompt = hub.pull("rlm/rag-prompt")

    # def format_docs(docs):
    #     print(docs)
    #     return "\n\n".join(doc.page_content.strip() for doc in docs)

    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # response = rag_chain.invoke(query)
    # print(response)

if __name__ == "__main__":
    query = input("Enter your query: ")
    run_query(query)