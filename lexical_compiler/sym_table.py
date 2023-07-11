from alguma_utils import VarTypes

"""
    Classe para nossa tabela de símbolos

    Nossa tabela de símbolos consiste de um dicionário, onde a chave é o nome
    da variável e o valor é um dicionário com as informações da variável.

    Salvamos 3 informações de cada variável:
    - type: tipo da variável
    - value: valor da variável
    - name: nome da variável
"""

class SymTable():
    def __init__(self):
        self.table = {}

    def add(self, name, var_type, value=None):
        if name in self.table:
            raise Exception(f"identificador {name} ja declarado anteriormente")

        self.table[name] = {
            "type": var_type,
            "value": value,
            "name": name
        }

        if var_type not in VarTypes.__members__:
            raise Exception(f"tipo {var_type} nao declarado")

    def check_if_exists(self, name):
        if name not in self.table.keys():
            raise Exception(f"identificador {name} nao declarado")
        return self.table[name]

    def get_type(self, name):
        return self.table[name]["type"]

    def get_value(self, name):
        return self.table[name]["value"]
