from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load CSV data
loader = CSVLoader('data/transformed_gppd_data.csv', encoding="utf-8")
data = loader.load()

# Split text into chunks
rc_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=60, separators=['.'])
docs = rc_splitter.split_documents(data)


# Compute embeddings and persist them
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

vectorstore = Chroma.from_documents(
    docs, embedding=embedding_function, persist_directory="chroma_db"
)

print("Vectorstore created and saved!")
