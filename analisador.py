import re
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple
import os
import sys

class TokenType(Enum):
    # Palavras reservadas
    INICIO = "als"
    TIPO_VAR = "tipo_var"
    COND_SE = "cdt"
    COND_SENAO = "!cdt"
    COND_SENAOSE = "!cdt+"
    REP_PARA = "cycle"
    REP_ENQUANTO = "during"
    REP_RANGE = "repeat"
    WRT = "wrt"
    INPUT = "input"
    FUNCTION = "function"
    NOME_FUNCAO = "funcao"
    PULAR_LINHA = "brkln"
    IN = "in"  # Palavra reservada para repeat...in
    
    # Operadores
    OPER_MATEMATICO = "oper_matematico"
    OPER_ATRIB = "op_atrib"
    OPER_LOGICO = "oper_logico"
    OP_REL = "op_rel"
    
    # Valores
    VALOR_LOGICO = "valor_logico"
    VALOR_TEXTO = "valor_texto"
    VALOR_INTEIRO = "valor_inteiro"
    VALOR_REAL = "valor_real"
    
    # Delimitadores
    ABRE_PARENT = "abre_parent"
    FECHA_PARENT = "fecha_parent"
    ABRE_COLCHETES = "abre_colchetes"
    FECHA_COLCHETES = "fecha_colchetes"
    VIRGULA = "virgula"
      # Outros
    COMENTARIO = "comentario"
    IDENTIFICADOR = "identificador"
    WHITESPACE = "whitespace"
    NEWLINE = "newline"
    EOF = "eof"
    
    # Tipos de erro léxicos
    ERRO_SIMBOLO_INVALIDO = "erro_simbolo_invalido"
    ERRO_IDENTIFICADOR_MALFORMADO = "erro_identificador_malformado"
    ERRO_IDENTIFICADOR_MUITO_LONGO = "erro_identificador_muito_longo"
    ERRO_NUMERO_MALFORMADO = "erro_numero_malformado"
    ERRO_NUMERO_MUITO_LONGO = "erro_numero_muito_longo"
    ERRO_STRING_NAO_FECHADA = "erro_string_nao_fechada"
    ERRO_COMENTARIO_NAO_FECHADO = "erro_comentario_nao_fechado"
    ERRO_PROGRAMA_SEM_INICIO = "erro_programa_sem_inicio"
    ERRO_TIPO_INCOMPATIVEL = "erro_tipo_incompativel"
    ERRO_OPERADOR_RELACIONAL_MALFORMADO = "erro_operador_relacional_malformado"
    ERRO_PALAVRA_RESERVADA_MALFORMADA = "erro_palavra_reservada_malformada"
    ERRO_OPERADOR_RELACIONAL_AUSENTE = "erro_operador_relacional_ausente"
    ERRO_INPUT_SEM_VARIAVEL = "erro_input_sem_variavel"
    ERRO_INPUT_VARIAVEL_NAO_DECLARADA = "erro_input_variavel_nao_declarada"
    ERRO_INPUT_SINTAXE_INCORRETA = "erro_input_sintaxe_incorreta"
    ERRO = "erro"

    # Tipos de erro sintático
    ERRO_SINTAXE_PROGRAMA_INCOMPLETO = "erro_sintaxe_programa_incompleto"
    ERRO_SINTAXE_PARENTESES_NAO_FECHADOS = "erro_sintaxe_parenteses_nao_fechados"
    ERRO_SINTAXE_COLCHETES_NAO_FECHADOS = "erro_sintaxe_colchetes_nao_fechados"
    ERRO_SINTAXE_COMANDO_INCOMPLETO = "erro_sintaxe_comando_incompleto"
    ERRO_SINTAXE_ESTRUTURA_CONDICIONAL_MALFORMADA = "erro_sintaxe_estrutura_condicional_malformada"
    ERRO_SINTAXE_ESTRUTURA_REPETICAO_MALFORMADA = "erro_sintaxe_estrutura_repeticao_malformada"
    ERRO_SINTAXE_EXPRESSAO_INVALIDA = "erro_sintaxe_expressao_invalida"
    ERRO_SINTAXE_DECLARACAO_VARIAVEL_INCORRETA = "erro_sintaxe_declaracao_variavel_incorreta"
    ERRO_SINTAXE_ATRIBUICAO_INCORRETA = "erro_sintaxe_atribuicao_incorreta"
    ERRO_SINTAXE_COMANDO_INPUT_MALFORMADO = "erro_sintaxe_comando_input_malformado"
    ERRO_SINTAXE_COMANDO_WRT_MALFORMADO = "erro_sintaxe_comando_wrt_malformado"
    ERRO_SINTAXE_ORDEM_INCORRETA = "erro_sintaxe_ordem_incorreta"

@dataclass
class Token:
    tipo: TokenType
    lexema: str
    linha: int
    coluna: int
    descricao: str = ""
    eh_erro: bool = False
    
    def __str__(self):
        if self.eh_erro:
            return f"Linha: {self.linha} - Coluna: {self.coluna} - ERRO: <{self.tipo.value}, {self.lexema}> - {self.descricao}"
        else:
            return f"Linha: {self.linha} - Coluna: {self.coluna} - Token: <{self.tipo.value}, {self.lexema}>"

@dataclass
class NoSintatico:
    """Representa um nó na árvore sintática."""
    tipo: str
    valor: str = ""
    filhos: List['NoSintatico'] = None
    token: Token = None
    linha: int = 0
    coluna: int = 0
    
    def __post_init__(self):
        if self.filhos is None:
            self.filhos = []
    
    def adicionar_filho(self, filho: 'NoSintatico'):
        self.filhos.append(filho)
    
    def __str__(self, nivel=0):
        indent = "  " * nivel
        resultado = f"{indent}{self.tipo}"
        if self.valor:
            resultado += f": {self.valor}"
        resultado += "\n"
        
        for filho in self.filhos:
            resultado += filho.__str__(nivel + 1)
        
        return resultado

