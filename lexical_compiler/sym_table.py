from alguma_utils import VarTypes
import json

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
        self.new_types = {}
        self.functions = {}
        self.context = 'global'
        self.function_name = ''

    def check_if_identificador_exists(self, name):
        if name in self.table.keys() or name in self.new_types.keys() or name in self.functions.keys():
            return True
        return False

    def check_if_tipo_exists(self, name):
        if name not in VarTypes.__members__ and name not in self.new_types.keys():
            raise Exception(f"tipo {name} nao declarado")
    
    def check_if_ponteiro(self, var_type):
        if "^" in var_type:
            return True
        return False

    def handle_registro(self, registro):
        registro_dict = {}
        for var in registro.variavel():
            for i in var.identificador():
                registro_dict[i.getText()] = {
                    "type": var.tipo().getText(),
                    "value": None,
                    "name": i.getText(),
                    "ponteiro": self.check_if_ponteiro(var.tipo().getText())
                }
        return registro_dict

    def add_function(self, name, parametros, return_type=None):
        if self.check_if_identificador_exists(name):
            raise Exception(f"identificador {name} ja declarada anteriormente")

        if return_type:
            self.check_if_tipo_exists(return_type)

        parametros_table = {}

        for params in parametros.parametro():
            param_type = params.tipo_estendido().getText()
            for parametro in params.identificador():
                var_type = param_type

                value = None

                param_name = parametro.getText()

                self.check_if_tipo_exists(param_type)


                for new_type in self.new_types.keys():
                    if new_type == param_type:
                        value = self.new_types[new_type]["value"].copy()
                        var_type = self.new_types[new_type]["type"]

                parametros_table[param_name] = {
                    "type": var_type,
                    "value": value,
                    "name": param_name,
                    "ponteiro": self.check_if_ponteiro(param_type)
                }

        self.functions[name] = {
            "params": parametros_table,
            "return_type": return_type,
            "name": name
        }

    def add_type(self, name, complement):
        if self.check_if_identificador_exists(name):
            raise Exception(f"identificador {name} ja declarado anteriormente")

        if hasattr(complement, "registro") and complement.registro() is not None:
            self.new_types[name] = {
                'value': self.handle_registro(complement.registro()),
                'type': 'registro',
                'name': name
            }
    
    def check_if_vetor(self, name):
        if "[" in name:
            return name.split("[")[1].split("]")[0], name.split("[")[0]
        return None, name

    def add_var(self, name, complement, value=None, is_const=False):
        if self.context == "global":
            existing_vars = self.table.copy()
        else:
            existing_vars = self.functions[self.function_name]["params"]

        if self.check_if_identificador_exists(name):
            raise Exception(f"identificador {name} ja declarado anteriormente")

        var_type = complement.getText().replace("^", "", 1)

        if hasattr(complement, "registro") and complement.registro() is not None:
            var_type = VarTypes.registro.name
            value = self.handle_registro(complement.registro())

        # verifica se é um tipo novo, criado no programa
        for new_type in self.new_types.keys():
            if new_type == var_type:
                value = self.new_types[new_type]["value"].copy()
                var_type = self.new_types[new_type]["type"]

        is_ponteiro = self.check_if_ponteiro(complement.getText())

        vetor, name = self.check_if_vetor(name)

        existing_vars[name] = {
            "type": var_type,
            "value": value,
            "name": name,
            "ponteiro": is_ponteiro,
            "vetor": vetor,
            "constante": is_const
        }

        if self.check_if_tipo_exists(var_type):
            raise Exception(f"tipo {var_type} nao declarado")

        if self.context == "global":
            self.table = existing_vars
        else:
            self.functions[self.function_name]["params"] = existing_vars

    def check_if_exists(self, name):
        if self.context == 'local':
            found_var = self.functions[self.function_name]["params"].copy()
        else:
            found_var = self.table.copy()

        vetor, name = self.check_if_vetor(name)

        if "." in name:
            for var in name.split("."):
                if var not in found_var.keys():
                    return False

                if found_var[var]["type"] == VarTypes.registro.name:
                    found_var = found_var[var]["value"]
                else:
                    found_var = found_var[var]
        else:
            if name not in found_var.keys():
                return None

            found_var = found_var[name]

        return found_var

    def get_type(self, value=None, name=None):
        if name:
            return self.check_if_exists(name)["type"]
        else:
            return type(value)

    def get_value(self, name):
        return self.table[name]["value"]

    def get_function_context(self):
        return self.functions[self.function_name]