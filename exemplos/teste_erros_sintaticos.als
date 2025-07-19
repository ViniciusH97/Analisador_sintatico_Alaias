als

-- Arquivo de teste para ERROS SINTÁTICOS
-- Este arquivo contém propositalmente vários erros sintáticos

-- Erro 1: Declaração incompleta (falta identificador)
intn 

-- Erro 2: Atribuição sem operador
numero valor

-- Erro 3: Comando input mal formado (sem parênteses)
input idade

-- Erro 4: Comando input sem variável
input()

-- Erro 5: Estrutura condicional sem colchetes
cdt numero gt 18
    wrt "Maior de idade"

-- Erro 6: Colchetes não fechados
cdt [ idade ge 18
    wrt "Teste"

-- Erro 7: Parênteses não fechados
input(nome

-- Erro 8: Estrutura repeat sem 'in'
repeat contador 5
    wrt "Erro"

-- Erro 9: Expressão incompleta
intn resultado
resultado <= 10 +

-- Erro 10: Operador relacional ausente
cdt [ idade 18 ]
    wrt "Erro de operador"

-- Erro 11: Comando wrt sem expressão
wrt

-- Erro 12: Estrutura during sem condição
during
    wrt "Erro"

-- Erro 13: Atribuição sem valor
intn teste
teste <=

-- Erro 14: Estrutura !cdt+ sem condição
cdt [ idade gt 18 ]
    wrt "Maior"
!cdt+
    wrt "Erro aqui"

-- Erro 15: Parênteses extra sem abertura
wrt "teste")

-- Erro 16: Colchetes extra sem abertura
cdt teste ]
    wrt "erro"
