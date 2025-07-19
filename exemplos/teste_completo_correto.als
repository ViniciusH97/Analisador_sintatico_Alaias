als

-- Programa de teste completo - SINTATICAMENTE CORRETO
-- Este arquivo testa todas as funcionalidades da linguagem ALAIAS

-- Declarações de variáveis de todos os tipos
intn numero
den decimal
txt texto
bln logico
crt caractere

-- Atribuições básicas
numero <= 42
decimal <= 3.14159
texto <= "Olá, mundo!"
logico <= valid
caractere <= "A"

-- Comando de entrada
input(numero)
input(texto)

-- Estrutura condicional simples
cdt [ numero gt 0 ]
    wrt "Número positivo"
!cdt
    wrt "Número não positivo"

-- Estrutura condicional complexa com senão-se
cdt [ numero gt 100 ]
    wrt "Número grande"
!cdt+ [ numero gt 50 ]
    wrt "Número médio"
!cdt+ [ numero gt 0 ]
    wrt "Número pequeno"
!cdt
    wrt "Número inválido"

-- Estruturas de repetição
intn contador
contador <= 1

-- Loop during (enquanto)
during [ contador le 5 ]
    wrt "Contador during: "
    wrt contador
    contador <= contador + 1
    brkln

-- Loop cycle (para)
contador <= 1
cycle [ contador le 3 ]
    wrt "Contador cycle: "
    wrt contador
    contador <= contador + 1

-- Loop repeat (repetição fixa)
repeat contador in 4
    wrt "Repetição número: "
    wrt contador
    brkln

-- Expressões matemáticas complexas
intn resultado
resultado <= numero + decimal * 2 - 1

-- Expressões lógicas complexas
cdt [ numero ge 10 and numero le 100 or logico eq valid ]
    wrt "Condição complexa verdadeira"
!cdt
    wrt "Condição complexa falsa"

-- Aninhamento de estruturas
cdt [ numero gt 0 ]
    cdt [ decimal gt 0.0 ]
        wrt "Ambos positivos"
        during [ contador lt 2 ]
            wrt "Loop aninhado"
            contador <= contador + 1
    !cdt
        wrt "Decimal não positivo"
!cdt
    wrt "Número não positivo"

wrt "Programa executado com sucesso!"
