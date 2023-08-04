from enum import Enum

# Esse enumerável contém os tipos de variáveis válidas para nossa linguagem
class VarTypes(Enum):
    literal = 1
    inteiro = 2
    real = 3
    logico = 4
    registro = 5
    cadeia = 6

class VarNameTypes(str, Enum):
    inteiro = "int"
    real = "float"
    logico = "bool"
    literal = "char"

class ControlChars(str, Enum):
    inteiro = "%d"
    real = "%f"
    literal = "%s"

switcher_operators = {
    "=": "==",
    "<>": "!=",
    ">": ">",
    "<": "<",
    ">=": ">=",
    "<=": "<=",
    "e": "&&",
    "nao": "!",
}

# Esse enumerável contém os tipos de expressões para nossa linguagem
# Ele é utilizado para percorrer a árvore sintática e verificar a qual
# tipo de expressão cada nó pertence, para que possamos verificar mais a fundo
class ExprTypes(Enum):
    termo = 0
    fator = 1
    parcela = 2
    parcela_unario = 3
    parcela_nao_unario = 4
    exp_relacional = 5
    expressao = 6
    termo_logico = 7
    fator_logico = 8
    parcela_logica = 9

# Classe com algumas funções úteis para a análise semântica
class AlgumaUtils():
    def __init__(self, sym_table):
        self.sym_table = sym_table

    # Essa função vai olhar para os nós acima das folhas da nossa árvore sintática.
    # Se o nó for composto de uma expressão aritmética mais uma folha(identificador,
    # número, cadeia, etc), ela chama a função verify_exp_aritmetica para verificar
    # a expressão aritmética, e retorna a informação da folha. Senão apenas retorna
    # o as informações da folha
    def verify_parcela(self, parcela, ret):
        if parcela is None:
            return None
        if hasattr(parcela, "expressao") and parcela.expressao() is not None:
            self.verify_exp_aritmetica(parcela.expressao(), ret)
        if hasattr(parcela, "exp_relacional") and parcela.exp_relacional() is not None:
            return self.verify_parcela(parcela.exp_relacional(), ret)
        if hasattr(parcela, "exp_aritmetica") and parcela.exp_aritmetica() is not None:
            self.verify_exp_aritmetica(parcela.exp_aritmetica(), ret)
        if hasattr(parcela, "identificador") and parcela.identificador() is not None:
            var = self.sym_table.check_if_exists(parcela.identificador().getText())
            if var:
                return var
            else:
                raise Exception(f"identificador {parcela.identificador().getText()} nao declarado")
        if hasattr(parcela, "CADEIA") and parcela.CADEIA() is not None:
            return {
                "type": VarTypes.cadeia.name,
                "value": parcela.CADEIA().getText(),
                "name": parcela.CADEIA().getText()
            }
        if hasattr(parcela, "NUM_INT") and parcela.NUM_INT() is not None:
            return {
                "type": VarTypes.inteiro.name,
                "value": parcela.NUM_INT().getText(),
                "name": f"int{len(ret.keys())}"
            }
        if hasattr(parcela, "NUM_REAL") and parcela.NUM_REAL() is not None:
            return {
                "type": VarTypes.real.name,
                "value": parcela.NUM_REAL().getText(),
                "name": f"real{len(ret.keys())}"
            }
        if hasattr(parcela, "op_relacional") and parcela.op_relacional() is not None:
            return {
                "type": "op_relacional",
                "value": parcela.op_relacional().getText(),
                "name": f"op{len(ret.keys())}"
            }
        if hasattr(parcela, "getText") and (parcela.getText() == "verdadeiro" \
                or parcela.getText() == "falso"):
            return {
                "type": "logico",
                "value": parcela.getText(),
                "name": f"op{len(ret.keys())}"
            }

    # Verificamos se a expressão aritmética é válida. No caso, percorremos
    # a expressão usando o método depth-first search e verificamos se cada
    # variável existe na tabela de símbolos. Se não existir, levantamos uma
    # exceção.
    def verify_exp_aritmetica(self, ctx, ret={}):
        for var in ctx:
            for i in range(0,10):
                if hasattr(var, ExprTypes(i).name):
                    func = getattr(var, ExprTypes(i).name)

                    if ExprTypes(i).name == "parcela_unario" or \
                        ExprTypes(i).name == "parcela_nao_unario" or \
                        ExprTypes(i).name == "parcela_logica":

                        if ExprTypes(i).name == "parcela_unario":
                            if self.verify_if_function(func()):
                                continue

                        parcela = self.verify_parcela(func(), ret)

                        if parcela:
                            ret[parcela["name"]] = parcela

                    else:
                        self.verify_exp_aritmetica(func(), ret)
        return ret

    # Verificamos se a expressão possui operadores relacionais
    def verify_exp_logica(self, vars):
        for var in vars.values():
            if var["type"] == "op_relacional":
                return True
        return False

    # Verificamos se a expressão de atribuição é correta
    # Comparamos o tipo da variável de destino com o tipo da expressão
    # de origem. Se forem compatíveis, a atribuição é válida.
    # Senão levantamos uma exceção
    def command_attr(self, ctx):
        if ctx.ponteiro() is not None:
            ponteiro = "^"
        else:
            ponteiro = ""

        var_dest = self.sym_table.check_if_exists(ctx.identificador().getText())

        if var_dest is None:
            raise Exception(f"identificador {ctx.identificador().getText()} nao declarado")

        used_vars = self.verify_exp_aritmetica(ctx.expressao().termo_logico(), {})

        exp_logica = self.verify_exp_logica(used_vars)

        if exp_logica:
            if var_dest["type"] != VarTypes.logico.name:
                raise Exception(f"atribuicao nao compativel para {ponteiro}{ctx.identificador().getText()}")
        else:
            for var in used_vars.values():
                comparacao_cadeia = [VarTypes.cadeia.name, VarTypes.literal.name]
                comparacao_numeral = [VarTypes.inteiro.name, VarTypes.real.name]
                if var["type"] != var_dest["type"]:
                    if var_dest["type"] in comparacao_numeral and var["type"] in comparacao_numeral:
                        continue
                    if var_dest["type"] in comparacao_cadeia and var["type"] in comparacao_cadeia:
                        continue
                    raise Exception(f"atribuicao nao compativel para {ponteiro}{ctx.identificador().getText()}")

    # Verifica se um dado contexto é uma função
    def verify_if_function(self, f):
        if hasattr(f, "IDENT") and f.IDENT() is not None \
            and hasattr(f, "expressao") and f.expressao() is not None:
            return self.call_function(f)

    # Faz uma "chamada" de função. Verifica se os parâmetros recebidos são válidos,
    # o número de parâmetros, tipo de parâmetros.
    def call_function(self, fun):
        name = fun.IDENT()
        params = fun.expressao()
        function = self.sym_table.functions[name.getText()]
        if len(params) != len(function["params"]):
            raise Exception(f"incompatibilidade de parametros na chamada de {name.getText()}")
        for i in range(len(params)):
            param_name = list(function["params"].keys())[i]
            called_name = params[i].getText().split("[")[0]

            if self.sym_table.check_if_exists(called_name):
                if self.sym_table.get_type(name=called_name) \
                    != function["params"][param_name]["type"]:
                    raise Exception(f"incompatibilidade de parametros na chamada de {name.getText()}")
            else:
                if "(" in called_name:
                    possible_function = called_name.split("(")[0]
                    if possible_function in self.sym_table.functions.keys():
                        if self.sym_table.functions[possible_function]["return_type"] \
                            != function["params"][param_name]["type"]:
                            raise Exception(f"incompatibilidade de parametros na chamada de {name.getText()}")
                if hasattr(params[i], "termo_logico") and params[i].termo_logico() is not None:
                    self.verify_exp_aritmetica(params[i].termo_logico())
                return function

        return function

    # Função que valida se um retorno está declarado num local correto.
    def validate_retorne(self):
        if self.sym_table.context != 'global':
            function_context = self.sym_table.get_function_context()
            if function_context["return_type"] is None:
                raise Exception("comando retorne nao permitido nesse escopo")
        else:
            raise Exception("comando retorne nao permitido nesse escopo")
