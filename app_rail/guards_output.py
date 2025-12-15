import re

PII_PATTERNS = [
    r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",   # CPF
    r"\b\d{16}\b",                     # cartão
    r"\b\d{3}-\d{2}-\d{4}\b",          # SSN
]

# respostas proibidas
FORBIDDEN_OUTPUT = [
    "como hackear",
    "como invadir",
    "burlar sistema",
    "quebrar senha",
]

def validate_output(text: str) -> bool:
    """
    Retorna False se a resposta for perigosa.
    """
    text_lower = text.lower()

    # dados sensíveis
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            return False

    # conteúdo proibido
    for phrase in FORBIDDEN_OUTPUT:
        if phrase in text_lower:
            return False

    return True
