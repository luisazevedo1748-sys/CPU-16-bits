# RAM — memória de dados 16 × 16 bits

Ficheiro: `RAM.dig`

## Propósito

Memória de dados do processador. Guarda 16 palavras de 16 bits, endereçáveis de
0 a 15, com uma porta de leitura e uma de escrita partilhadas pelo mesmo
endereço.

É o bloco que tira os dados do programa de dentro dos 4 registos do banco. Sem
ele, um programa só pode manipular quatro valores de cada vez.

## Interface

| Pino | Direção | Bits | Função |
|---|---|---|---|
| `Adress` | entrada | 4 | palavra a ler ou a escrever |
| `WE` | entrada | 1 | 1 = escreve no flanco do relógio |
| `Clk` | entrada | 1 | relógio |
| `Data_In` | entrada | 16 | palavra a escrever |
| `Data_Out` | saída | 16 | palavra lida, sempre válida |

Ordem dos pinos no símbolo, de cima para baixo: `Adress`, `WE`, `Clk`,
`Data_In`, com o `Data_Out` do lado direito ao meio.

A leitura é combinatória e não depende do `WE`: o `Data_Out` mostra sempre a
palavra do endereço atual. A escrita é síncrona e só acontece com `WE`=1.

Durante uma escrita, o `Data_Out` mostra a palavra antiga até ao flanco.

## Funcionamento

O `Adress` entra num descodificador que acende exatamente uma de 16 linhas
one-hot. Cada linha faz duas coisas:

**Na escrita**, entra numa porta E junto com o `WE`. A saída dessa porta vai ao
`EN` do registo correspondente. Só o registo endereçado fica habilitado, e só
quando `WE` está ativo.

**Na leitura**, vai direta ao `Enable` do tristate desse registo. Sem passar pelo
`WE`, porque ler não depende de escrever.

O `Data_In` e o `Clk` ligam aos 16 registos em paralelo. Quem decide onde se
escreve é o endereço, não o barramento de dados.

### O barramento de saída

As 16 saídas dos tristates ligam **ao mesmo fio**, que é o `Data_Out`. Parece
errado e é a única parte deliberadamente assim.

Funciona por causa do terceiro estado. Um tristate desligado não força 0 — fica
em alta impedância, `Z`, eletricamente desligado do fio. Como o descodificador
garante que só uma linha está ativa, só um tristate conduz de cada vez e os
outros quinze não interferem.

Com portas normais isto seria um curto-circuito: duas saídas no mesmo fio, uma a
0 e outra a 1.

### Porquê tristates e não muxes

O `register_file` usa muxes para escolher a saída, e com 4 palavras isso faz
sentido. Com 16, um mux 16:1 de 16 bits seria muito mais hardware do que 16
tristates. O barramento escala melhor, e é o que a memória real usa.

## Estrutura

| Quantos | Componente |
|---|---|
| 16 | `Registro_16bits` |
| 16 | `tristate_16bits` |
| 16 | porta E de 2 entradas |
| 1 | `Decoder` nativo com `Bits de seleção` = 4 |

O esquema está organizado em 16 linhas, uma por palavra, de cima para baixo. Em
cada linha, da esquerda para a direita: porta E, registo, tristate.

Total de 256 flip-flops D, quatro vezes o `register_file`.

## Notas

**Registos sem reset.** Usa-se o `Registro_16bits` simples, não a versão com
reset. Memória de dados não se limpa no arranque — se limpasse, perdia o que lá
estivesse, e o ponto de ter memória é guardar coisas. Nenhum computador real
apaga a RAM ao ligar. Os 16 registos arrancam com valores indefinidos, e cabe ao
programa escrever antes de ler.

**É SRAM, não DRAM.** A memória principal de um PC é DRAM: um transístor e um
condensador por bit, densa mas com necessidade de refresh. Dentro de um
processador não há DRAM nenhuma — registos, caches e buffers são todos SRAM. Esta
implementação é SRAM feita de flip-flops D, que é mais hardware por bit do que as
células de 6 transístores da SRAM real, mas é a forma digital pura de fazer a
mesma coisa e a única viável no Digital.

**Protótipo de 4 palavras.** Foi construída e validada primeiro uma versão de 4
palavras com endereço de 2 bits, antes de replicar para 16. Com 256 flip-flops
por baixo, procurar um erro de ligação na versão grande sem ter a pequena
validada seria doloroso.

**Hierarquia não se aplica.** A tentação de fazer 16 palavras a partir de quatro
blocos de 4 não compensa: cada bloco daria o seu `Data_Out` próprio, e juntá-los
exigiria um mux de nível superior mais um segundo descodificador. Acrescentava
hardware para desfazer a hierarquia. Em memórias maiores a divisão em bancos
volta a fazer sentido, mas não a esta escala.

## Teste

Escrever valores diferentes e reconhecíveis nas 16 posições — por exemplo o
próprio número do endereço — e só depois percorrer os endereços a ler. Escrever
e ler uma posição de cada vez não apanha duas linhas do descodificador trocadas.

Confirmar também que com `WE`=0 uma mudança no `Data_In` não altera nada.

## Ligação ao processador

A RAM vive no `CPU.dig`, ao lado do `datapath` e não dentro dele. O endereço
vem do `RegA_Out` cortado aos 4 bits de baixo, o dado a escrever vem do
`RegB_Out`, e o `Data_Out` entra num multiplexador que escolhe entre a palavra
lida e o imediato antes de chegar ao `Data_In` do `datapath`.

Detalhes em `../cpu/CPU.md`.

## Nota de nomenclatura

Na biblioteca do Digital o ficheiro está guardado como `RAM 16x16 bits.dig`,
com espaços no nome. Passou a `RAM.dig` na passagem lib→repo, corrigindo a
string `<elementName>` no `CPU.dig`.
