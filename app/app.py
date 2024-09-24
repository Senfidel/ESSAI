import streamlit as st
import pandas as pd
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document

# Charger les données à partir d'un fichier CSV
df = pd.read_csv('/Users/etienne/Documents/Mémoire/countinents_topics.csv')

# Initialiser le splitter avec une taille de segment de 1000 caractères et un chevauchement de 200 caractères
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Appliquer le text splitter sur la colonne contenant le texte
df['splits'] = df['Résumé_translated'].apply(lambda x: text_splitter.split_text(x))

# Flatten the list of lists in 'splits' column and include additional metadata
documents = []
for idx, row in df.iterrows():
    for split in row['splits']:
        metadata = {
            "author": row["Auteurs"],
            "title": row["Titre"],
            "country": row["Countries"],
        }
        documents.append(Document(page_content=split, metadata=metadata))

# Create Ollama embeddings
embeddings = OllamaEmbeddings(model="llama3")

# Create vector store
vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)

# Define the LLM query function
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

# Define document retrieval and formatting functions
retriever = vectorstore.as_retriever()

def combine_docs(docs):
    combined_text = ""
    for doc in docs:
        metadata = doc.metadata
        combined_text += f"Author: {metadata['author']}\nTitle: {metadata['title']}\nCountry: {metadata['country']}\n\n{doc.page_content}\n\n---\n\n"
    return combined_text

def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = combine_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

# Streamlit Interface
st.title("Question Answering avec Chroma et Ollama")

question = st.text_input("Posez une question :")

if st.button("Obtenir une réponse"):
    if question:
        result = rag_chain(question)
        st.write(f"**Question :** {question}")
        st.write(f"**Réponse :** {result}")
    else:
        st.warning("Veuillez poser une question.")
