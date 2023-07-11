import sys
from antlr4 import *
from lexer.grammarLinguagemLAVisitor import grammarLinguagemLAVisitor
from lexer.grammarLinguagemLAParser import grammarLinguagemLAParser
from sym_table import SymTable

class AlgumaSemantico(grammarLinguagemLAVisitor) :
    def __init__(self):
        self.sym_table = SymTable()
        self.errors = []

    # Visit a parse tree produced by grammarLinguagemLAParser#variavel.
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

    # Visit a parse tree produced by grammarLinguagemLAParser#cmdleia.
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

    # Visit a parse tree produced by grammarLinguagemLAParser#cmdatribuicao.
    def visitCmdatribuicao(self, ctx:grammarLinguagemLAParser.CmdatribuicaoContext):
        try:
            self.sym_table.command_attr(ctx)
        except Exception as e:
            self.errors.append({
                "message": str(e),
                "line": ctx.start.line
                })
        return self.visitChildren(ctx)

    # Visit a parse tree produced by grammarLinguagemLAParser#exp_aritmetica.
    def visitExp_aritmetica(self, ctx:grammarLinguagemLAParser.Exp_aritmeticaContext):
        try:
            self.sym_table.verify_exp_aritmetica(ctx.termo())
        except Exception as e:
            self.errors.append({
                "message": str(e),
                "line": ctx.start.line
                })
        return self.visitChildren(ctx)
