# Generated from grammarLinguagemLA.g4 by ANTLR 4.13.0
from antlr4 import *
from lexer.grammarLinguagemLAParser import grammarLinguagemLAParser
from alguma_utils import VarTypes
from alguma_utils import VarNameTypes
from alguma_utils import ControlChars
from alguma_utils import AlgumaUtils
from alguma_utils import switcher_operators

class AlgumaGeradorC(ParseTreeVisitor):
    def __init__(self, sym_table):
        self.sym_table = sym_table
        self.code = []
        self.headers = []
        self.indent = 0
        self.utils = AlgumaUtils(self.sym_table)
        self.line = ""
        self.vars = {}
    
    def indent_line(self):
        indent = ""
        for i in range(self.indent):
            indent += "\t"
        return indent

    def add_line(self, code_line):
        indent = self.indent_line()
        self.code.append(f"{indent}{code_line}")
    
    def add_headers(self, code_line):
        if code_line not in self.headers:
            self.headers.append(code_line)
    
    def change_context(self, new_context):
        if new_context != "global":
            self.sym_table.context = "local"
            self.sym_table.function_name = new_context
        else:
            self.sym_table.context = "global"
            self.sym_table.function_name = ""

    # Visit a parse tree produced by grammarLinguagemLAParser#programa.
    def visitPrograma(self, ctx:grammarLinguagemLAParser.ProgramaContext):
        self.add_headers("#include <stdio.h>")
        self.add_headers("#include <stdlib.h>")

        self.visitDeclaracoes(ctx.declaracoes())

        self.add_line("\nint main() {")
        self.indent += 1

        self.visitCorpo(ctx.corpo())

        self.add_line("return 0;")
        self.indent -= 1
        self.add_line("}")

        return None


    # Visit a parse tree produced by grammarLinguagemLAParser#declaracoes.
    def visitDeclaracoes(self, ctx:grammarLinguagemLAParser.DeclaracoesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#decl_local_global.
    def visitDecl_local_global(self, ctx:grammarLinguagemLAParser.Decl_local_globalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#declaracao_local.
    def visitDeclaracao_local(self, ctx:grammarLinguagemLAParser.Declaracao_localContext):
        if hasattr(ctx, "variavel") and ctx.variavel() is not None:
            pass
        elif hasattr(ctx, "tipo") and ctx.tipo() is not None:
            self.add_line("typedef struct {")
            self.indent += 1
            self.visitTipo(ctx.tipo())
            self.indent -= 1
            self.add_line(f"}} {ctx.IDENT().getText()};")
            pass
        elif hasattr(ctx, "valor_constante") and ctx.valor_constante() is not None:
            self.add_line(f"#define {ctx.IDENT().getText()} {ctx.valor_constante().getText()}")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#variavel.
    def visitVariavel(self, ctx:grammarLinguagemLAParser.VariavelContext):
        self.line = ""
        ponteiro = ""
        tipo = ctx.tipo().getText()

        if "^" in tipo:
            tipo = tipo.replace("^", "")
            ponteiro = "*"

        if tipo in VarNameTypes.__members__:
            tipo = VarNameTypes[tipo].value

        for var in ctx.identificador():
            name_var = var.getText()
            if tipo == VarNameTypes.literal.value:
                self.add_line(f"{tipo}{ponteiro} {name_var}[80];")
            elif "registro" in tipo:
                self.add_line("struct {")
                self.indent += 1
                self.visitChildren(ctx.tipo())
                self.indent -= 1
                self.add_line(f"}} {name_var};")
            else:
                self.add_line(f"{tipo}{ponteiro} {name_var};")


    # Visit a parse tree produced by grammarLinguagemLAParser#identificador.
    def visitIdentificador(self, ctx:grammarLinguagemLAParser.IdentificadorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#dimensao.
    def visitDimensao(self, ctx:grammarLinguagemLAParser.DimensaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#tipo.
    def visitTipo(self, ctx:grammarLinguagemLAParser.TipoContext):
        print(ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#tipo_basico.
    def visitTipo_basico(self, ctx:grammarLinguagemLAParser.Tipo_basicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#tipo_basico_ident.
    def visitTipo_basico_ident(self, ctx:grammarLinguagemLAParser.Tipo_basico_identContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#tipo_estendido.
    def visitTipo_estendido(self, ctx:grammarLinguagemLAParser.Tipo_estendidoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#valor_constante.
    def visitValor_constante(self, ctx:grammarLinguagemLAParser.Valor_constanteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#registro.
    def visitRegistro(self, ctx:grammarLinguagemLAParser.RegistroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#declaracao_global.
    def visitDeclaracao_global(self, ctx:grammarLinguagemLAParser.Declaracao_globalContext):
        function_name = ctx.IDENT().getText()
        self.change_context(function_name)
        functio_return_value = self.sym_table.functions[self.sym_table.function_name]["return_type"]

        if functio_return_value is None:
            function_type = "void"
        else:
            function_type = VarNameTypes[functio_return_value].value
            
        self.line = ""
        self.visitParametros(ctx.parametros())
        self.add_line(f"{function_type} {function_name}({self.line}){{")
        self.line = ""
        self.indent += 1
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self.indent -= 1
        self.add_line("}")

        return None


    # Visit a parse tree produced by grammarLinguagemLAParser#parametro.
    def visitParametro(self, ctx:grammarLinguagemLAParser.ParametroContext):
        var_type = ctx.tipo_estendido().getText()
        var_type = VarNameTypes[var_type].value
        ponteiro = ""
        if var_type == VarNameTypes.literal.value:
            ponteiro = "*"
        for param in ctx.identificador():
            self.line += f"{var_type}{ponteiro} {param.getText()}"
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parametros.
    def visitParametros(self, ctx:grammarLinguagemLAParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#corpo.
    def visitCorpo(self, ctx:grammarLinguagemLAParser.CorpoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmd.
    def visitCmd(self, ctx:grammarLinguagemLAParser.CmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdleia.
    def visitCmdleia(self, ctx:grammarLinguagemLAParser.CmdleiaContext):
        for ident in ctx.identificador():
            var_type = self.sym_table.get_type(name=ident.getText())
            if var_type == VarNameTypes.literal.name:
                self.add_line(f"gets({ident.getText()});")
            else:
                self.add_line(f"scanf(\"{ControlChars[var_type].value}\", &{ident.getText()});")

        return None


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdescreva.
    def visitCmdescreva(self, ctx:grammarLinguagemLAParser.CmdescrevaContext):
        vars = []
        line = "printf(\""
        for ident in ctx.expressao():
            self.line = ""
            self.visitChildren(ident)
            expressao = self.utils.verify_exp_aritmetica([ident], {})
            keys = list(expressao.keys())
            if len(keys) > 0:
                expr_type = expressao[keys[0]]["type"]

                if expr_type == VarTypes.cadeia.name:
                    line += ident.getText().replace("\"", "")
                else:
                    if expr_type in VarNameTypes.__members__:
                        vars.append(ident.getText())
                        line += ControlChars[expr_type].value
            # Especifica que é uma expressao
            if "(" in ident.getText() and ")" in ident.getText():
                function_name = ident.getText().split("(")[0]
                return_type_function = self.sym_table.functions[function_name]["return_type"]
                self.line = ""
                self.visitChildren(ident)
                line = f"printf(\"{ControlChars[return_type_function].value}\", {self.line});"
                self.add_line(line)
                return None
        line += "\""
        for var in vars:
            line += ", " + var
        line += ");"
        self.add_line(line)
        return None


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdse.
    def visitCmdse(self, ctx:grammarLinguagemLAParser.CmdseContext):
        self.visitExpressao(ctx.expressao())
        self.add_line(f"if ({self.line}) {{")
        self.line = ""
        self.indent += 1
        self.visitCmd(ctx.cmd()[0])
        self.indent -= 1

        if "senao" in ctx.getText():
            for cmd in ctx.cmd()[1:]:
                self.add_line("} else {")
                self.indent += 1
                self.visitCmd(cmd)
                self.indent -= 1

        self.add_line("}")


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdcaso.
    def visitCmdcaso(self, ctx:grammarLinguagemLAParser.CmdcasoContext):
        self.add_line(f"switch ({ctx.exp_aritmetica().getText()}) {{")
        self.indent += 1
        for i in range(len(ctx.selecao().item_selecao())):
            self.line = "case"
            self.visitConstantes(ctx.selecao().item_selecao()[i].constantes())

            self.indent += 1
            for cmd in ctx.selecao().item_selecao()[i].cmd():
                self.visitCmd(cmd)
            self.add_line("break;")
            self.indent -= 1
        
        if "senao" in ctx.getText():
            self.add_line("default:")
            self.indent += 1
            for cmd in ctx.cmd():
                self.visitCmd(cmd)
        self.indent -= 1
        self.add_line("}")


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdpara.
    def visitCmdpara(self, ctx:grammarLinguagemLAParser.CmdparaContext):
        variable = ctx.IDENT().getText()
        init_for = ctx.exp_aritmetica()[0].getText()
        end_for = ctx.exp_aritmetica()[1].getText()
        self.add_line(f"for({variable} = {init_for}; {variable} <= {end_for}; {variable}++){{")
        self.indent += 1

        for cmd in ctx.cmd():
            self.visitCmd(cmd)

        self.indent -= 1
        self.add_line("}")

        return None


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdenquanto.
    def visitCmdenquanto(self, ctx:grammarLinguagemLAParser.CmdenquantoContext):
        self.add_line(f"while ({ctx.expressao().getText()}) {{")
        self.indent += 1
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self.indent -= 1
        self.add_line("}")


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdfaca.
    def visitCmdfaca(self, ctx:grammarLinguagemLAParser.CmdfacaContext):
        self.add_line("do {")
        self.indent += 1
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self.indent -= 1
        self.line = ""
        self.visitExpressao(ctx.expressao())
        self.add_line(f"}} while ({self.line});")


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdatribuicao.
    def visitCmdatribuicao(self, ctx:grammarLinguagemLAParser.CmdatribuicaoContext):
        ponteiro = ""

        if hasattr(ctx, "ponteiro") and ctx.ponteiro() is not None:
            ponteiro = "*"
        

        var_dest = ctx.identificador().getText()
        var_dest_type = self.sym_table.get_type(name=var_dest)
        expressao = ctx.expressao().getText()

        if var_dest_type == VarTypes.literal.name:
            self.add_headers("#include <string.h>")
            self.add_headers("#include <string.h>")
            self.add_line(f"strcpy({var_dest}, {expressao});")
        else:
            self.add_line(f"{ponteiro}{var_dest} = {expressao};")

        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdchamada.
    def visitCmdchamada(self, ctx:grammarLinguagemLAParser.CmdchamadaContext):
        self.add_line(f"{ctx.getText()};")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdretorno.
    def visitCmdretorno(self, ctx:grammarLinguagemLAParser.CmdretornoContext):
        self.add_line(f"return {ctx.expressao().getText()};")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#selecao.
    def visitSelecao(self, ctx:grammarLinguagemLAParser.SelecaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#item_selecao.
    def visitItem_selecao(self, ctx:grammarLinguagemLAParser.Item_selecaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#constantes.
    def visitConstantes(self, ctx:grammarLinguagemLAParser.ConstantesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#numero_intervalo.
    def visitNumero_intervalo(self, ctx:grammarLinguagemLAParser.Numero_intervaloContext):
        start_val = int(ctx.NUM_INT()[0].getText())
        if len(ctx.NUM_INT()) > 1:
            end_val = int(ctx.NUM_INT()[1].getText()) + 1
        else:
            end_val = start_val + 1
        for val in range(start_val, end_val):
            self.add_line(f"{self.line} {val}:")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op_unario.
    def visitOp_unario(self, ctx:grammarLinguagemLAParser.Op_unarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#exp_aritmetica.
    def visitExp_aritmetica(self, ctx:grammarLinguagemLAParser.Exp_aritmeticaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#termo.
    def visitTermo(self, ctx:grammarLinguagemLAParser.TermoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#fator.
    def visitFator(self, ctx:grammarLinguagemLAParser.FatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op1.
    def visitOp1(self, ctx:grammarLinguagemLAParser.Op1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op2.
    def visitOp2(self, ctx:grammarLinguagemLAParser.Op2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op3.
    def visitOp3(self, ctx:grammarLinguagemLAParser.Op3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parcela.
    def visitParcela(self, ctx:grammarLinguagemLAParser.ParcelaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parcela_unario.
    def visitParcela_unario(self, ctx:grammarLinguagemLAParser.Parcela_unarioContext):
        if hasattr(ctx, "NUM_INT") and ctx.NUM_INT() is not None:
            self.line += ctx.NUM_INT().getText()
        if hasattr(ctx, "identificador") and ctx.identificador() is not None:
            self.line += ctx.identificador().getText()
        if hasattr(ctx, "IDENT") and ctx.IDENT() is not None:
            self.line += f"{ctx.IDENT().getText()}("
            self.visitChildren(ctx)
            self.line += ")"
            return None
        return self.visitChildren(ctx)
            
        


    # Visit a parse tree produced by grammarLinguagemLAParser#parcela_nao_unario.
    def visitParcela_nao_unario(self, ctx:grammarLinguagemLAParser.Parcela_nao_unarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#exp_relacional.
    def visitExp_relacional(self, ctx:grammarLinguagemLAParser.Exp_relacionalContext):
        exp = ctx.exp_aritmetica()
        for i in range(len(exp[:-1])):
            self.visitExp_aritmetica(exp[i])
            if op_relacional := ctx.op_relacional():
                self.visitOp_relacional(op_relacional)
        self.visitExp_aritmetica(exp[-1])


    # Visit a parse tree produced by grammarLinguagemLAParser#op_relacional.
    def visitOp_relacional(self, ctx:grammarLinguagemLAParser.Op_relacionalContext):
        self.line += switcher_operators[ctx.getText()]
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#expressao.
    def visitExpressao(self, ctx:grammarLinguagemLAParser.ExpressaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#termo_logico.
    def visitTermo_logico(self, ctx:grammarLinguagemLAParser.Termo_logicoContext):
        for i in range(len(ctx.fator_logico()[:-1])):
            self.visitFator_logico(ctx.fator_logico()[i])
            self.visitOp_logico_2(ctx.op_logico_2()[i])
        self.visitFator_logico(ctx.fator_logico()[-1])


    # Visit a parse tree produced by grammarLinguagemLAParser#fator_logico.
    def visitFator_logico(self, ctx:grammarLinguagemLAParser.Fator_logicoContext):
        if "nao" in ctx.getText():
            self.line += "!("
            self.visitChildren(ctx)
            self.line += ")"
            return None
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parcela_logica.
    def visitParcela_logica(self, ctx:grammarLinguagemLAParser.Parcela_logicaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op_logico_1.
    def visitOp_logico_1(self, ctx:grammarLinguagemLAParser.Op_logico_1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op_logico_2.
    def visitOp_logico_2(self, ctx:grammarLinguagemLAParser.Op_logico_2Context):
        self.line += " " + switcher_operators[ctx.getText()] + " "
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#ponteiro.
    def visitPonteiro(self, ctx:grammarLinguagemLAParser.PonteiroContext):
        return self.visitChildren(ctx)



del grammarLinguagemLAParser