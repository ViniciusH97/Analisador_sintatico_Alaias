-- Arquivo de teste para ERROS LÉXICOS
-- Este arquivo contém propositalmente vários erros léxicos
-- NOTA: Este arquivo NÃO começa com 'als' propositalmente
als
-- Erro 1: Identificador começando com número
intn 1variavel

-- Erro 2: Identificador com símbolos inválidos
txt nome@usuario
txt email#teste
den valor$preco

-- Erro 3: Números mal formados
intn numero1 <= 2.a3
den numero2 <= 1.2.3
intn numero3 <= 123abc

-- Erro 4: Strings não fechadas
txt mensagem1 <= "Esta string não tem fechamento
txt mensagem2 <= "Outra string sem fim

-- Erro 5: Símbolos não pertencentes à linguagem
intn teste @ valor
txt nome $ "teste"
den preco & 10.5

-- Erro 6: Identificadores muito longos (mais de 30 caracteres)
intn minha_variavel_com_nome_muito_muito_muito_longo_demais

-- Erro 7: Números muito longos (mais de 15 dígitos)
intn numero_gigante <= 123456789012345678901234567890

-- Erro 8: Palavras reservadas mal formadas
wr "Deveria ser wrt"
inp(idade)
cd [ idade gt 18 ]
    wrt "teste"

-- Erro 9: Operadores relacionais mal formados
cdt [ idade e 18 ]
    wrt "Deveria ser eq"

cdt [ valor g 10 ]
    wrt "Deveria ser gt"

-- Erro 10: Caracteres não reconhecidos
intn valor ~ 10
txt nome % "teste"
den preco § 15.5

-- Mistura de erros léxicos e sintáticos
intn 2teste <= "string mal formada
cdt [ 3variavel e valor@ ]
    wr "múltiplos erros
!cdt
    inp teste)
