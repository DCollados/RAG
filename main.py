from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app_rail.guards_input import validate_input
from app_rail.guards_output import validate_output

load_dotenv()
CAMINHO_DB = 'db'

prompt_template = """  
Responda a pergunta do usuário:
{pergunta}

com base nessas informações abaixo:
{base_de_conhecimento}

Se a resposta não estiver clara ou não encontrar ela, responda "Não sei".
"""
# texto que passa o prompt que quero

def perguntar():
    pergunta = input("Escreva sua pergunta: ")

    if not validate_input(pergunta):
        print("Pergunta bloqueada por segurança (dados sensíveis ou tentativa de ataque).")
        return

    # carrega o banco de dados vetorizado
    funcao_embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embeddings)

    # comparar a pergunta do usuario (embedding) com o meu banco de dados
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=4)
    if len(resultados) == 0 or resultados[0][1] < 0.7: # se similaridade for menor que 0.7 nao passa    
        print("Sem informação relevante na base")
        return 
    texto_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content # concatena e pega o 1 item da tupla
        texto_resultado.append(texto) # lista com todos os textos

    base_de_conhecimento = "\n---\n".join(texto_resultado) # junta os textos com separador
    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke({"pergunta": pergunta, "base_de_conhecimento": base_de_conhecimento}) # invoca o modelo

    modelo = ChatOpenAI()
    texto_resposta = modelo.invoke(prompt).content

    if not validate_output(texto_resposta):
        print("Resposta bloqueada por conter dados sensíveis.")
        return

    print("Resposta: ", texto_resposta)

perguntar()