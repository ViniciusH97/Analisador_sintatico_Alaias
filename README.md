# Analisador Léxico e Sintático - Linguagem ALAIAS

## Descrição

Este projeto implementa um analisador léxico e sintático completo para a linguagem de programação ALAIAS, desenvolvido em Python com interface gráfica usando Tkinter. O sistema realiza análise em duas etapas: primeiro a análise léxica (identificação de tokens) e depois a análise sintática (verificação da estrutura gramatical).

## IDE Utilizada

**IDE:** Visual Studio Code (VSCode)
**Versão Python:** 3.8 ou superior
**Bibliotecas:** Todas são nativas do Python (tkinter, re, enum, dataclasses, typing)

## Estrutura do Projeto

```
Analisador_sintático_Alaias/
├── analisador.py          # Código principal com analisador léxico e sintático
├── README.md              # Este arquivo com instruções
└── exemplos/              # Arquivos de exemplo .als
    ├── exemplo_basico.als
    ├── exemplo_loops.als
    ├── programa_completo.als
    └── exemplo com erros.als
```

## Como Executar o Projeto

### Pré-requisitos
1. Python 3.8 ou superior instalado
2. Tkinter (geralmente incluído com Python)

### Passo a Passo para Execução

#### 1. Verificar Instalação do Python
Abra o Prompt de Comando (cmd) e execute:
```cmd
python --version
```
Deve retornar algo como "Python 3.x.x"

#### 2. Navegar para o Diretório do Projeto
```cmd
cd ".\Analisador_sintático_Alaias"
```

#### 3. Executar o Analisador (Interface Gráfica)
```cmd
python analisador.py
```

#### 4. Executar em Modo Console (Opcional)
```cmd
python analisador.py --console
```

## Interface Gráfica

A interface gráfica possui as seguintes funcionalidades:

### Área Principal
- **Código Fonte (Esquerda)**: Editor de texto para inserir código ALAIAS
- **Resultados (Direita)**: Cinco abas com informações da análise

### Abas de Resultado
1. **Tokens**: Lista todos os tokens identificados (análise léxica)
2. **Erros**: Lista erros léxicos encontrados
3. **Erros Sintáticos**: Lista erros de estrutura sintática
4. **Árvore Sintática**: Mostra a árvore de derivação sintática gerada
5. **Estatísticas**: Mostra estatísticas completas da análise

### Botões Disponíveis
- **Abrir Arquivo**: Carrega arquivo .als ou .txt
- **Salvar Arquivo**: Salva o código atual
- **Limpar**: Limpa editor e resultados
- **ANALISAR CÓDIGO (LÉXICO + SINTÁTICO)**: Executa análise completa

## Funcionalidades do Analisador

### Análise Léxica
#### Tokens Reconhecidos
- Palavras reservadas: `als`, `cdt`, `!cdt`, `!cdt+`, `cycle`, `during`, `repeat`, `in`, etc.
- Tipos de variáveis: `intn`, `den`, `txt`, `bln`, `crt`
- Operadores: matemáticos, lógicos, relacionais, atribuição
- Valores: inteiros, reais, strings, booleanos
- Delimitadores: parênteses, colchetes, vírgulas
- Identificadores e comentários

#### Detecção de Erros Léxicos
1. **Símbolos inválidos**: Caracteres não pertencentes à linguagem (ex: `@`)
2. **Identificadores mal formados**: 
   - Começando com número (ex: `1abc`)
   - Contendo caracteres inválidos (ex: `var@`)
3. **Identificadores muito longos**: Mais de 30 caracteres
4. **Números mal formados**: (ex: `2.a3`)
5. **Números muito longos**: Mais de 15 dígitos
6. **Strings não fechadas**: (ex: `"hello world`)
7. **Caracteres não reconhecidos**

### Análise Sintática
#### Validação de Estrutura
O analisador sintático verifica se a sequência de tokens segue a gramática da linguagem ALAIAS e constrói uma árvore sintática.

#### Detecção de Erros Sintáticos
1. **Programa incompleto**: Programa não inicia com `als`
2. **Parênteses não balanceados**: `(` sem `)` correspondente
3. **Colchetes não balanceados**: `[` sem `]` correspondente
4. **Comandos mal formados**: Estruturas incompletas ou incorretas
5. **Estruturas condicionais inválidas**: `cdt`, `!cdt+`, `!cdt` mal formados
6. **Estruturas de repetição inválidas**: `cycle`, `during`, `repeat` incorretos
7. **Expressões incompletas**: Operadores sem operandos
8. **Declarações incorretas**: Sintaxe de declaração de variáveis inválida
9. **Atribuições malformadas**: Operador `<=` mal utilizado
10. **Comandos input/output incorretos**: `input()` e `wrt` mal formados

## Regras Sintáticas (Gramática) da Linguagem ALAIAS

A linguagem ALAIAS segue uma gramática livre de contexto com as seguintes regras de produção:

