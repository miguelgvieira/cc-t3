import sys
from antlr4 import *
from lexer.grammarLinguagemLAVisitor import grammarLinguagemLAVisitor
from lexer.grammarLinguagemLAParser import grammarLinguagemLAParser
from sym_table import SymTable
from alguma_utils import AlgumaUtils

class AlgumaSemantico(grammarLinguagemLAVisitor) :
    def __init__(self):
        self.sym_table = SymTable()
        self.errors = []
        self.utils = AlgumaUtils(self.sym_table)

    # Modificamos o método visitVariavel para verificar se a declaração
    # de variável é válida. Conferimos se a variável já existe e se seu tipo
    # é válido
    def visitVariavel(self, ctx:grammarLinguagemLAParser.VariavelContext):
        for id in ctx.identificador():
            try:
                self.sym_table.add(id.getText(), ctx.tipo().getText())
            except Exception as e:
                self.errors.append({
                    "message": str(e),
                    "line": id.start.line
                    })
        return self.visitChildren(ctx)

    # Modificamos o método visitCmdleia para verificar se a leitura
    # é válida. No caso, verificamos se a variável já foi declarada.
    def visitCmdleia(self, ctx:grammarLinguagemLAParser.CmdleiaContext):
        for id in ctx.identificador():
            try:
                self.sym_table.check_if_exists(id.getText())
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