class AnalisadorSintatico:
    """Analisador sintático para a linguagem ALAIAS."""
    
    def __init__(self):
        self.tokens = []
        self.posicao = 0
        self.erros_sintaticos = []
        self.arvore_sintatica = None
        
    def analisar(self, tokens: List[Token]) -> Tuple[Optional[NoSintatico], List[Token]]:
        """
        Analisa sintaticamente uma lista de tokens.
        Retorna a árvore sintática e lista de erros sintáticos.
        """
        # Filtra tokens não significativos para análise sintática
        self.tokens = [t for t in tokens if t.tipo not in [
            TokenType.WHITESPACE, TokenType.COMENTARIO
        ] and not t.eh_erro]
        
        self.posicao = 0
        self.erros_sintaticos = []
        
        try:
            self.arvore_sintatica = self._analisar_programa()
        except Exception as e:
            erro = Token(
                tipo=TokenType.ERRO_SINTAXE_PROGRAMA_INCOMPLETO,
                lexema="",
                linha=self._token_atual().linha if self._token_atual() else 1,
                coluna=self._token_atual().coluna if self._token_atual() else 1,
                descricao=f"Erro sintático geral: {str(e)}",
                eh_erro=True
            )
            self.erros_sintaticos.append(erro)
        
        return self.arvore_sintatica, self.erros_sintaticos
    
    def _token_atual(self) -> Optional[Token]:
        """Retorna o token atual."""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None
    
    def _avancar(self) -> Optional[Token]:
        """Avança para o próximo token e retorna o token anterior."""
        if self.posicao < len(self.tokens):
            token = self.tokens[self.posicao]
            self.posicao += 1
            return token
        return None
    
    def _verificar_token(self, tipo_esperado: TokenType) -> bool:
        """Verifica se o token atual é do tipo esperado."""
        token = self._token_atual()
        return token is not None and token.tipo == tipo_esperado
    
    def _consumir_token(self, tipo_esperado: TokenType, mensagem_erro: str = "") -> Optional[Token]:
        """Consome um token esperado ou gera erro."""
        if self._verificar_token(tipo_esperado):
            return self._avancar()
        else:
            token_atual = self._token_atual()
            if not mensagem_erro:
                mensagem_erro = f"Esperado token {tipo_esperado.value}"
            
            erro = Token(
                tipo=TokenType.ERRO_SINTAXE_COMANDO_INCOMPLETO,
                lexema=token_atual.lexema if token_atual else "EOF",
                linha=token_atual.linha if token_atual else 1,
                coluna=token_atual.coluna if token_atual else 1,
                descricao=mensagem_erro,
                eh_erro=True
            )
            self.erros_sintaticos.append(erro)
            return None
    
    def _analisar_programa(self) -> NoSintatico:
        """
        Programa -> 'als' ListaComandos
        """
        programa = NoSintatico("PROGRAMA")
        
        # Deve começar com 'als'
        if not self._consumir_token(TokenType.INICIO, "Programa deve começar com 'als'"):
            return programa
        
        # Adiciona nó para o 'als'
        no_inicio = NoSintatico("INICIO", "als")
        programa.adicionar_filho(no_inicio)
        
        # Ignora quebras de linha após 'als'
        while self._verificar_token(TokenType.NEWLINE):
            self._avancar()
        
        # Analisa lista de comandos
        lista_comandos = self._analisar_lista_comandos()
        if lista_comandos:
            programa.adicionar_filho(lista_comandos)
        
        return programa
    
    def _analisar_lista_comandos(self) -> NoSintatico:
        """
        ListaComandos -> Comando ListaComandos | ε
        """
        lista = NoSintatico("LISTA_COMANDOS")
        
        while self._token_atual() and self._token_atual().tipo != TokenType.EOF:
            # Ignora quebras de linha
            if self._verificar_token(TokenType.NEWLINE):
                self._avancar()
                continue
            
            comando = self._analisar_comando()
            if comando:
                lista.adicionar_filho(comando)
            else:
                # Se não conseguiu analisar comando, avança para evitar loop infinito
                if self._token_atual():
                    self._avancar()
        
        return lista if lista.filhos else None
    
    def _analisar_comando(self) -> Optional[NoSintatico]:
        """
        Comando -> DeclaracaoVariavel | Atribuicao | ComandoInput | ComandoOutput | 
                   EstruturaCondicional | EstruturaRepeticao | ComandoBreakLine | 
                   DeclaracaoFuncao | ChamadaFuncao
        """
        token = self._token_atual()
        if not token:
            return None
        
        if token.tipo == TokenType.TIPO_VAR:
            return self._analisar_declaracao_variavel()
        elif token.tipo == TokenType.FUNCTION:
            return self._analisar_declaracao_funcao()
        elif token.tipo == TokenType.IDENTIFICADOR:
            # Verifica se é uma chamada de função (identificador seguido de parênteses)
            if (self.posicao + 1 < len(self.tokens) and 
                self.tokens[self.posicao + 1].tipo == TokenType.ABRE_PARENT):
                return self._analisar_chamada_funcao()
            else:
                return self._analisar_atribuicao()
        elif token.tipo == TokenType.INPUT:
            return self._analisar_comando_input()
        elif token.tipo == TokenType.WRT:
            return self._analisar_comando_output()
        elif token.tipo == TokenType.COND_SE:
            return self._analisar_estrutura_condicional()
        elif token.tipo in [TokenType.REP_PARA, TokenType.REP_ENQUANTO, TokenType.REP_RANGE]:
            return self._analisar_estrutura_repeticao()
        elif token.tipo == TokenType.PULAR_LINHA:
            self._avancar()
            return NoSintatico("COMANDO_BREAKLINE", "brkln")
        else:
            # Token não reconhecido para início de comando
            erro = Token(
                tipo=TokenType.ERRO_SINTAXE_COMANDO_INCOMPLETO,
                lexema=token.lexema,
                linha=token.linha,
                coluna=token.coluna,
                descricao=f"Token inesperado '{token.lexema}' não inicia um comando válido",
                eh_erro=True
            )
            self.erros_sintaticos.append(erro)
            self._avancar()
            return None
    
    def _analisar_declaracao_variavel(self) -> NoSintatico:
        """
        DeclaracaoVariavel -> TipoVar Identificador
        """
        no = NoSintatico("DECLARACAO_VARIAVEL")
        
        # Tipo da variável
        token_tipo = self._consumir_token(TokenType.TIPO_VAR, "Esperado tipo de variável")
        if token_tipo:
            no_tipo = NoSintatico("TIPO", token_tipo.lexema, token=token_tipo)
            no.adicionar_filho(no_tipo)
        
        # Identificador
        token_id = self._consumir_token(TokenType.IDENTIFICADOR, "Esperado identificador após tipo de variável")
        if token_id:
            no_id = NoSintatico("IDENTIFICADOR", token_id.lexema, token=token_id)
            no.adicionar_filho(no_id)
        
        return no
    
    def _analisar_atribuicao(self) -> NoSintatico:
        """
        Atribuicao -> Identificador '<=' Expressao
        """
        no = NoSintatico("ATRIBUICAO")
        
        # Identificador
        token_id = self._consumir_token(TokenType.IDENTIFICADOR, "Esperado identificador")
        if token_id:
            no_id = NoSintatico("IDENTIFICADOR", token_id.lexema, token=token_id)
            no.adicionar_filho(no_id)
        
        # Operador de atribuição
        if not self._consumir_token(TokenType.OPER_ATRIB, "Esperado operador de atribuição '<='"):
            return no
        
        no_op = NoSintatico("OPERADOR_ATRIBUICAO", "<=")
        no.adicionar_filho(no_op)
        
        # Expressão
        expressao = self._analisar_expressao()
        if expressao:
            no.adicionar_filho(expressao)
        
        return no
    
    def _analisar_declaracao_funcao(self) -> NoSintatico:
        """
        DeclaracaoFuncao -> 'func' NomeFuncao '(' ')'
        """
        no = NoSintatico("DECLARACAO_FUNCAO")
        
        # 'func'
        token_func = self._consumir_token(TokenType.FUNCTION, "Esperado 'func'")
        if token_func:
            no_func = NoSintatico("PALAVRA_FUNC", token_func.lexema, token=token_func)
            no.adicionar_filho(no_func)
        
        # Nome da função (identificador)
        token_nome = self._consumir_token(TokenType.IDENTIFICADOR, "Esperado nome da função após 'func'")
        if token_nome:
            no_nome = NoSintatico("NOME_FUNCAO", token_nome.lexema, token=token_nome)
            no.adicionar_filho(no_nome)
        
        # '('
        if self._consumir_token(TokenType.ABRE_PARENT, "Esperado '(' após nome da função"):
            no_abre = NoSintatico("ABRE_PARENTESES", "(")
            no.adicionar_filho(no_abre)
        
        # ')'
        if self._consumir_token(TokenType.FECHA_PARENT, "Esperado ')' para fechar declaração da função"):
            no_fecha = NoSintatico("FECHA_PARENTESES", ")")
            no.adicionar_filho(no_fecha)
        
        return no
    
    def _analisar_chamada_funcao(self) -> NoSintatico:
        """
        ChamadaFuncao -> Identificador '(' ')'
        """
        no = NoSintatico("CHAMADA_FUNCAO")
        
        # Nome da função (identificador)
        token_nome = self._consumir_token(TokenType.IDENTIFICADOR, "Esperado nome da função")
        if token_nome:
            no_nome = NoSintatico("NOME_FUNCAO", token_nome.lexema, token=token_nome)
            no.adicionar_filho(no_nome)
        
        # '('
        if self._consumir_token(TokenType.ABRE_PARENT, "Esperado '(' após nome da função"):
            no_abre = NoSintatico("ABRE_PARENTESES", "(")
            no.adicionar_filho(no_abre)
        
        # ')'
        if self._consumir_token(TokenType.FECHA_PARENT, "Esperado ')' para fechar chamada da função"):
            no_fecha = NoSintatico("FECHA_PARENTESES", ")")
            no.adicionar_filho(no_fecha)
        
        return no
    
    def _analisar_comando_input(self) -> NoSintatico:
        """
        ComandoInput -> 'input' '(' Identificador ')'
        """
        no = NoSintatico("COMANDO_INPUT")
        
        # 'input'
        self._consumir_token(TokenType.INPUT, "Esperado 'input'")
        
        # '('
        if not self._consumir_token(TokenType.ABRE_PARENT, "Esperado '(' após 'input'"):
            return no
        
        # Identificador
        token_id = self._consumir_token(TokenType.IDENTIFICADOR, "Esperado identificador dentro dos parênteses")
        if token_id:
            no_id = NoSintatico("IDENTIFICADOR", token_id.lexema, token=token_id)
            no.adicionar_filho(no_id)
        
        # ')'
        self._consumir_token(TokenType.FECHA_PARENT, "Esperado ')' para fechar comando input")
        
        return no
    
    def _analisar_comando_output(self) -> NoSintatico:
        """
        ComandoOutput -> 'wrt' Expressao
        """
        no = NoSintatico("COMANDO_OUTPUT")
        
        # 'wrt'
        self._consumir_token(TokenType.WRT, "Esperado 'wrt'")
        
        # Expressão (pode ser string, identificador, valor)
        expressao = self._analisar_expressao()
        if expressao:
            no.adicionar_filho(expressao)
        else:
            erro = Token(
                tipo=TokenType.ERRO_SINTAXE_COMANDO_WRT_MALFORMADO,
                lexema="wrt",
                linha=self._token_atual().linha if self._token_atual() else 1,
                coluna=self._token_atual().coluna if self._token_atual() else 1,
                descricao="Comando 'wrt' deve ser seguido por uma expressão válida",
                eh_erro=True
            )
            self.erros_sintaticos.append(erro)
        
        return no
    
    def _analisar_estrutura_condicional(self) -> NoSintatico:
        """
        EstruturaCondicional -> 'cdt' '[' ExpressaoLogica ']' ListaComandos 
                               ('!cdt+' '[' ExpressaoLogica ']' ListaComandos)* 
                               ('!cdt' ListaComandos)?
        """
        no = NoSintatico("ESTRUTURA_CONDICIONAL")
        
        # 'cdt'
        self._consumir_token(TokenType.COND_SE, "Esperado 'cdt'")
        
        # Analisa condição principal
        condicao = self._analisar_condicao()
        if condicao:
            no.adicionar_filho(condicao)
        
        # Comandos do 'cdt'
        comandos_if = self._analisar_bloco_comandos("COND_SE")
        if comandos_if:
            no.adicionar_filho(comandos_if)
        
        # Analisa '!cdt+' (senãose) - pode ter múltiplos
        while self._verificar_token(TokenType.COND_SENAOSE):
            self._avancar()
            no_senaose = NoSintatico("SENAO_SE")
            
            condicao_senaose = self._analisar_condicao()
            if condicao_senaose:
                no_senaose.adicionar_filho(condicao_senaose)
            
            comandos_senaose = self._analisar_bloco_comandos("COND_SENAOSE")
            if comandos_senaose:
                no_senaose.adicionar_filho(comandos_senaose)
            
            no.adicionar_filho(no_senaose)
        
        # Analisa '!cdt' (senão) - opcional
        if self._verificar_token(TokenType.COND_SENAO):
            self._avancar()
            no_senao = NoSintatico("SENAO")
            
            comandos_senao = self._analisar_bloco_comandos("COND_SENAO")
            if comandos_senao:
                no_senao.adicionar_filho(comandos_senao)
            
            no.adicionar_filho(no_senao)
        
        return no
    
    def _analisar_estrutura_repeticao(self) -> NoSintatico:
        """
        EstruturaRepeticao -> 'cycle' '[' ExpressaoLogica ']' ListaComandos |
                             'during' '[' ExpressaoLogica ']' ListaComandos |
                             'repeat' Identificador 'in' Valor ListaComandos
        """
        token = self._token_atual()
        no = NoSintatico("ESTRUTURA_REPETICAO")
        
        if token.tipo == TokenType.REP_PARA:  # cycle
            self._avancar()
            no_tipo = NoSintatico("TIPO_REPETICAO", "cycle")
            no.adicionar_filho(no_tipo)
            
            condicao = self._analisar_condicao()
            if condicao:
                no.adicionar_filho(condicao)
            
            comandos = self._analisar_bloco_comandos("REP_PARA")
            if comandos:
                no.adicionar_filho(comandos)
                
        elif token.tipo == TokenType.REP_ENQUANTO:  # during
            self._avancar()
            no_tipo = NoSintatico("TIPO_REPETICAO", "during")
            no.adicionar_filho(no_tipo)
            
            condicao = self._analisar_condicao()
            if condicao:
                no.adicionar_filho(condicao)
            
            comandos = self._analisar_bloco_comandos("REP_ENQUANTO")
            if comandos:
                no.adicionar_filho(comandos)
                
        elif token.tipo == TokenType.REP_RANGE:  # repeat
            self._avancar()
            no_tipo = NoSintatico("TIPO_REPETICAO", "repeat")
            no.adicionar_filho(no_tipo)
            
            # Identificador
            token_id = self._consumir_token(TokenType.IDENTIFICADOR, "Esperado identificador após 'repeat'")
            if token_id:
                no_id = NoSintatico("IDENTIFICADOR", token_id.lexema, token=token_id)
                no.adicionar_filho(no_id)
            
            # 'in'
            if self._verificar_token(TokenType.IN):
                self._avancar()
                no_in = NoSintatico("PALAVRA_IN", "in")
                no.adicionar_filho(no_in)
            else:
                erro = Token(
                    tipo=TokenType.ERRO_SINTAXE_ESTRUTURA_REPETICAO_MALFORMADA,
                    lexema="repeat",
                    linha=token.linha,
                    coluna=token.coluna,
                    descricao="Esperado 'in' após identificador em comando 'repeat'",
                    eh_erro=True
                )
                self.erros_sintaticos.append(erro)
            
            # Valor
            valor = self._analisar_valor()
            if valor:
                no.adicionar_filho(valor)
            
            comandos = self._analisar_bloco_comandos("REP_RANGE")
            if comandos:
                no.adicionar_filho(comandos)
        
        return no
    
    def _analisar_condicao(self) -> Optional[NoSintatico]:
        """
        Condicao -> '[' ExpressaoLogica ']'
        """
        # '['
        if not self._consumir_token(TokenType.ABRE_COLCHETES, "Esperado '[' para iniciar condição"):
            return None
        
        # Expressão lógica
        expressao = self._analisar_expressao_logica()
        
        # ']'
        self._consumir_token(TokenType.FECHA_COLCHETES, "Esperado ']' para fechar condição")
        
        return expressao
    
    def _analisar_bloco_comandos(self, contexto_pai: str = "") -> Optional[NoSintatico]:
        """Analisa um bloco de comandos até encontrar uma palavra-chave de fechamento."""
        bloco = NoSintatico("BLOCO_COMANDOS")
        
        while self._token_atual() and self._token_atual().tipo != TokenType.EOF:
            token = self._token_atual()
            
            # Ignora quebras de linha
            if self._verificar_token(TokenType.NEWLINE):
                self._avancar()
                continue
            
            # Para quando encontra tokens que finalizam blocos condicionais
            if token.tipo in [TokenType.COND_SENAO, TokenType.COND_SENAOSE]:
                break
            
            # Para quando encontra uma nova estrutura de controle no mesmo nível 
            # (apenas se já temos comandos no bloco)
            if (token.tipo in [TokenType.COND_SE, TokenType.REP_PARA, 
                              TokenType.REP_ENQUANTO, TokenType.REP_RANGE] and 
                len(bloco.filhos) > 0):
                # Se estamos em um contexto de repetição e encontramos outra estrutura de controle,
                # isso indica o fim do bloco de repetição
                if contexto_pai in ["REP_PARA", "REP_ENQUANTO", "REP_RANGE"]:
                    break
                # Se estamos em um contexto condicional, só paramos em estruturas de mesmo nível
                elif contexto_pai == "COND_SE" and token.tipo == TokenType.COND_SE:
                    break
            
            comando = self._analisar_comando()
            if comando:
                bloco.adicionar_filho(comando)
            else:
                # Se não conseguiu analisar comando, para para evitar loop infinito
                break
        
        return bloco if bloco.filhos else None
    
    def _analisar_expressao_logica(self) -> Optional[NoSintatico]:
        """
        ExpressaoLogica -> ExpressaoRelacional (OperadorLogico ExpressaoRelacional)*
        """
        esq = self._analisar_expressao_relacional()
        if not esq:
            return None
        
        while (self._token_atual() and 
               self._token_atual().tipo == TokenType.OPER_LOGICO):
            op_token = self._avancar()
            dir = self._analisar_expressao_relacional()
            
            if dir:
                no_op = NoSintatico("EXPRESSAO_LOGICA", op_token.lexema)
                no_op.adicionar_filho(esq)
                no_op.adicionar_filho(dir)
                esq = no_op
            else:
                erro = Token(
                    tipo=TokenType.ERRO_SINTAXE_EXPRESSAO_INVALIDA,
                    lexema=op_token.lexema,
                    linha=op_token.linha,
                    coluna=op_token.coluna,
                    descricao=f"Expressão incompleta após operador lógico '{op_token.lexema}'",
                    eh_erro=True
                )
                self.erros_sintaticos.append(erro)
                break
        
        return esq
    
    def _analisar_expressao_relacional(self) -> Optional[NoSintatico]:
        """
        ExpressaoRelacional -> Expressao OperadorRelacional Expressao
        """
        esq = self._analisar_expressao()
        if not esq:
            return None
        
        if (self._token_atual() and 
            self._token_atual().tipo == TokenType.OP_REL):
            op_token = self._avancar()
            dir = self._analisar_expressao()
            
            if dir:
                no_op = NoSintatico("EXPRESSAO_RELACIONAL", op_token.lexema)
                no_op.adicionar_filho(esq)
                no_op.adicionar_filho(dir)
                return no_op
            else:
                erro = Token(
                    tipo=TokenType.ERRO_SINTAXE_EXPRESSAO_INVALIDA,
                    lexema=op_token.lexema,
                    linha=op_token.linha,
                    coluna=op_token.coluna,
                    descricao=f"Expressão incompleta após operador relacional '{op_token.lexema}'",
                    eh_erro=True
                )
                self.erros_sintaticos.append(erro)
        
        return esq
    
    def _analisar_expressao(self) -> Optional[NoSintatico]:
        """
        Expressao -> Termo (OperadorMatematico Termo)*
        """
        esq = self._analisar_termo()
        if not esq:
            return None
        
        while (self._token_atual() and 
               self._token_atual().tipo == TokenType.OPER_MATEMATICO):
            op_token = self._avancar()
            dir = self._analisar_termo()
            
            if dir:
                no_op = NoSintatico("EXPRESSAO_MATEMATICA", op_token.lexema)
                no_op.adicionar_filho(esq)
                no_op.adicionar_filho(dir)
                esq = no_op
            else:
                erro = Token(
                    tipo=TokenType.ERRO_SINTAXE_EXPRESSAO_INVALIDA,
                    lexema=op_token.lexema,
                    linha=op_token.linha,
                    coluna=op_token.coluna,
                    descricao=f"Expressão incompleta após operador matemático '{op_token.lexema}'",
                    eh_erro=True
                )
                self.erros_sintaticos.append(erro)
                break
        
        return esq
    
    def _analisar_termo(self) -> Optional[NoSintatico]:
        """
        Termo -> Valor | Identificador | '(' Expressao ')'
        """
        token = self._token_atual()
        if not token:
            return None
        
        if token.tipo == TokenType.ABRE_PARENT:
            # Expressão entre parênteses
            self._avancar()
            expressao = self._analisar_expressao()
            self._consumir_token(TokenType.FECHA_PARENT, "Esperado ')' para fechar expressão")
            return expressao
        elif token.tipo == TokenType.IDENTIFICADOR:
            self._avancar()
            return NoSintatico("IDENTIFICADOR", token.lexema, token=token)
        else:
            return self._analisar_valor()
    
    def _analisar_valor(self) -> Optional[NoSintatico]:
        """
        Valor -> ValorInteiro | ValorReal | ValorTexto | ValorLogico
        """
        token = self._token_atual()
        if not token:
            return None
        
        if token.tipo in [TokenType.VALOR_INTEIRO, TokenType.VALOR_REAL, 
                         TokenType.VALOR_TEXTO, TokenType.VALOR_LOGICO]:
            self._avancar()
            tipo_map = {
                TokenType.VALOR_INTEIRO: "VALOR_INTEIRO",
                TokenType.VALOR_REAL: "VALOR_REAL",
                TokenType.VALOR_TEXTO: "VALOR_TEXTO",
                TokenType.VALOR_LOGICO: "VALOR_LOGICO"
            }
            return NoSintatico(tipo_map[token.tipo], token.lexema, token=token)
        
        return None
    
    def obter_arvore_como_string(self) -> str:
        """Retorna a árvore sintática como string formatada."""
        if not self.arvore_sintatica:
            return "Nenhuma árvore sintática gerada."
        
        return str(self.arvore_sintatica)
    
    def validar_delimitadores(self) -> List[Token]:
        """Valida se parênteses e colchetes estão balanceados."""
        erros = []
        pilha_parenteses = []
        pilha_colchetes = []
        
        for token in self.tokens:
            if token.tipo == TokenType.ABRE_PARENT:
                pilha_parenteses.append(token)
            elif token.tipo == TokenType.FECHA_PARENT:
                if not pilha_parenteses:
                    erro = Token(
                        tipo=TokenType.ERRO_SINTAXE_PARENTESES_NAO_FECHADOS,
                        lexema=token.lexema,
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao="Parênteses de fechamento ')' sem abertura correspondente",
                        eh_erro=True
                    )
                    erros.append(erro)
                else:
                    pilha_parenteses.pop()
            elif token.tipo == TokenType.ABRE_COLCHETES:
                pilha_colchetes.append(token)
            elif token.tipo == TokenType.FECHA_COLCHETES:
                if not pilha_colchetes:
                    erro = Token(
                        tipo=TokenType.ERRO_SINTAXE_COLCHETES_NAO_FECHADOS,
                        lexema=token.lexema,
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao="Colchetes de fechamento ']' sem abertura correspondente",
                        eh_erro=True
                    )
                    erros.append(erro)
                else:
                    pilha_colchetes.pop()
        
        # Verifica parênteses não fechados
        for token in pilha_parenteses:
            erro = Token(
                tipo=TokenType.ERRO_SINTAXE_PARENTESES_NAO_FECHADOS,
                lexema=token.lexema,
                linha=token.linha,
                coluna=token.coluna,
                descricao="Parênteses de abertura '(' não fechado",
                eh_erro=True
            )
            erros.append(erro)
        
        # Verifica colchetes não fechados
        for token in pilha_colchetes:
            erro = Token(
                tipo=TokenType.ERRO_SINTAXE_COLCHETES_NAO_FECHADOS,
                lexema=token.lexema,
                linha=token.linha,
                coluna=token.coluna,
                descricao="Colchetes de abertura '[' não fechado",
                eh_erro=True
            )
            erros.append(erro)
        
        return erros