### Estrutura Geral do Programa
```
Programa → 'als' ListaComandos

ListaComandos → Comando ListaComandos | ε

Comando → DeclaracaoVariavel | Atribuicao | ComandoInput | ComandoOutput |
          EstruturaCondicional | EstruturaRepeticao | ComandoBreakLine
```

### Declarações e Atribuições
```
DeclaracaoVariavel → TipoVar Identificador

TipoVar → 'intn' | 'den' | 'txt' | 'bln' | 'crt'

Atribuicao → Identificador '<=' Expressao
```

### Comandos de Entrada e Saída
```
ComandoInput → 'input' '(' Identificador ')'

ComandoOutput → 'wrt' Expressao

ComandoBreakLine → 'brkln'
```

### Estruturas Condicionais
```
EstruturaCondicional → 'cdt' '[' ExpressaoLogica ']' ListaComandos
                      ('!cdt+' '[' ExpressaoLogica ']' ListaComandos)*
                      ('!cdt' ListaComandos)?
```

### Estruturas de Repetição
```
EstruturaRepeticao → 'cycle' '[' ExpressaoLogica ']' ListaComandos |
                    'during' '[' ExpressaoLogica ']' ListaComandos |
                    'repeat' Identificador 'in' Valor ListaComandos
```

### Expressões
```
ExpressaoLogica → ExpressaoRelacional (OperadorLogico ExpressaoRelacional)*

ExpressaoRelacional → Expressao OperadorRelacional Expressao

Expressao → Termo (OperadorMatematico Termo)*

Termo → Valor | Identificador | '(' Expressao ')'

Valor → ValorInteiro | ValorReal | ValorTexto | ValorLogico

OperadorLogico → 'and' | 'or'

OperadorRelacional → 'gt' | 'eq' | 'ne' | 'lt' | 'ge' | 'le'

OperadorMatematico → '+' | '-' | '*' | '/'

ValorLogico → 'valid' | 'invalid'
```

### Elementos Terminais
```
Identificador → [a-zA-Z_][a-zA-Z0-9_]*

ValorInteiro → [0-9]+

ValorReal → [0-9]+.[0-9]+

ValorTexto → "[^"]*"

Comentario → --.*
```

## Exemplos de Código ALAIAS

### Exemplo Básico
```alaias
als

intn idade
input(idade)

cdt [ idade ge 18 ]
    wrt "Maior de idade"
!cdt
    wrt "Menor de idade"
```

### Exemplo com Estruturas de Repetição
```alaias
als

intn i
intn contador

repeat i in 5
    wrt "Executando i vezes"
brkln

contador <= 1
during [ contador le 5 ]
    wrt "Contador: "
    wrt contador
    contador <= contador + 1
```

### Programa Completo (Sintaticamente Correto)
```alaias
als

-- Programa completo demonstrando recursos da linguagem ALAIAS

-- Declaração de variáveis
intn idade
txt nome
bln adulto
den salario

-- Atribuições
nome <= "João Silva"
idade <= 25
salario <= 3500.75

-- Estrutura condicional
cdt [ idade ge 18 ]
    adulto <= valid
    wrt "Pessoa adulta"
    
    cdt [ salario gt 3000.0 ]
        wrt "Salário bom"
    !cdt+ [ salario gt 1500.0 ]
        wrt "Salário médio"
    !cdt
        wrt "Salário baixo"
!cdt
    adulto <= invalid
    wrt "Pessoa menor de idade"

-- Estrutura de repetição
intn contador
contador <= 1

during [ contador le 5 ]
    wrt "Contador: "
    wrt contador
    contador <= contador + 1
    brkln

-- Repetição com range fixo
repeat contador in 3
    wrt "Repetição número "
    wrt contador
    brkln

wrt "Programa finalizado"
```

### Exemplo com Erros (Para Teste)
```alaias
als

intn 1abc -- Erro: Identificador mal formado
txt nome @ -- Erro: Símbolo inválido
input idade -- Erro: Sintaxe incorreta (sem parênteses)
cdt [ idade 18 ] -- Erro: Operador relacional ausente
    wrt "teste"
repeat sem_in 5 -- Erro: Falta palavra 'in'
    wrt "erro"
```

## Principais Erros Tratados pelo Analisador Sintático

### 1. Erros de Estrutura do Programa
- **Programa sem início**: Código que não começa com `als`
- **Estrutura incompleta**: Comandos não finalizados corretamente

### 2. Erros de Delimitadores
- **Parênteses desbalanceados**: `(` sem `)` correspondente ou vice-versa
- **Colchetes desbalanceados**: `[` sem `]` correspondente ou vice-versa

### 3. Erros em Estruturas Condicionais
- **Condição mal formada**: `cdt` sem `[condição]`
- **Expressão condicional inválida**: Operadores relacionais ausentes
- **Estrutura `!cdt+` incorreta**: Senão-se mal formado
- **Estrutura `!cdt` incorreta**: Senão mal posicionado

