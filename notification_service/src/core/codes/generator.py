import secrets


class CodeGenerator:
    def __init__(self, alphabet: str, length: int):
        self.__alphabet = alphabet
        self.__length = length

    
    def generate_code(self) -> str:
        return ''.join(secrets.choice(self.__alphabet) for _ in range(self.__length))