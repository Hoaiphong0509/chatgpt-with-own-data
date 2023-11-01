import os
import sys

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

import constants as constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

# CHAT DEFAULT WITH MOCK DATA (MIO)
def chat_default(query):
    # Initialize the conversational retrieval chain
    def initialize_chain():
        if PERSIST and os.path.exists("persist"):
            print("Reusing index...\n")
            vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
            index = VectorStoreIndexWrapper(vectorstore=vectorstore)
        else:
            app_dir = os.getcwd() + "\\app"
            mock_path = app_dir + "\\mock"
            
            # persist_path = os.path.join(current_dir, '../..', 'persist')
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # mock_data_dir = os.path.join(current_dir, '..', 'mock')
            loader = DirectoryLoader(mock_path)

            if PERSIST:
                index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
            else:
                index = VectorstoreIndexCreator().from_loaders([loader])

        result = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 4}),
        ) 
        
        return result   
    
    chain = initialize_chain()
    chat_history = []
    
    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))
    return result['answer']

# CHAT WITH PERSIST DATA
def chat(query):
    os.environ["OPENAI_API_KEY"] = constants.APIKEY
    
    app_dir = os.getcwd() + "\\app"
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # persist_path = os.path.join(current_dir, '../..', 'persist')
    
    persist_path = app_dir + "\\persist" 
    index = VectorstoreIndexCreator().from_persistent_index(path=persist_path)

    chain = ConversationalRetrievalChain.from_llm(
        llm = ChatOpenAI(model="gpt-3.5-turbo"),
        retriever = index.vectorstore.as_retriever(search_kwargs={"k": 4}),
    )

    chat_history = []

    result = chain({"question": query, "chat_history": chat_history})

    return result['answer']