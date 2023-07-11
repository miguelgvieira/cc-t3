# Generated from grammarLinguagemLA.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .grammarLinguagemLAParser import grammarLinguagemLAParser
else:
    from grammarLinguagemLAParser import grammarLinguagemLAParser

# This class defines a complete generic visitor for a parse tree produced by grammarLinguagemLAParser.

class grammarLinguagemLAVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by grammarLinguagemLAParser#programa.
    def visitPrograma(self, ctx:grammarLinguagemLAParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#declaracoes.
    def visitDeclaracoes(self, ctx:grammarLinguagemLAParser.DeclaracoesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#decl_local_global.
    def visitDecl_local_global(self, ctx:grammarLinguagemLAParser.Decl_local_globalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#declaracao_local.
    def visitDeclaracao_local(self, ctx:grammarLinguagemLAParser.Declaracao_localContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#variavel.
    def visitVariavel(self, ctx:grammarLinguagemLAParser.VariavelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#identificador.
    def visitIdentificador(self, ctx:grammarLinguagemLAParser.IdentificadorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#dimensao.
    def visitDimensao(self, ctx:grammarLinguagemLAParser.DimensaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#tipo.
    def visitTipo(self, ctx:grammarLinguagemLAParser.TipoContext):
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parametro.
    def visitParametro(self, ctx:grammarLinguagemLAParser.ParametroContext):
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdescreva.
    def visitCmdescreva(self, ctx:grammarLinguagemLAParser.CmdescrevaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdse.
    def visitCmdse(self, ctx:grammarLinguagemLAParser.CmdseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdcaso.
    def visitCmdcaso(self, ctx:grammarLinguagemLAParser.CmdcasoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdpara.
    def visitCmdpara(self, ctx:grammarLinguagemLAParser.CmdparaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdenquanto.
    def visitCmdenquanto(self, ctx:grammarLinguagemLAParser.CmdenquantoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdfaca.
    def visitCmdfaca(self, ctx:grammarLinguagemLAParser.CmdfacaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdatribuicao.
    def visitCmdatribuicao(self, ctx:grammarLinguagemLAParser.CmdatribuicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdchamada.
    def visitCmdchamada(self, ctx:grammarLinguagemLAParser.CmdchamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#cmdretorno.
    def visitCmdretorno(self, ctx:grammarLinguagemLAParser.CmdretornoContext):
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
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parcela_nao_unario.
    def visitParcela_nao_unario(self, ctx:grammarLinguagemLAParser.Parcela_nao_unarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#exp_relacional.
    def visitExp_relacional(self, ctx:grammarLinguagemLAParser.Exp_relacionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op_relacional.
    def visitOp_relacional(self, ctx:grammarLinguagemLAParser.Op_relacionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#expressao.
    def visitExpressao(self, ctx:grammarLinguagemLAParser.ExpressaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#termo_logico.
    def visitTermo_logico(self, ctx:grammarLinguagemLAParser.Termo_logicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#fator_logico.
    def visitFator_logico(self, ctx:grammarLinguagemLAParser.Fator_logicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#parcela_logica.
    def visitParcela_logica(self, ctx:grammarLinguagemLAParser.Parcela_logicaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op_logico_1.
    def visitOp_logico_1(self, ctx:grammarLinguagemLAParser.Op_logico_1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by grammarLinguagemLAParser#op_logico_2.
    def visitOp_logico_2(self, ctx:grammarLinguagemLAParser.Op_logico_2Context):
        return self.visitChildren(ctx)



del grammarLinguagemLAParser