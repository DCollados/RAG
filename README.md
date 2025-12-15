Projeto RAG

Sistema LLM que utiliza LangChain + Chroma
Guardrail local que protege o pipeline contra SQL injection, Prompt injection etc. 
Banco de dados separados em chunks

Funcionamento
Agente recebe a resposta, verifica se passa pelo guardrail, puxa no banco de dados informações relevantes para a resposta (nos chunks), gera respostas com llm e verifica se passa no guardrail do output
