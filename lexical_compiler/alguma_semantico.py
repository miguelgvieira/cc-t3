import sys
from antlr4 import *
from lexer.grammarLinguagemLAVisitor import grammarLinguagemLAVisitor
from lexer.grammarLinguagemLAParser import grammarLinguagemLAParser
from sym_table import SymTable
from alguma_utils import AlgumaUtils

import json

def print_dict(variavel):
    print(json.dumps(variavel, indent=2))

class AlgumaSemantico(grammarLinguagemLAVisitor) :
    def __init__(self):
        self.sym_table = SymTable()
        self.errors = []
        self.utils = AlgumaUtils(self.sym_table)

    # Modificamos o método visitVariavel para verificar se a declaração
    # de variável é válida. Conferimos se a variável já existe e se seu tipo
    # é válido
    # def visitVariavel(self, ctx:grammarLinguagemLAParser.VariavelContext):
    def visitDeclaracao_local(self, ctx:grammarLinguagemLAParser.Declaracao_localContext):
        if hasattr(ctx, "variavel") and ctx.variavel() is not None:
            ctx = ctx.variavel()
            for id in ctx.identificador():
                try:
                    self.sym_table.add_var(id.getText(), ctx.tipo())
                except Exception as e:
                    self.errors.append({
                        "message": str(e),
                        "line": ctx.start.line
                        })
        elif hasattr(ctx, "tipo") and ctx.tipo() is not None:
            try:
                self.sym_table.add_type(ctx.IDENT().getText(), ctx.tipo())
            except Exception as e:
                self.errors.append({
                    "message": str(e),
                    "line": ctx.start.line
                    })
        elif hasattr(ctx, "valor_constante") and ctx.valor_constante() is not None:
            try:
                self.sym_table.add_var(
                    ctx.IDENT().getText(),
                    ctx.tipo_basico(),
                    ctx.valor_constante().getText(),
                    is_const=True
                )
            except Exception as e:
                self.errors.append({
                    "message": str(e),
                    "line": ctx.start.line
                    })
                
        print_dict(self.sym_table.table)
        return self.visitChildren(ctx)

    def visitDeclaracao_global(self, ctx:grammarLinguagemLAParser.Declaracao_globalContext):
        try:
            if hasattr(ctx, "tipo_estendido") and ctx.tipo_estendido() is not None:
                self.sym_table.add_function(ctx.IDENT().getText(), ctx.parametros(),\
                                         ctx.tipo_estendido().getText())
            elif hasattr(ctx, "parametros") and ctx.parametros() is not None:
                self.sym_table.add_function(ctx.IDENT().getText(), ctx.parametros())
        except Exception as e:
            self.errors.append({
                "message": str(e),
                "line": ctx.start.line
                })

        self.sym_table.context = 'local'
        self.sym_table.function_name = ctx.IDENT().getText()

        return_value = self.visitChildren(ctx)

        self.sym_table.context = 'global'
        self.sym_table.function_name = ''

        return return_value

    # Modificamos o método visitCmdleia para verificar se a leitura
    # é válida. No caso, verificamos se a variável já foi declarada.
    def visitCmdleia(self, ctx:grammarLinguagemLAParser.CmdleiaContext):
        for id in ctx.identificador():
            try:
                if not self.sym_table.check_if_exists(id.getText()):
                    raise Exception(f"identificador {id.getText()} nao declarado")
            except Exception as e:
                self.errors.append({
                    "message": str(e),
                    "line": ctx.start.line
                    })
        return self.visitChildren(ctx)

    # Modificamos o método visitCmdatribuicao para verificar se a atribuição
    # é válida.
    def visitCmdatribuicao(self, ctx:grammarLinguagemLAParser.CmdatribuicaoContext):
        try:
            self.utils.command_attr(ctx)
        except Exception as e:
            self.errors.append({
                "message": str(e),
                "line": ctx.start.line
                })
        return self.visitChildren(ctx)

    # Modificamos o método visitExp_aritmetica para verificar se a expressão
    # aritmética é válida.
    def visitExp_aritmetica(self, ctx:grammarLinguagemLAParser.Exp_aritmeticaContext):
        try:
            self.utils.verify_exp_aritmetica(ctx.termo())
        except Exception as e:
            self.errors.append({
                "message": str(e),
                "line": ctx.start.line
                })
        return self.visitChildren(ctx)

    # Visit a parse tree produced by grammarLinguagemLAParser#cmdretorno.
    def visitCmdretorno(self, ctx:grammarLinguagemLAParser.CmdretornoContext):
        try:
            self.utils.validate_retorne()
        except Exception as e:
            self.errors.append({
                "message": str(e),
                "line": ctx.start.line
                })
        return self.visitChildren(ctx)