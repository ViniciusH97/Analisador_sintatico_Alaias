als

-- Teste específico para ESTRUTURAS DE REPETIÇÃO
-- Este arquivo testa todas as variações de loops da linguagem ALAIAS

-- Declaração de variáveis para os testes
intn contador
intn limite
intn valor

-- Inicialização
contador <= 1
limite <= 10
valor <= 0

-- Teste 1: REPEAT com valor fixo
wrt "=== Teste REPEAT ==="
repeat contador in 5
    wrt "Iteração repeat: "
    wrt contador
    brkln

-- Teste 2: DURING (enquanto)
wrt "=== Teste DURING ==="
contador <= 1
during [ contador le 3 ]
    wrt "Contador during: "
    wrt contador
    contador <= contador + 1
    brkln

-- Teste 3: CYCLE (para)
wrt "=== Teste CYCLE ==="
contador <= 1
cycle [ contador le 4 ]
    wrt "Contador cycle: "
    wrt contador
    contador <= contador + 1

-- Teste 4: Loops aninhados
wrt "=== Teste LOOPS ANINHADOS ==="
intn i
intn j
i <= 1

during [ i le 2 ]
    wrt "Loop externo i: "
    wrt i
    j <= 1
    
    cycle [ j le 2 ]
        wrt "  Loop interno j: "
        wrt j
        j <= j + 1
    
    i <= i + 1
    brkln

-- Teste 5: Repeat com diferentes valores
wrt "=== Teste REPEAT com valores diferentes ==="
repeat valor in 1
    wrt "Uma vez"

repeat valor in 3
    wrt "Três vezes - iteração: "
    wrt valor

-- Teste 6: Condições complexas em loops
wrt "=== Teste CONDIÇÕES COMPLEXAS ==="
contador <= 1
during [ contador lt 5 and contador gt 0 ]
    wrt "Condição complexa: "
    wrt contador
    contador <= contador + 1

-- Teste 7: Loop com estruturas condicionais internas
wrt "=== Teste LOOP com IF interno ==="
contador <= 1
cycle [ contador le 4 ]
    cdt [ contador eq 2 ]
        wrt "Contador especial: 2"
    !cdt
        wrt "Contador normal: "
        wrt contador
    
    contador <= contador + 1

wrt "Todos os testes de repetição concluídos!"
