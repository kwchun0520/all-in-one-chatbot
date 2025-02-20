import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader,DirectoryLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings


class Chatbot:
    def __init__(self) -> None:
        self.rag_chain = None

    def create_engine_from_url(self, url:str)-> None:
      
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        # Load, chunk and index the contents of the blog.
        loader = WebBaseLoader(
            web_paths=(f"{url}",),
            # bs_kwargs=dict(
            #     parse_only=bs4.SoupStrainer(
            #         class_=("post-content", "post-title", "post-header")
            #     )
            # ),
        )
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")


        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )


    def create_engine_from_file(self, files:list)-> None:
      
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        # Load, chunk and index the contents of the blog.
        for file in files:
            with open(f"/tmp/{file.name}", "wb") as f:
                f.write(file.getvalue())
        loader = DirectoryLoader("/tmp/")
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")


        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def chat(self, input:str)->str:
        return self.rag_chain.invoke(f"{input}")
