import streamlit as st
import pandas as pd
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document

# Charger les données à partir d'un fichier CSV
try:
    df = pd.read_csv('/Users/etienne/Documents/Mémoire/countinents_topics.csv')
except FileNotFoundError:
    st.error("Le fichier CSV est introuvable. Vérifiez le chemin du fichier.")
    st.stop()

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

# Créer les embeddings Ollama
embeddings = OllamaEmbeddings(model="llama3")

# Créer le vector store
try:
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
except Exception as e:
    st.error(f"Erreur lors de la création du vector store : {e}")
    st.stop()

# Fonction pour interroger le modèle LLM
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    try:
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
        return response['message']['content']
    except Exception as e:
        st.error(f"Erreur lors de la génération de la réponse : {e}")
        return None

# Fonction pour combiner les documents récupérés
def combine_docs(docs):
    combined_text = ""
    for doc in docs:
        metadata = doc.metadata
        combined_text += f"Author: {metadata['author']}\nTitle: {metadata['title']}\nCountry: {metadata['country']}\n\n{doc.page_content}\n\n---\n\n"
    return combined_text

# Fonction principale de la chaîne RAG (Retrieval-Augmented Generation)
def rag_chain(question):
    try:
        retrieved_docs = retriever.invoke(question)
        formatted_context = combine_docs(retrieved_docs)
        return ollama_llm(question, formatted_context)
    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la chaîne RAG : {e}")
        return None

# Interface utilisateur Streamlit
st.title("Question Answering avec Chroma et Ollama")

question = st.text_input("Posez une question :")

if st.button("Obtenir une réponse"):
    if question:
        result = rag_chain(question)
        if result:
            st.write(f"**Question :** {question}")
            st.write(f"**Réponse :** {result}")
        else:
            st.warning("Aucune réponse n'a été générée.")
    else:
        st.warning("Veuillez poser une question.")