### 4. Erros em Estruturas de Repetição
- **`repeat` mal formado**: Falta palavra `in` (ex: `repeat i 5`)
- **`cycle` sem condição**: `cycle` sem `[condição]`
- **`during` sem condição**: `during` sem `[condição]`

### 5. Erros em Comandos
- **Input mal formado**: `input` sem parênteses ou sem variável
- **Output incompleto**: `wrt` sem expressão
- **Declaração incorreta**: Tipo de variável sem identificador
- **Atribuição inválida**: Identificador sem `<=` ou sem valor

### 6. Erros de Expressões
- **Expressão matemática incompleta**: Operador sem operandos
- **Expressão relacional inválida**: Comparação sem operador relacional
- **Expressão lógica mal formada**: `and`/`or` sem expressões completas

### 7. Erros de Sintaxe Geral
- **Token inesperado**: Símbolo que não inicia comando válido
- **Comando incompleto**: Estrutura iniciada mas não finalizada
- **Ordem incorreta**: Comandos fora da sequência esperada

## Outras Informações Relevantes sobre a Implementação

### Arquitetura do Sistema
O analisador foi implementado seguindo o modelo tradicional de compiladores:

1. **Analisador Léxico (`AnalisadorLexico`)**: 
   - Converte texto em tokens
   - Detecta erros de formação de tokens
   - Valida limites (identificadores e números)

2. **Analisador Sintático (`AnalisadorSintatico`)**:
   - Analisa sequência de tokens
   - Constrói árvore sintática
   - Detecta erros de estrutura

3. **Interface Gráfica (`InterfaceGrafica`)**:
   - Apresenta resultados de forma organizada
   - Permite interação com o usuário
   - Exibe árvore sintática e estatísticas

### Técnicas Utilizadas

#### Análise Léxica
- **Expressões regulares**: Para reconhecimento de padrões
- **Autômatos finitos**: Implementação implícita via regex
- **Validação semântica básica**: Verificação de tipos e limites

#### Análise Sintática
- **Análise descendente recursiva**: Método top-down
- **Gramática LL(1)**: Estrutura de gramática livre de contexto
- **Árvore sintática concreta**: Representação da estrutura do programa
- **Validação de delimitadores**: Verificação de balanceamento

### Características Especiais

1. **Análise integrada**: Léxica e sintática em uma única execução
2. **Recuperação de erros**: Sistema continua análise após encontrar erro
3. **Mensagens detalhadas**: Erros com linha, coluna e descrição específica
4. **Árvore sintática visual**: Representação hierárquica da estrutura
5. **Estatísticas completas**: Métricas de análise em tempo real

### Limitações e Extensões Futuras

#### Limitações Atuais
- Análise semântica limitada (apenas tipos básicos)
- Não há otimização de código
- Escopo de variáveis não implementado completamente

#### Possíveis Extensões
- Análise semântica completa
- Geração de código intermediário
- Otimizações sintáticas
- Suporte a funções definidas pelo usuário
- Sistema de módulos/imports

## Solução de Problemas

### Erro: "Python não é reconhecido"
1. Verifique se Python está instalado
2. Adicione Python ao PATH do sistema
3. Reinicie o prompt de comando

### Erro: "tkinter não encontrado"
- No Windows: Reinstalar Python marcando "tcl/tk and IDLE"
- No Linux: `sudo apt install python3-tk`

### Interface não abre
1. Verifique se está executando `python analisador.py` (sem --console)
2. Verifique se tkinter está funcionando: `python -c "import tkinter; tkinter.Tk()"`

## Comandos Resumidos

```cmd
# Navegar para o projeto
cd ".\Analisador_sintático_Alaias"

# Executar interface gráfica (análise léxica + sintática)
python analisador.py

# Executar em modo console
python analisador.py --console
```

## Recursos da Interface

- **Syntax highlighting**: Código com fonte monoespaçada para melhor legibilidade
- **Abas organizadas**: Separação clara entre tokens, erros léxicos, erros sintáticos, árvore e estatísticas
- **Contadores em tempo real**: Estatísticas atualizadas automaticamente
- **Status bar**: Feedback visual do estado da análise
- **Gerenciamento de arquivos**: Abrir/salvar arquivos .als
- **Exemplo integrado**: Código de exemplo carregado automaticamente
- **Árvore sintática visual**: Representação hierárquica da estrutura do programa

## Estatísticas Fornecidas

### Análise Léxica
- Total de tokens encontrados
- Número de tokens válidos
- Número de erros léxicos
- Taxa de sucesso da análise léxica
- Distribuição por tipo de token

### Análise Sintática
- Número de erros sintáticos encontrados
- Status da árvore sintática (gerada/não gerada)
- Número de nós na árvore sintática
- Resumo geral de correção do código

### Resumo Integrado
- Total de erros (léxicos + sintáticos)
- Status final do código (correto/incorreto)
- Estatísticas combinadas das duas análises
