from langchain_community.document_loaders import PyPDFDirectoryLoader # carregar PDFs de um diretório
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

PASTA_BASE = "BASE"
load_dotenv()

def criar_db ():
    documentos = carregar_documentos()
    print(documentos)
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

def carregar_documentos():
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="**/*.pdf")
    documentos = carregador.load()
    return documentos

def dividir_chunks(documentos):

    separador_doc = RecursiveCharacterTextSplitter(
        chunk_size=3000, # tanto de caracteres em cada chunk
        chunk_overlap=500, # sobreposição entre chunks
        length_function=len,
        add_starting_indices=True # verifica os índices iniciais
    )
    chunks = separador_doc.split_documents(documentos)
    return chunks

def vetorizar_chunks(chunks):
    embeddings = OpenAIEmbeddings()
    vetor_db = Chroma.from_documents(
        documents=chunks, # lista de chunks
        embedding=embeddings,
        persist_directory="db" # diretório onde o banco de dados será salvo
    )
    vetor_db.persist() # salva o banco de dados no diretório especificado

