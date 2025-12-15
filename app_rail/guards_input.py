import re

# padrões perigosos
PROMPT_INJECTION_PATTERNS = [
    r"ignore .*instructions",
    r"forget .*instructions",
    r"disregard .*rules",
    r"system prompt",
    r"developer mode",
    r"act as",
    r"jailbreak",
]

SQL_INJECTION_PATTERNS = [
    r"select .* from",
    r"insert into",
    r"delete from",
    r"update .* set",
    r"drop table",
    r"--",
    r";--",
    r"' or '1'='1",
]

def validate_input(text: str) -> bool:
    """
    Retorna False se detectar tentativa de ataque.
    """
    text_lower = text.lower()

    # prompt injection
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return False

    # sql injection
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return False

    if len(text) > 2000:
        return False

    return True
