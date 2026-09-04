from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledgebase"

CHROMA_DIR = PROJECT_ROOT / "database" / "chroma_incidents"

COLLECTION_NAME = "enterprise_incident_knowledge"


# ---------------------------------------------------------
# Embedding model
# ---------------------------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ---------------------------------------------------------
# Load enterprise KB documents
# ---------------------------------------------------------

def load_knowledge_base():

    documents = []

    docx_files = list(KNOWLEDGE_BASE_DIR.glob("*.docx"))

    print(f"Found {len(docx_files)} knowledge documents.")

    for file_path in docx_files:

        print(f"Loading: {file_path.name}")

        loader = Docx2txtLoader(str(file_path))

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = file_path.name

        documents.extend(docs)

    return documents


# ---------------------------------------------------------
# Split documents into chunks
# ---------------------------------------------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} document chunks.")

    return chunks


# ---------------------------------------------------------
# Create / load Chroma vector store
# ---------------------------------------------------------

def get_vector_store():

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    # Check whether the collection already contains data.
    document_count = vector_store._collection.count()

    if document_count == 0:

        print("ChromaDB is empty. Building knowledge index...")

        documents = load_knowledge_base()

        chunks = split_documents(documents)

        if chunks:
            vector_store.add_documents(chunks)

        print(
            f"Indexed {len(chunks)} chunks into ChromaDB."
        )

    else:

        print(
            f"Existing ChromaDB index found: "
            f"{document_count} chunks."
        )

    return vector_store


# ---------------------------------------------------------
# Retrieve relevant enterprise knowledge
# ---------------------------------------------------------

def retrieve_incident_knowledge(
    incident: str,
    k: int = 4
):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        incident,
        k=k
    )

    return results


# ---------------------------------------------------------
# Standalone RAG test
# ---------------------------------------------------------

if __name__ == "__main__":

    test_incident = (
        "Payment application is returning HTTP 503 "
        "errors for multiple users."
    )

    results = retrieve_incident_knowledge(
        test_incident
    )

    print("\n========== RAG RESULTS ==========\n")

    for index, document in enumerate(results, start=1):

        print(f"Result {index}")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Content:\n{document.page_content}")
        print("\n--------------------------------\n")