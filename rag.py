import os
import asyncio
from langchain import hub
from langchain_chroma import Chroma
# from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import JSONLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from config import OPENAI_API_KEY
from datetime import datetime, timedelta
import uuid
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

DB_PERSIST_DIR = "./chroma_db"

async def load_documents(loader):
    docs = []
    async for doc in loader.alazy_load():
        docs.append(doc)
    return docs

def load_db():
    """
    WARNING: This is an expensive operation.
    
    Load the database from the JSON file, split the documents into chunks, embed them using OpenAI embeddings, 
    and persist the vectorstore to disk.

    Returns:
        vectorstore (Chroma): The vectorstore containing the embedded documents.
    """
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


session_store = {}
session_timestamps = {}  # Track when sessions were last used
SESSION_TIMEOUT = timedelta(minutes=5)  # Adjust timeout as needed

def cleanup_old_sessions():
    """Remove sessions that haven't been used for longer than SESSION_TIMEOUT"""
    current_time = datetime.now()
    expired_sessions = [
        session_id for session_id, timestamp in session_timestamps.items()
        if current_time - timestamp > SESSION_TIMEOUT
    ]
    for session_id in expired_sessions:
        del session_store[session_id]
        del session_timestamps[session_id]

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    cleanup_old_sessions()
    if not session_id or session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    session_timestamps[session_id] = datetime.now()
    return session_store[session_id]

def run_query(query, session_id):
    cleanup_old_sessions()
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Check if we already have a persisted database
    if os.path.exists(DB_PERSIST_DIR):
        print("Loading existing db")
        vectorstore = Chroma(
            persist_directory=DB_PERSIST_DIR,
            embedding_function=OpenAIEmbeddings()
        )
    else:
        print("Creating new db")
        vectorstore = load_db()

    print("Prompting")
    retriever = vectorstore.as_retriever()

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    
    qa_system_prompt = """You are an assistant for information retrieval tasks related to the University of New Mexico. \
    Your requirements for your answer are: Use the following pieces of retrieved context to respond to the prompt. \
    Keep the answer concise. Use strictly HTML formatting in your answer. \
    Include relevant links in your answer.\nContext: {context}"""
    # prompt = hub.pull("rlm/rag-prompt")
    # prompt.messages[0].prompt.template = prompt_text
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    # def format_docs(docs):
    #     return "\n\n".join(doc.page_content.strip() for doc in docs)

    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(session_id and history_aware_retriever or retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda: get_session_history(session_id) if session_id else ChatMessageHistory(),
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    # Invoke the chain with session_id for chat history
    response = conversational_rag_chain.invoke(
        {"input": query},
        config={"configurable": {"session_id": session_id}}
    )
    
    if not session_id:
        session_id = str(uuid.uuid4())
    history = get_session_history(session_id)
    history.add_user_message(query)
    history.add_ai_message(response["answer"])

    return response["answer"], session_id

if __name__ == "__main__":
    # load_db()
    while True:
        query = input("Enter your query: ")
        session_id = input("Enter session ID: ")
        print(run_query(query))