class AnalisadorLexico:
    def __init__(self):
        # Constantes para limites
        self.MAX_IDENTIFICADOR_LENGTH = 30
        self.MAX_NUMERO_LENGTH = 15
        
        # Definindo os padrões de tokens com base na tabela fornecida
        self.token_patterns = [
            # Comentários (deve vir primeiro para evitar conflitos)
            (TokenType.COMENTARIO, r'--.*', "Comentário"),
            
            # Palavras reservadas (ordem específica para evitar conflitos)
            (TokenType.INICIO, r'\bals\b', "Palavra reservada para início"),
            (TokenType.COND_SENAOSE, r'!cdt\+', "Palavra reservada para senãose"),
            (TokenType.COND_SENAO, r'!cdt(?!\+)', "Palavra reservada para senão"),
            (TokenType.COND_SE, r'\bcdt\b', "Palavra reservada para se"),
            (TokenType.REP_PARA, r'\bcycle\b', "Palavra reservada para estrutura de repetição para"),
            (TokenType.REP_ENQUANTO, r'\bduring\b', "Palavra reservada para estrutura de repetição enquanto"),
            (TokenType.REP_RANGE, r'\brepeat\b', "Palavra reservada para repetição com contador fixo"),
            (TokenType.WRT, r'\bwrt\b', "Palavra reservada para saída"),
            (TokenType.INPUT, r'\binput\b', "Palavra reservada para entrada de dados"),
            (TokenType.FUNCTION, r'\bfunc\b', "Palavra reservada para criação de funções"),
            (TokenType.PULAR_LINHA, r'\bbrkln\b', "Palavra reservada para quebra de linha"),
            (TokenType.IN, r'\bin\b', "Palavra reservada para repeat...in"),
            
            # Tipos de variáveis
            (TokenType.TIPO_VAR, r'\b(intn|den|txt|bln|crt)\b', "Tipos de variáveis"),
            
            # Valores lógicos
            (TokenType.VALOR_LOGICO, r'\b(valid|invalid)\b', "Valor booleano"),
            
            # Operadores relacionais
            (TokenType.OP_REL, r'\b(gt|eq|ne|lt|ge|le)\b', "Operadores relacionais"),
            
            # Operadores lógicos
            (TokenType.OPER_LOGICO, r'\b(and|or)\b', "Operadores lógicos"),
            
            # Operador de atribuição
            (TokenType.OPER_ATRIB, r'<=', "Operador de atribuição"),
            
            # Operadores matemáticos
            (TokenType.OPER_MATEMATICO, r'[+\-*/]', "Operadores matemáticos"),
            
            # Valores numéricos (reais devem vir antes dos inteiros)
            (TokenType.VALOR_REAL, r'\b\d+\.\d+\b', "Valor real"),
            (TokenType.VALOR_INTEIRO, r'\b\d+\b', "Valor inteiro"),
            
            # Strings (valores de texto)
            (TokenType.VALOR_TEXTO, r'"[^"]*"', "Valor de texto"),
            
            # Delimitadores
            (TokenType.ABRE_PARENT, r'\(', "Abertura de parênteses"),
            (TokenType.FECHA_PARENT, r'\)', "Fechamento de parênteses"),
            (TokenType.ABRE_COLCHETES, r'\[', "Abertura de colchetes"),
            (TokenType.FECHA_COLCHETES, r'\]', "Fechamento de colchetes"),
            (TokenType.VIRGULA, r',', "Vírgula"),
            
            # Identificadores (nomes de funções e variáveis)
            (TokenType.IDENTIFICADOR, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', "Identificador"),
            
            # Whitespace e quebras de linha
            (TokenType.NEWLINE, r'\n', "Quebra de linha"),
            (TokenType.WHITESPACE, r'[ \t]+', "Espaço em branco"),
        ]
        
        # Compilar os padrões regex
        self.compiled_patterns = [
            (token_type, re.compile(pattern), desc) 
            for token_type, pattern, desc in self.token_patterns
        ]
    
    def _verificar_string_nao_fechada(self, linha: str, posicao: int) -> Optional[Token]:
        if linha[posicao] == '"':
            # Procura pelo fechamento da string
            pos_atual = posicao + 1
            while pos_atual < len(linha) and linha[pos_atual] != '"':
                pos_atual += 1
            
            if pos_atual >= len(linha):
                # String não fechada
                lexema = linha[posicao:]
                return Token(
                    tipo=TokenType.ERRO_STRING_NAO_FECHADA,
                    lexema=lexema,
                    linha=0,  # Será definido pelo chamador
                    coluna=posicao + 1,
                    descricao=f"String não fechada: '{lexema}'",
                    eh_erro=True
                )
        return None
    
    def _verificar_numero_malformado(self, linha: str, posicao: int) -> Optional[Token]:
        if linha[posicao].isdigit():
            pos_atual = posicao
            tem_ponto = False
            lexema = ""
            
            while pos_atual < len(linha):
                char = linha[pos_atual]
                if char.isdigit():
                    lexema += char
                elif char == '.' and not tem_ponto:
                    lexema += char
                    tem_ponto = True
                elif char.isalpha():
                    # Número seguido de letra - erro
                    lexema += char
                    pos_atual += 1
                    # Continua coletando até encontrar um delimitador
                    while pos_atual < len(linha) and (linha[pos_atual].isalnum() or linha[pos_atual] == '.'):
                        lexema += linha[pos_atual]
                        pos_atual += 1
                    
                    return Token(
                        tipo=TokenType.ERRO_NUMERO_MALFORMADO,
                        lexema=lexema,
                        linha=0,  # Será definido pelo chamador
                        coluna=posicao + 1,
                        descricao=f"Número mal formado: '{lexema}'",
                        eh_erro=True
                    )
                else:
                    break
                pos_atual += 1
            
            # Verifica se o número é muito longo
            if len(lexema) > self.MAX_NUMERO_LENGTH:
                return Token(
                    tipo=TokenType.ERRO_NUMERO_MUITO_LONGO,
                    lexema=lexema,
                    linha=0,  # Será definido pelo chamador
                    coluna=posicao + 1,
                    descricao=f"Número muito longo (máximo {self.MAX_NUMERO_LENGTH} caracteres): '{lexema}'",
                    eh_erro=True
                )
        
        return None
    
    def _verificar_identificador_malformado(self, linha: str, posicao: int) -> Optional[Token]:
        """Verifica se há um identificador mal formado."""
        char = linha[posicao]
        
        # Identificador começando com número
        if char.isdigit():
            pos_atual = posicao
            lexema = ""
            
            # Coleta o identificador mal formado
            while pos_atual < len(linha) and (linha[pos_atual].isalnum() or linha[pos_atual] in '_@'):
                lexema += linha[pos_atual]
                pos_atual += 1
            
            if any(c.isalpha() or c in '_@' for c in lexema):
                return Token(
                    tipo=TokenType.ERRO_IDENTIFICADOR_MALFORMADO,
                    lexema=lexema,
                    linha=0,  # Será definido pelo chamador
                    coluna=posicao + 1,
                    descricao=f"Identificador mal formado (não pode começar com número): '{lexema}'",
                    eh_erro=True
                )
        
        # Identificador com caracteres inválidos
        if char.isalpha() or char == '_':
            pos_atual = posicao
            lexema = ""
            tem_caracter_invalido = False
            
            while pos_atual < len(linha) and (linha[pos_atual].isalnum() or linha[pos_atual] in '_@'):
                lexema += linha[pos_atual]
                if linha[pos_atual] == '@':
                    tem_caracter_invalido = True
                pos_atual += 1
            
            if tem_caracter_invalido:
                return Token(
                    tipo=TokenType.ERRO_IDENTIFICADOR_MALFORMADO,
                    lexema=lexema,
                    linha=0,  # Será definido pelo chamador
                    coluna=posicao + 1,
                    descricao=f"Identificador mal formado (contém caracteres inválidos): '{lexema}'",
                    eh_erro=True
                )
            
            # Verifica se o identificador é muito longo
            if len(lexema) > self.MAX_IDENTIFICADOR_LENGTH:
                return Token(
                    tipo=TokenType.ERRO_IDENTIFICADOR_MUITO_LONGO,
                    lexema=lexema,
                    linha=0,  # Será definido pelo chamador
                    coluna=posicao + 1,
                    descricao=f"Identificador muito longo (máximo {self.MAX_IDENTIFICADOR_LENGTH} caracteres): '{lexema}'",
                    eh_erro=True
                )
        
        return None
    
    def _verificar_operador_relacional_malformado(self, linha: str, posicao: int) -> Optional[Token]:
        # Lista de operadores relacionais válidos
        operadores_validos = {'gt', 'eq', 'ne', 'lt', 'ge', 'le'}
        
        # Lista de possíveis erros comuns de operadores relacionais
        operadores_malformados = {
            'e': 'eq',      # "e" em vez de "eq" (igual)
            'g': 'gt',      # "g" em vez de "gt" (maior que)
            'l': 'lt',      # "l" em vez de "lt" (menor que)
            'n': 'ne',      # "n" em vez de "ne" (não igual)
            'ge': 'ge',     # parcialmente correto
            'le': 'le',     # parcialmente correto
            'igual': 'eq',  # palavra em português
            'maior': 'gt',  # palavra em português
            'menor': 'lt',  # palavra em português
        }
        
        # Extrai a próxima palavra
        match = re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', linha[posicao:])
        if match:
            lexema = match.group(0)
            
            # Verifica se está dentro de colchetes (contexto de condição)
            inicio_colchete = linha.rfind('[', 0, posicao)
            fim_colchete = linha.find(']', posicao)
            
            if inicio_colchete != -1 and fim_colchete != -1:
                # Está dentro de uma condição, verifica se é um operador malformado
                if lexema in operadores_malformados and lexema not in operadores_validos:
                    sugestao = operadores_malformados[lexema]
                    return Token(
                        tipo=TokenType.ERRO_OPERADOR_RELACIONAL_MALFORMADO,
                        lexema=lexema,
                        linha=0,  # Será definido pelo chamador
                        coluna=posicao + 1,
                        descricao=f"Operador relacional mal formado: '{lexema}'. Sugestão: use '{sugestao}'",
                        eh_erro=True
                    )
        
        return None
    
    def _verificar_palavra_reservada_malformada(self, linha: str, posicao: int) -> Optional[Token]:
        # Lista de palavras reservadas válidas
        palavras_validas = {
            'als', 'cdt', '!cdt', '!cdt+', 'cycle', 'during', 'repeat', 
            'wrt', 'input', 'func', 'brkln', 'intn', 'den', 'txt', 'bln', 'crt', 'in'
        }
        
        # Lista de possíveis erros comuns de palavras reservadas
        palavras_malformadas = {
            'wr': 'wrt',        # "wr" em vez de "wrt"
            'wt': 'wrt',        # "wt" em vez de "wrt"
            'write': 'wrt',     # palavra em inglês
            'inp': 'input',     # "inp" em vez de "input"
            'read': 'input',    # palavra em inglês
            'scanf': 'input',   # referência C
            'int': 'intn',      # "int" em vez de "intn"
            'cd': 'cdt',        # "cd" em vez de "cdt"
            'if': 'cdt',        # palavra em inglês
            'else': '!cdt',     # palavra em inglês
            'elseif': '!cdt+',  # palavra em inglês
            'al': 'als',        # "al" em vez de "als"
            'start': 'als',     # palavra em inglês
            'function': 'func', # "function" em vez de "func"
            'fn': 'func',       # "fn" em vez de "func"
        }
        
        # Extrai a próxima palavra
        match = re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', linha[posicao:])
        if match:
            lexema = match.group(0)
            
            # Verifica se é uma palavra reservada malformada
            if lexema in palavras_malformadas and lexema not in palavras_validas:
                sugestao = palavras_malformadas[lexema]
                return Token(
                    tipo=TokenType.ERRO_PALAVRA_RESERVADA_MALFORMADA,
                    lexema=lexema,
                    linha=0,  # Será definido pelo chamador
                    coluna=posicao + 1,
                    descricao=f"Palavra reservada mal formada: '{lexema}'. Sugestão: use '{sugestao}'",
                    eh_erro=True
                )
        
        return None

    def _validar_inicio_programa(self, tokens: List[Token]) -> Optional[Token]:
        for token in tokens:
            # Ignora tokens que não são significativos para a estrutura
            if token.tipo in [TokenType.COMENTARIO, TokenType.WHITESPACE, TokenType.NEWLINE, TokenType.EOF]:
                continue
            
            # O primeiro token significativo deve ser 'als'
            if token.tipo == TokenType.INICIO:
                return None  # Programa válido
            else:
                # Programa não começa com 'als'
                return Token(
                    tipo=TokenType.ERRO_PROGRAMA_SEM_INICIO,
                    lexema="",
                    linha=token.linha,
                    coluna=token.coluna,
                    descricao="Programa deve começar com a palavra reservada 'als'",
                    eh_erro=True
                )
        
        # Se chegou aqui, não há tokens significativos
        return Token(
            tipo=TokenType.ERRO_PROGRAMA_SEM_INICIO,
            lexema="",
            linha=1,
            coluna=1,
            descricao="Programa deve começar com a palavra reservada 'als'",
            eh_erro=True
        )
    
    def _validar_tipos_variaveis(self, tokens: List[Token]) -> List[Token]:
        erros_tipo = []
        variaveis = {}  # {nome_variavel: tipo}
        
        i = 0
        while i < len(tokens):
            token_atual = tokens[i]
            
            # Identifica declaração de variável: tipo identificador
            if (token_atual.tipo == TokenType.TIPO_VAR and 
                i + 1 < len(tokens) and 
                tokens[i + 1].tipo == TokenType.IDENTIFICADOR):
                
                tipo_var = token_atual.lexema
                nome_var = tokens[i + 1].lexema
                variaveis[nome_var] = tipo_var
                i += 2
                continue
            
            # Identifica atribuição: identificador <= valor
            if (token_atual.tipo == TokenType.IDENTIFICADOR and
                i + 2 < len(tokens) and
                tokens[i + 1].tipo == TokenType.OPER_ATRIB):
                
                nome_var = token_atual.lexema
                valor_token = tokens[i + 2]
                
                # Verifica se a variável foi declarada
                if nome_var in variaveis:
                    tipo_var = variaveis[nome_var]
                    
                    # Validação de tipos
                    erro = None
                    if tipo_var == "intn" and valor_token.tipo == TokenType.VALOR_REAL:
                        erro = Token(
                            tipo=TokenType.ERRO_TIPO_INCOMPATIVEL,
                            lexema=f"{nome_var} <= {valor_token.lexema}",
                            linha=token_atual.linha,
                            coluna=token_atual.coluna,
                            descricao=f"Variável '{nome_var}' do tipo 'intn' não pode receber valor decimal '{valor_token.lexema}'. Use tipo 'den' para valores decimais.",
                            eh_erro=True
                        )
                    elif tipo_var == "bln" and valor_token.tipo not in [TokenType.VALOR_LOGICO]:
                        erro = Token(
                            tipo=TokenType.ERRO_TIPO_INCOMPATIVEL,
                            lexema=f"{nome_var} <= {valor_token.lexema}",
                            linha=token_atual.linha,
                            coluna=token_atual.coluna,
                            descricao=f"Variável '{nome_var}' do tipo 'bln' só pode receber valores lógicos (valid/invalid).",
                            eh_erro=True
                        )
                    elif tipo_var == "txt" and valor_token.tipo != TokenType.VALOR_TEXTO:
                        erro = Token(
                            tipo=TokenType.ERRO_TIPO_INCOMPATIVEL,
                            lexema=f"{nome_var} <= {valor_token.lexema}",
                            linha=token_atual.linha,
                            coluna=token_atual.coluna,
                            descricao=f"Variável '{nome_var}' do tipo 'txt' só pode receber valores de texto entre aspas.",
                            eh_erro=True
                        )
                    
                    if erro:
                        erros_tipo.append(erro)
                
                i += 3
                continue
            
            i += 1
        
        return erros_tipo

    def _validar_expressoes_condicionais(self, tokens: List[Token]) -> List[Token]:
        erros = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # Procura por abertura de colchetes
            if token.tipo == TokenType.ABRE_COLCHETES:
                j = i + 1
                elementos_significativos = []
                
                # Coleta tokens até o fechamento dos colchetes
                while j < len(tokens) and tokens[j].tipo != TokenType.FECHA_COLCHETES:
                    token_atual = tokens[j]
                    # Ignora whitespace e newlines
                    if token_atual.tipo not in [TokenType.WHITESPACE, TokenType.NEWLINE]:
                        elementos_significativos.append(token_atual)
                    j += 1
                
                # Valida a estrutura da expressão condicional
                if len(elementos_significativos) >= 2:
                    # Verifica se há dois valores consecutivos sem operador relacional
                    # mas ignora se há operadores lógicos entre eles
                    for k in range(len(elementos_significativos) - 1):
                        token_atual = elementos_significativos[k]
                        token_proximo = elementos_significativos[k + 1]
                        
                        # Verifica se são dois valores/identificadores consecutivos
                        # sem operador relacional ou lógico entre eles
                        if (token_atual.tipo in [TokenType.IDENTIFICADOR, TokenType.VALOR_INTEIRO, TokenType.VALOR_REAL] and
                            token_proximo.tipo in [TokenType.IDENTIFICADOR, TokenType.VALOR_INTEIRO, TokenType.VALOR_REAL]):
                            
                            # Verifica se não há operador lógico anterior que justifique
                            tem_operador_logico = False
                            if k > 0 and elementos_significativos[k - 1].tipo == TokenType.OPER_LOGICO:
                                tem_operador_logico = True
                            
                            if not tem_operador_logico:
                                erro = Token(
                                    tipo=TokenType.ERRO_OPERADOR_RELACIONAL_AUSENTE,
                                    lexema=f"{token_atual.lexema} {token_proximo.lexema}",
                                    linha=token_atual.linha,
                                    coluna=token_atual.coluna,
                                    descricao=f"Operador relacional ausente entre '{token_atual.lexema}' e '{token_proximo.lexema}'. Use: gt, eq, ne, lt, ge, le",
                                    eh_erro=True
                                )
                                erros.append(erro)
                
                # Valida a estrutura de expressões com operadores lógicos
                self._validar_expressao_logica(elementos_significativos, erros)
                
                i = j  # Pula para depois dos colchetes
            else:
                i += 1
        
        return erros
    
    def _validar_expressao_logica(self, elementos: List[Token], erros: List[Token]) -> None:
        """Valida a estrutura de expressões lógicas compostas."""
        i = 0
        while i < len(elementos):
            token = elementos[i]
            
            # Se encontrou um operador lógico (AND/OR)
            if token.tipo == TokenType.OPER_LOGICO:
                # Verifica se há elementos suficientes antes e depois
                if i < 3:  # Precisa de pelo menos: valor op_rel valor AND
                    erro = Token(
                        tipo=TokenType.ERRO_OPERADOR_RELACIONAL_AUSENTE,
                        lexema=token.lexema,
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao=f"Operador lógico '{token.lexema}' sem expressão relacional completa anterior",
                        eh_erro=True
                    )
                    erros.append(erro)
                
                if i + 3 >= len(elementos):  # Precisa de pelo menos: AND valor op_rel valor
                    erro = Token(
                        tipo=TokenType.ERRO_OPERADOR_RELACIONAL_AUSENTE,
                        lexema=token.lexema,
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao=f"Operador lógico '{token.lexema}' sem expressão relacional completa posterior",
                        eh_erro=True
                    )
                    erros.append(erro)
            
            i += 1

    def _validar_comando_input(self, tokens: List[Token]) -> List[Token]:
        """Valida a sintaxe do comando input."""
        erros = []
        variaveis_declaradas = set()
        
        # Primeiro, coleta todas as variáveis declaradas
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if (token.tipo == TokenType.TIPO_VAR and 
                i + 1 < len(tokens) and 
                tokens[i + 1].tipo == TokenType.IDENTIFICADOR):
                variaveis_declaradas.add(tokens[i + 1].lexema)
                i += 2
            else:
                i += 1
        
        # Agora valida os comandos input
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.tipo == TokenType.INPUT:
                # Verifica se há parênteses após input
                j = i + 1
                # Pula whitespace
                while j < len(tokens) and tokens[j].tipo == TokenType.WHITESPACE:
                    j += 1
                
                if j >= len(tokens) or tokens[j].tipo != TokenType.ABRE_PARENT:
                    erro = Token(
                        tipo=TokenType.ERRO_INPUT_SINTAXE_INCORRETA,
                        lexema="input",
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao="Comando 'input' deve ser seguido por parênteses: input(variavel)",
                        eh_erro=True
                    )
                    erros.append(erro)
                    i += 1
                    continue
                
                j += 1  # Pula o (
                # Pula whitespace
                while j < len(tokens) and tokens[j].tipo == TokenType.WHITESPACE:
                    j += 1
                
                if j >= len(tokens):
                    erro = Token(
                        tipo=TokenType.ERRO_INPUT_SEM_VARIAVEL,
                        lexema="input(",
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao="Comando 'input' sem variável especificada",
                        eh_erro=True
                    )
                    erros.append(erro)
                    i = j
                    continue
                
                # Deve ter um identificador
                if tokens[j].tipo != TokenType.IDENTIFICADOR:
                    erro = Token(
                        tipo=TokenType.ERRO_INPUT_SEM_VARIAVEL,
                        lexema=f"input({tokens[j].lexema}",
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao="Comando 'input' deve conter uma variável válida entre parênteses",
                        eh_erro=True
                    )
                    erros.append(erro)
                    i = j + 1
                    continue
                
                # Verifica se a variável foi declarada
                nome_variavel = tokens[j].lexema
                if nome_variavel not in variaveis_declaradas:
                    erro = Token(
                        tipo=TokenType.ERRO_INPUT_VARIAVEL_NAO_DECLARADA,
                        lexema=f"input({nome_variavel})",
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao=f"Variável '{nome_variavel}' não foi declarada antes do comando input",
                        eh_erro=True
                    )
                    erros.append(erro)
                
                j += 1  # Pula o identificador
                # Pula whitespace
                while j < len(tokens) and tokens[j].tipo == TokenType.WHITESPACE:
                    j += 1
                
                # Deve ter parêntese de fechamento
                if j >= len(tokens) or tokens[j].tipo != TokenType.FECHA_PARENT:
                    erro = Token(
                        tipo=TokenType.ERRO_INPUT_SINTAXE_INCORRETA,
                        lexema=f"input({nome_variavel}",
                        linha=token.linha,
                        coluna=token.coluna,
                        descricao="Comando 'input' deve ser fechado com parênteses: input(variavel)",
                        eh_erro=True
                    )
                    erros.append(erro)
                
                i = j + 1 if j < len(tokens) else len(tokens)
            else:
                i += 1
        
        return erros

    def analisar_completo(self, codigo: str) -> Tuple[List[Token], Optional[NoSintatico], List[Token]]:
        """
        Realiza análise léxica e sintática completa.
        Retorna: (tokens_lexicos, arvore_sintatica, erros_sintaticos)
        """
        # Análise léxica
        tokens_lexicos = self.analisar(codigo)
        
        # Análise sintática
        analisador_sintatico = AnalisadorSintatico()
        arvore_sintatica, erros_sintaticos = analisador_sintatico.analisar(tokens_lexicos)
        
        # Adiciona validação de delimitadores
        erros_delimitadores = analisador_sintatico.validar_delimitadores()
        erros_sintaticos.extend(erros_delimitadores)
        
        return tokens_lexicos, arvore_sintatica, erros_sintaticos

    def analisar(self, codigo: str) -> List[Token]:
        tokens = []
        linhas = codigo.split('\n')
        
        for num_linha, linha in enumerate(linhas, 1):
            coluna = 0
            
            while coluna < len(linha):
                token_encontrado = False
                
                # Verifica erros específicos primeiro
                erro_string = self._verificar_string_nao_fechada(linha, coluna)
                if erro_string:
                    erro_string.linha = num_linha
                    tokens.append(erro_string)
                    coluna = len(linha)  # Pula para o final da linha
                    continue
                
                erro_numero = self._verificar_numero_malformado(linha, coluna)
                if erro_numero:
                    erro_numero.linha = num_linha
                    tokens.append(erro_numero)
                    # Pula o número mal formado
                    coluna += len(erro_numero.lexema)
                    continue
                
                erro_identificador = self._verificar_identificador_malformado(linha, coluna)
                if erro_identificador:
                    erro_identificador.linha = num_linha
                    tokens.append(erro_identificador)
                    # Pula o identificador mal formado
                    coluna += len(erro_identificador.lexema)
                    continue
                
                erro_operador_relacional = self._verificar_operador_relacional_malformado(linha, coluna)
                if erro_operador_relacional:
                    erro_operador_relacional.linha = num_linha
                    tokens.append(erro_operador_relacional)
                    coluna += len(erro_operador_relacional.lexema)
                    continue
                
                erro_palavra_reservada = self._verificar_palavra_reservada_malformada(linha, coluna)
                if erro_palavra_reservada:
                    erro_palavra_reservada.linha = num_linha
                    tokens.append(erro_palavra_reservada)
                    coluna += len(erro_palavra_reservada.lexema)
                    continue
                
                # Tenta fazer match com cada padrão
                for token_type, pattern, desc in self.compiled_patterns:
                    match = pattern.match(linha, coluna)
                    
                    if match:
                        lexema = match.group(0)
                        
                        # Verifica se identificador é muito longo
                        if token_type == TokenType.IDENTIFICADOR and len(lexema) > self.MAX_IDENTIFICADOR_LENGTH:
                            token = Token(
                                tipo=TokenType.ERRO_IDENTIFICADOR_MUITO_LONGO,
                                lexema=lexema,
                                linha=num_linha,
                                coluna=coluna + 1,
                                descricao=f"Identificador muito longo (máximo {self.MAX_IDENTIFICADOR_LENGTH} caracteres): '{lexema}'",
                                eh_erro=True
                            )
                        elif token_type == TokenType.VALOR_INTEIRO and len(lexema) > self.MAX_NUMERO_LENGTH:
                            token = Token(
                                tipo=TokenType.ERRO_NUMERO_MUITO_LONGO,
                                lexema=lexema,
                                linha=num_linha,
                                coluna=coluna + 1,
                                descricao=f"Número muito longo (máximo {self.MAX_NUMERO_LENGTH} caracteres): '{lexema}'",
                                eh_erro=True
                            )
                        else:
                            # Pula whitespace (mas não quebras de linha)
                            if token_type == TokenType.WHITESPACE:
                                coluna = match.end()
                                token_encontrado = True
                                break
                            
                            token = Token(
                                tipo=token_type,
                                lexema=lexema,
                                linha=num_linha,
                                coluna=coluna + 1,
                                descricao=desc
                            )
                        
                        tokens.append(token)
                        coluna = match.end()
                        token_encontrado = True
                        break
                
                if not token_encontrado:
                    # Verifica se é um símbolo inválido específico
                    char = linha[coluna]
                    if char in '@$%#&!':
                        token = Token(
                            tipo=TokenType.ERRO_SIMBOLO_INVALIDO,
                            lexema=char,
                            linha=num_linha,
                            coluna=coluna + 1,
                            descricao=f"Símbolo não pertencente ao conjunto de símbolos terminais da linguagem: '{char}'",
                            eh_erro=True
                        )
                    else:
                        # Caractere não reconhecido genérico
                        token = Token(
                            tipo=TokenType.ERRO,
                            lexema=char,
                            linha=num_linha,
                            coluna=coluna + 1,
                            descricao=f"Caractere não reconhecido: '{char}'",
                            eh_erro=True
                        )
                    
                    tokens.append(token)
                    coluna += 1
          # Adiciona token EOF
        tokens.append(Token(
            tipo=TokenType.EOF,
            lexema="",
            linha=len(linhas) + 1,
            coluna=1,
            descricao="Fim do arquivo"
        ))
        
        # Valida se o programa começa com 'als'
        erro_inicio = self._validar_inicio_programa(tokens)
        if erro_inicio:
            tokens.insert(0, erro_inicio)
        
        # Validação de tipos
        erros_tipo = self._validar_tipos_variaveis(tokens)
        tokens.extend(erros_tipo)
        
        # Validação de expressões condicionais
        erros_condicionais = self._validar_expressoes_condicionais(tokens)
        tokens.extend(erros_condicionais)
        
        # Validação de comandos input
        erros_input = self._validar_comando_input(tokens)
        tokens.extend(erros_input)
        
        return tokens
    def imprimir_tokens(self, tokens: List[Token]) -> str:
        resultado = f"{'Token':<25} {'Lexema':<20} {'Linha':<6} {'Coluna':<7} {'Descrição'}\n"
        resultado += "-" * 100 + "\n"
        
        for token in tokens:
            if token.tipo != TokenType.EOF:
                cor = "ERRO" if token.eh_erro else "OK"
                resultado += f"{token.tipo.value:<25} {token.lexema:<20} {token.linha:<6} {token.coluna:<7} {token.descricao}\n"
        
        return resultado
    
    def obter_estatisticas(self, tokens: List[Token]) -> dict:
        total_tokens = len([t for t in tokens if t.tipo != TokenType.EOF and t.tipo != TokenType.WHITESPACE])
        total_erros = len([t for t in tokens if t.eh_erro])
        
        tipos_tokens = {}
        for token in tokens:
            if token.tipo != TokenType.EOF and token.tipo != TokenType.WHITESPACE:
                if token.tipo.value in tipos_tokens:
                    tipos_tokens[token.tipo.value] += 1
                else:
                    tipos_tokens[token.tipo.value] = 1
        
        return {
            'total_tokens': total_tokens,
            'total_erros': total_erros,
            'tipos_tokens': tipos_tokens,
            'tokens_validos': total_tokens - total_erros
        }
    
    def analisar_arquivo(self, caminho_arquivo: str) -> List[Token]:
        """
        Analisa um arquivo e retorna os tokens.
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                codigo = arquivo.read()
            return self.analisar(codigo)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return []
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return []


class InterfaceGrafica:
    def __init__(self):
        self.analisador = AnalisadorLexico()
        self.tokens_atuais = []
        self.arvore_sintatica = None
        self.erros_sintaticos = []
        
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Analisador Léxico e Sintático - Linguagem ALAIAS")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configuração de estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        self.criar_interface()
        
    def criar_interface(self):
    
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        titulo = tk.Label(main_frame, text="ANALISADOR LÉXICO E SINTÁTICO - LINGUAGEM ALAIAS", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        frame_esquerda = ttk.LabelFrame(main_frame, text="Código Fonte", padding="10")
        frame_esquerda.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        
        # Área de texto para código
        self.texto_codigo = scrolledtext.ScrolledText(frame_esquerda, width=50, height=25, 
                                                     font=('Consolas', 10))
        self.texto_codigo.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        # Botões de arquivo
        frame_botoes_arquivo = ttk.Frame(frame_esquerda)
        frame_botoes_arquivo.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        
        btn_abrir = ttk.Button(frame_botoes_arquivo, text="Abrir Arquivo", 
                              command=self.abrir_arquivo)
        btn_abrir.grid(row=0, column=0, padx=(0, 5))
        
        btn_salvar = ttk.Button(frame_botoes_arquivo, text="Salvar Arquivo", 
                               command=self.salvar_arquivo)
        btn_salvar.grid(row=0, column=1, padx=(0, 5))
        
        btn_limpar = ttk.Button(frame_botoes_arquivo, text="Limpar", 
                               command=self.limpar_codigo)
        btn_limpar.grid(row=0, column=2)
        
        # Botão de análise
        btn_analisar = ttk.Button(frame_esquerda, text="ANALISAR CÓDIGO (LÉXICO + SINTÁTICO)", 
                                 command=self.analisar_codigo, style='Accent.TButton')
        btn_analisar.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        
        # Frame da direita - Resultados
        frame_direita = ttk.LabelFrame(main_frame, text="Resultados da Análise", padding="10")
        frame_direita.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        
        # Notebook para abas
        self.notebook = ttk.Notebook(frame_direita)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Aba de tokens
        frame_tokens = ttk.Frame(self.notebook)
        self.notebook.add(frame_tokens, text="Tokens")
        
        self.texto_tokens = scrolledtext.ScrolledText(frame_tokens, width=60, height=20, 
                                                     font=('Consolas', 9))
        self.texto_tokens.grid(row=0, column=0, sticky="nsew")
        
        # Aba de erros
        frame_erros = ttk.Frame(self.notebook)
        self.notebook.add(frame_erros, text="Erros")
        
        self.texto_erros = scrolledtext.ScrolledText(frame_erros, width=60, height=20, 
                                                    font=('Consolas', 9))
        self.texto_erros.grid(row=0, column=0, sticky="nsew")
        
        # Aba de erros sintáticos
        frame_erros_sint = ttk.Frame(self.notebook)
        self.notebook.add(frame_erros_sint, text="Erros Sintáticos")
        
        self.texto_erros_sint = scrolledtext.ScrolledText(frame_erros_sint, width=60, height=20, 
                                                         font=('Consolas', 9))
        self.texto_erros_sint.grid(row=0, column=0, sticky="nsew")
        
        # Aba de árvore sintática
        frame_arvore = ttk.Frame(self.notebook)
        self.notebook.add(frame_arvore, text="Árvore Sintática")
        
        self.texto_arvore = scrolledtext.ScrolledText(frame_arvore, width=60, height=20, 
                                                     font=('Consolas', 9))
        self.texto_arvore.grid(row=0, column=0, sticky="nsew")
        
        frame_stats = ttk.Frame(self.notebook)
        self.notebook.add(frame_stats, text="Estatísticas")

        self.texto_stats = scrolledtext.ScrolledText(frame_stats, width=60, height=20, 
                                                    font=('Consolas', 9))
        self.texto_stats.grid(row=0, column=0, sticky="nsew")
        
        frame_status = ttk.Frame(main_frame)
        frame_status.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.label_status = tk.Label(frame_status, text="Pronto para análise", 
                                    bg='#f0f0f0', fg='#27ae60', font=('Arial', 10))
        self.label_status.grid(row=0, column=0, sticky="w")
        
        frame_esquerda.columnconfigure(0, weight=1)
        frame_esquerda.rowconfigure(0, weight=1)
        frame_direita.columnconfigure(0, weight=1)
        frame_direita.rowconfigure(0, weight=1)
        frame_tokens.columnconfigure(0, weight=1)
        frame_tokens.rowconfigure(0, weight=1)
        frame_erros.columnconfigure(0, weight=1)
        frame_erros.rowconfigure(0, weight=1)
        frame_erros_sint.columnconfigure(0, weight=1)
        frame_erros_sint.rowconfigure(0, weight=1)
        frame_arvore.columnconfigure(0, weight=1)
        frame_arvore.rowconfigure(0, weight=1)
        frame_stats.columnconfigure(0, weight=1)
        frame_stats.rowconfigure(0, weight=1)
        
        self.carregar_exemplo()
    
    def carregar_exemplo(self):
        """
        Carrega um exemplo de código na interface.
        """
        exemplo = """als

-- Declaração de variáveis
intn idade
intn peso
den altura

-- Função para calcular situação
func verificarSituacao()
    cdt [ idade ge 18 and peso gt 50 ]
        wrt "Apto para atividade"
    !cdt+ [ idade lt 18 or peso le 50 ]
        wrt "Verificar com responsável"
    !cdt
        wrt "Situação indefinida"

-- Programa principal
input(idade)
input(peso)
input(altura)

cdt [ idade ge 18 and idade lt 80 ]
    wrt "Idade válida"
    verificarSituacao()
!cdt
    wrt "Idade fora do intervalo"

wrt "Análise concluída"
"""
        self.texto_codigo.delete('1.0', tk.END)
        self.texto_codigo.insert('1.0', exemplo)
    
    def abrir_arquivo(self):
        """
        Abre um arquivo de código.
        """
        arquivo = filedialog.askopenfilename(
            title="Abrir arquivo de código",
            filetypes=[("Arquivos ALAIAS", "*.als"), ("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                self.texto_codigo.delete('1.0', tk.END)
                self.texto_codigo.insert('1.0', conteudo)
                self.label_status.config(text=f"Arquivo carregado: {os.path.basename(arquivo)}", fg='#27ae60')
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir arquivo: {str(e)}")
    
    def salvar_arquivo(self):
        """
        Salva o código atual em um arquivo.
        """
        arquivo = filedialog.asksaveasfilename(
            title="Salvar arquivo",
            defaultextension=".als",
            filetypes=[("Arquivos ALAIAS", "*.als"), ("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(self.texto_codigo.get('1.0', tk.END))
                self.label_status.config(text=f"Arquivo salvo: {os.path.basename(arquivo)}", fg='#27ae60')
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")
    
    def limpar_codigo(self):
        # Limpa o código fonte e os resultados
        self.texto_codigo.delete('1.0', tk.END)
        self.texto_tokens.delete('1.0', tk.END)
        self.texto_erros.delete('1.0', tk.END)
        self.texto_erros_sint.delete('1.0', tk.END)
        self.texto_arvore.delete('1.0', tk.END)
        self.texto_stats.delete('1.0', tk.END)
        self.label_status.config(text="Código limpo", fg='#27ae60')
    
    def analisar_codigo(self):
        # analisa o código fonte atual na interface gráfica (léxico + sintático)

        codigo = self.texto_codigo.get('1.0', tk.END).strip()
        
        if not codigo:
            messagebox.showwarning("Aviso", "Por favor, insira um código para análise.")
            return
        
        try:
            # Análise completa (léxica + sintática)
            self.label_status.config(text="Analisando código (léxico + sintático)...", fg='#f39c12')
            self.root.update()
            
            self.tokens_atuais, self.arvore_sintatica, self.erros_sintaticos = self.analisador.analisar_completo(codigo)
            
            # Atualizar resultados
            self.atualizar_tokens()
            self.atualizar_erros()
            self.atualizar_erros_sintaticos()
            self.atualizar_arvore_sintatica()
            self.atualizar_estatisticas()
            
            # Status final
            stats = self.analisador.obter_estatisticas(self.tokens_atuais)
            erros_lexicos = stats['total_erros']
            erros_sint = len(self.erros_sintaticos)
            total_erros = erros_lexicos + erros_sint
            
            if total_erros > 0:
                self.label_status.config(text=f"Análise concluída com {erros_lexicos} erro(s) léxico(s) e {erros_sint} erro(s) sintático(s)", fg='#e74c3c')
            else:
                self.label_status.config(text="Análise concluída com sucesso! Código léxica e sintaticamente correto.", fg='#27ae60')
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a análise: {str(e)}")
            self.label_status.config(text="Erro na análise", fg='#e74c3c')
    
    def atualizar_tokens(self):
        self.texto_tokens.delete('1.0', tk.END)
        
        resultado = ""
        for token in self.tokens_atuais:
            if token.tipo != TokenType.EOF:
                resultado += str(token) + "\n"
        
        self.texto_tokens.insert('1.0', resultado)
    
    def atualizar_erros(self):

        self.texto_erros.delete('1.0', tk.END)
        
        erros = [token for token in self.tokens_atuais if token.eh_erro]
        
        if not erros:
            self.texto_erros.insert('1.0', "Nenhum erro encontrado! O código está sintaticamente correto.")
        else:
            resultado = "ERROS ENCONTRADOS:\n\n"
            for i, erro in enumerate(erros, 1):
                resultado += f"{i}. {str(erro)}\n\n"
            
            resultado += "\nTIPOS DE ERROS DETECTÁVEIS:\n"
            resultado += "• Programa deve começar com a palavra reservada 'als'\n"
            resultado += "• Incompatibilidade de tipos (ex: intn recebendo valor decimal)\n"
            resultado += "• Operadores relacionais mal formados (ex: 'e' em vez de 'eq')\n"
            resultado += "• Palavras reservadas mal formadas (ex: 'wr' em vez de 'wrt')\n"
            resultado += "• Operadores relacionais ausentes em condições (ex: [ idade 18 ])\n"
            resultado += "• Expressões lógicas mal formadas (ex: 'and' sem expressões completas)\n"
            resultado += "• Comando 'input' com sintaxe incorreta (ex: input sem parênteses)\n"
            resultado += "• Comando 'input' sem variável especificada\n"
            resultado += "• Comando 'input' com variável não declarada\n"
            resultado += "• Símbolos não pertencentes ao conjunto de símbolos terminais (@)\n"
            resultado += "• Identificadores mal formados (j@, 1a)\n"
            resultado += "• Identificadores muito longos (mais de 30 caracteres)\n"
            resultado += "• Números mal formados (2.a3)\n"
            resultado += "• Números muito longos (mais de 15 dígitos)\n"
            resultado += "• Strings não fechadas (\"hello world)\n"
            resultado += "• Caracteres não reconhecidos\n"
            resultado += "\nOPERADORES LÓGICOS SUPORTADOS:\n"
            resultado += "• 'and' - E lógico (ex: [ idade ge 18 and idade lt 80 ])\n"
            resultado += "• 'or' - OU lógico (ex: [ idade lt 18 or idade ge 65 ])\n"
            
            self.texto_erros.insert('1.0', resultado)
    
    def atualizar_erros_sintaticos(self):
        """Atualiza a aba de erros sintáticos."""
        self.texto_erros_sint.delete('1.0', tk.END)
        
        if not self.erros_sintaticos:
            self.texto_erros_sint.insert('1.0', "Nenhum erro sintático encontrado! O código está sintaticamente correto.")
        else:
            resultado = "ERROS SINTÁTICOS ENCONTRADOS:\n\n"
            for i, erro in enumerate(self.erros_sintaticos, 1):
                resultado += f"{i}. {str(erro)}\n\n"
            
            resultado += "\nTIPOS DE ERROS SINTÁTICOS DETECTÁVEIS:\n"
            resultado += "• Programa deve começar com 'als'\n"
            resultado += "• Comandos incompletos ou mal formados\n"
            resultado += "• Parênteses não balanceados\n"
            resultado += "• Colchetes não balanceados\n"
            resultado += "• Estruturas condicionais mal formadas\n"
            resultado += "• Estruturas de repetição mal formadas\n"
            resultado += "• Expressões incompletas ou inválidas\n"
            resultado += "• Declarações de variáveis incorretas\n"
            resultado += "• Atribuições mal formadas\n"
            resultado += "• Comandos input/output mal formados\n"
            resultado += "• Ordem incorreta de comandos\n"
            
            resultado += "\nESTRUTURAS SINTÁTICAS SUPORTADAS:\n"
            resultado += "• Programa: als + lista de comandos\n"
            resultado += "• Declaração: tipo identificador\n"
            resultado += "• Atribuição: identificador <= expressão\n"
            resultado += "• Input: input(identificador)\n"
            resultado += "• Output: wrt expressão\n"
            resultado += "• Condicional: cdt [condição] comandos (!cdt+ [condição] comandos)* (!cdt comandos)?\n"
            resultado += "• Repetição: cycle/during [condição] comandos | repeat identificador in valor comandos\n"
            resultado += "• Expressões: suporte a operadores matemáticos, relacionais e lógicos\n"
            
            self.texto_erros_sint.insert('1.0', resultado)
    
    def atualizar_arvore_sintatica(self):
        """Atualiza a aba da árvore sintática."""
        self.texto_arvore.delete('1.0', tk.END)
        
        if not self.arvore_sintatica:
            self.texto_arvore.insert('1.0', "Nenhuma árvore sintática gerada devido a erros.")
        else:
            resultado = "ÁRVORE SINTÁTICA GERADA:\n"
            resultado += "=" * 50 + "\n\n"
            resultado += str(self.arvore_sintatica)
            
            resultado += "\n\nEXPLICAÇÃO DA ÁRVORE SINTÁTICA:\n"
            resultado += "-" * 40 + "\n"
            resultado += "• PROGRAMA: Nó raiz que representa todo o programa\n"
            resultado += "• INICIO: Palavra reservada 'als'\n"
            resultado += "• LISTA_COMANDOS: Sequência de comandos do programa\n"
            resultado += "• DECLARACAO_VARIAVEL: Declaração de variável (tipo + identificador)\n"
            resultado += "• ATRIBUICAO: Atribuição de valor (identificador <= expressão)\n"
            resultado += "• COMANDO_INPUT: Comando de entrada input(variável)\n"
            resultado += "• COMANDO_OUTPUT: Comando de saída wrt expressão\n"
            resultado += "• ESTRUTURA_CONDICIONAL: Estrutura if/else (cdt/!cdt)\n"
            resultado += "• ESTRUTURA_REPETICAO: Estruturas de loop (cycle/during/repeat)\n"
            resultado += "• EXPRESSAO_*: Expressões matemáticas, relacionais e lógicas\n"
            resultado += "• VALOR_*: Valores literais (inteiros, reais, texto, lógicos)\n"
            resultado += "• IDENTIFICADOR: Nomes de variáveis\n"
            
            self.texto_arvore.insert('1.0', resultado)
    
    def atualizar_estatisticas(self):
        """Atualiza a aba de estatísticas com informações léxicas e sintáticas."""
        self.texto_stats.delete('1.0', tk.END)
        
        stats = self.analisador.obter_estatisticas(self.tokens_atuais)
        
        resultado = "ESTATÍSTICAS DA ANÁLISE LÉXICA E SINTÁTICA\n"
        resultado += "=" * 60 + "\n\n"
        
        # Estatísticas léxicas
        resultado += "ANÁLISE LÉXICA:\n"
        resultado += "-" * 20 + "\n"
        resultado += f"Total de tokens encontrados: {stats['total_tokens']}\n"
        resultado += f"Tokens válidos: {stats['tokens_validos']}\n"
        resultado += f"Erros léxicos encontrados: {stats['total_erros']}\n\n"
        
        if stats['total_tokens'] > 0:
            porcentagem_sucesso = (stats['tokens_validos'] / stats['total_tokens']) * 100
            resultado += f"Taxa de sucesso léxica: {porcentagem_sucesso:.1f}%\n\n"
        
        # Estatísticas sintáticas
        resultado += "ANÁLISE SINTÁTICA:\n"
        resultado += "-" * 20 + "\n"
        resultado += f"Erros sintáticos encontrados: {len(self.erros_sintaticos)}\n"
        if self.arvore_sintatica:
            resultado += "Árvore sintática: Gerada com sucesso\n"
            # Conta nós na árvore
            num_nos = self._contar_nos_arvore(self.arvore_sintatica)
            resultado += f"Número de nós na árvore: {num_nos}\n"
        else:
            resultado += "Árvore sintática: Não gerada devido a erros\n"
        
        resultado += "\n"
        
        # Estatísticas gerais
        total_erros = stats['total_erros'] + len(self.erros_sintaticos)
        resultado += "RESUMO GERAL:\n"
        resultado += "-" * 15 + "\n"
        resultado += f"Total de erros (léxicos + sintáticos): {total_erros}\n"
        
        if total_erros == 0:
            resultado += "✓ Código totalmente correto!\n\n"
        else:
            resultado += "✗ Código contém erros que precisam ser corrigidos\n\n"
        
        resultado += "DISTRIBUIÇÃO DE TOKENS LÉXICOS:\n"
        resultado += "-" * 35 + "\n"
        
        for tipo, quantidade in sorted(stats['tipos_tokens'].items()):
            resultado += f"{tipo:<25}: {quantidade:>3}\n"
        
        self.texto_stats.insert('1.0', resultado)
    
    def _contar_nos_arvore(self, no: NoSintatico) -> int:
        """Conta recursivamente o número de nós na árvore sintática."""
        if not no:
            return 0
        
        count = 1  # Conta o nó atual
        for filho in no.filhos:
            count += self._contar_nos_arvore(filho)
        
        return count
    
    def executar(self):
        self.root.mainloop()


def main():

    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        # Modo console
        analisador = AnalisadorLexico()
        
        # Exemplo do enunciado
        exemplo = """als

-- Declaração de variáveis
intn idade
intn peso
den altura

-- Função para calcular situação
func verificarSituacao()
    cdt [ idade ge 18 and peso gt 50 ]
        wrt "Apto para atividade"
    !cdt+ [ idade lt 18 or peso le 50 ]
        wrt "Verificar com responsável"
    !cdt
        wrt "Situação indefinida"

-- Programa principal
input(idade)
input(peso)
input(altura)

cdt [ idade ge 18 and idade lt 80 ]
    wrt "Idade válida"
    verificarSituacao()
!cdt
    wrt "Idade fora do intervalo"

wrt "Análise concluída"
"""
        print("=== ANALISADOR LÉXICO - LINGUAGEM ALAIAS ===\n")
        print("CÓDIGO:")
        print(exemplo)
        print("\nTOKENS:")
        
        tokens = analisador.analisar(exemplo)
        print(analisador.imprimir_tokens(tokens))
        
        
        stats = analisador.obter_estatisticas(tokens)
        print(f"\nESTATÍSTICAS:")
        print(f"Total de tokens: {stats['total_tokens']}")
        print(f"Erros: {stats['total_erros']}")
    else:
        app = InterfaceGrafica()
        app.executar()


if __name__ == "__main__":
    main()