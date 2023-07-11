from enum import Enum

class VarTypes(Enum):
    literal = 1
    inteiro = 2
    real = 3
    logico = 4

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

    def verify_parcela(self, parcela, ret):
        if hasattr(parcela, "expressao") and parcela.expressao() is not None:
            self.verify_exp_aritmetica(parcela.expressao(), ret)
        if hasattr(parcela, "exp_relacional") and parcela.exp_relacional() is not None:
            return self.verify_parcela(parcela.exp_relacional(), ret)
        if hasattr(parcela, "exp_aritmetica") and parcela.exp_aritmetica() is not None:
            self.verify_exp_aritmetica(parcela.exp_aritmetica(), ret)
        if hasattr(parcela, "identificador") and parcela.identificador() is not None:
            return self.check_if_exists(parcela.identificador().getText())
        if hasattr(parcela, "CADEIA") and parcela.CADEIA() is not None:
            return {
                "type": VarTypes.literal.name,
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

    def verify_exp_aritmetica(self, ctx, ret={}):
        for var in ctx:
            for i in range(0,10):
                if hasattr(var, ExprTypes(i).name):
                    func = getattr(var, ExprTypes(i).name)

                    if ExprTypes(i).name == "parcela_unario" or \
                        ExprTypes(i).name == "parcela_nao_unario" or \
                        ExprTypes(i).name == "parcela_logica":

                        parcela = self.verify_parcela(func(), ret)

                        if parcela:
                            ret[parcela["name"]] = parcela

                    else:
                        self.verify_exp_aritmetica(func(), ret)
        return ret
    
    def verify_exp_logica(self, vars):
        for var in vars.values():
            if var["type"] == "op_relacional":
                return True
        return False


    def command_attr(self, ctx):
        var_dest = self.check_if_exists(ctx.identificador().getText())

        used_vars = self.verify_exp_aritmetica(ctx.expressao().termo_logico(), {})

        exp_logica = self.verify_exp_logica(used_vars)

        if exp_logica:
            if var_dest["type"] != VarTypes.logico.name:
                raise Exception(f"atribuicao nao compativel para {var_dest['name']}")
        else:
            for var in used_vars.values():
                if var["type"] != var_dest["type"]:
                    if (var["type"] == VarTypes.inteiro.name or var["type"] == VarTypes.real.name) \
                        and (var_dest["type"] == VarTypes.real.name or var_dest["type"] == VarTypes.inteiro.name):
                        continue
                    raise Exception(f"atribuicao nao compativel para {var_dest['name']}")

    def get_type(self, name):
        return self.table[name]["type"]

    def get_value(self, name):
        return self.table[name]["value"]
