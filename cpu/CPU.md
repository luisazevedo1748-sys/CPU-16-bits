# CPU 16 bits — nível de topo

Ficheiro: `CPU.dig` (guardado como `Unidade_de_controlo.dig`)

Nível onde a máquina inteira se junta: memória de instruções, registo de
instrução, contador de programa, descodificação, caminho de dados, memória de
dados, pilha e arranque automático.

Estado: **completo e validado.** Aritmética, lógica, memória, saltos
condicionais, pilha, chamadas de função e paragem.

---

## 1. Conteúdo

```
CPU.dig
 ├── ROM                    memória de instruções, 256 palavras úteis
 ├── Registo16bits_reset    o IR (registo de instrução)
 ├── program_counter        com pino EN exposto para o HLT
 ├── Decoder 4→16           descodificador primário, túneis D0..D15
 ├── Decoder 3→8            descodificador secundário, túneis F0..F7
 ├── 6 portas AND           combinam D0 com Fn, túneis S1..S6
 ├── datapath               banco de registos + ALU + mux de write-back
 ├── RAM 16x16 bits         memória de dados
 ├── Registro_16bits (SP)   apontador de pilha + Add + 2 muxes
 ├── Registro_16bits (HI)   segura o Out_HI/Rest da MDU
 ├── Counter nativo         gerador de reset de arranque
 ├── 6 multiplexadores      escolha de fonte nos pontos de convergência
 └── 15 splitters           extração e montagem de campos
```

Inventário: 10 AND, 17 OR, 3 NOT, 2 decoders, 6 muxes, 15 splitters, 134 túneis.

### Porque é que a RAM está aqui e não dentro do `datapath`

Nos processadores reais a memória é um bloco separado do caminho de dados,
precisamente porque mais tarde se substitui por uma cache ou se liga a um
barramento externo. Além disso evita revalidar um ficheiro já testado.

O `datapath` teve de ganhar dois pinos de saída: `RegA_Out` e `RegB_Out`, que
expõem as duas portas de leitura do banco de registos.

---

## 2. Formato da instrução

```
 15 14 13 12 | 11 10  9  8  7  6 |  5  4 |  3  2 |  1  0
+------------+-------------------+-------+-------+-------+
|   opcode   |       imm6        |  WA   |  RA2  |  RA1  |   tipo R / I
+------------+---------------------------+-------+-------+
|   opcode   |          addr8            |  RA2  |  RA1  |   tipo J
+------------+----------+----------+-----+-------+-------+
|    0000    | reservado|  funct   |  WA   |  RA2  | RA1  |   tipo F
+------------+----------+----------+-------+-------+------+
                bits 11-9  bits 8-6
```

`RA1`, `RA2` e `WA` vão diretos do splitter aos pinos do `datapath`, sem lógica
pelo meio. O `addr8` sobrepõe-se ao `WA`, o que é seguro porque nos saltos
`WE`=0.

---

## 3. Instruções

### Tipo R, I e J

| Opcode | Linha | Mnemónica | Operação |
|---|---|---|---|
| `0000` | D0 | — | ver tipo F |
| `0001` | D1 | `ADD rd,ra,rb` | rd ← ra + rb |
| `0010` | D2 | `SUB rd,ra,rb` | rd ← ra − rb |
| `0011` | D3 | `MUL rd,ra,rb` | rd ← (ra × rb) baixo; alto para o HI |
| `0100` | D4 | `DIV rd,ra,rb` | rd ← ra ÷ rb; resto para o HI |
| `0101` | D5 | `SHL rd,ra,rb` | rd ← ra << rb[3:0] |
| `0110` | D6 | `SHR rd,ra,rb` | rd ← ra >> rb[3:0] |
| `0111` | D7 | `AND rd,ra,rb` | rd ← ra & rb |
| `1000` | D8 | `OR rd,ra,rb` | rd ← ra \| rb |
| `1001` | D9 | `XOR rd,ra,rb` | rd ← ra ^ rb |
| `1010` | D10 | `LOAD rd,(ra)` | rd ← RAM[ ra[3:0] ] |
| `1011` | D11 | `LDI rd,imm6` | rd ← imm6 |
| `1100` | D12 | `JMP addr8` | PC ← addr8 |
| `1101` | D13 | `BEQ ra,rb,addr8` | se ra=rb, PC ← addr8 |
| `1110` | D14 | `BNE ra,rb,addr8` | se ra≠rb, PC ← addr8 |
| `1111` | D15 | `STORE rb,(ra)` | RAM[ ra[3:0] ] ← rb |

`ra` = campo RA1, `rb` = campo RA2, `rd` = campo WA.

No `LOAD` e no `STORE` o endereço vem sempre do **RA1**, porque é o `RegA_Out`
que alimenta o `Adress` da RAM. No `STORE`, o dado vem do **RA2**.

### Tipo F, dentro do opcode `0000`

| funct | Sinal | Mnemónica | Operação |
|---|---|---|---|
| `000` | — | `NOP` | nada |
| `001` | S1 | `PUSH rb` | SP ← SP−1; RAM[SP] ← rb |
| `010` | S2 | `POP rd` | rd ← RAM[SP]; SP ← SP+1 |
| `011` | S3 | `CALL (ra)` | empilha o PC; PC ← ra |
| `100` | S4 | `RET` | PC ← topo da pilha; SP ← SP+1 |
| `101` | S5 | `MFHI rd` | rd ← HI |
| `110` | S6 | `HLT` | para o PC definitivamente |
| `111` | — | livre | |

---

## 4. O segundo nível de descodificação

Os 16 opcodes esgotaram-se quando a RAM entrou. Em vez de alargar a instrução, a
saída foi um **campo secundário**, que é o que as ISAs reais fazem — o MIPS com o
opcode `SPECIAL`, o RISC-V com os campos `funct`.

No opcode `0000` os 12 bits de baixo estavam livres: 4096 codificações
desperdiçadas numa instrução que só precisava de uma.

| Componente | Configuração |
|---|---|
| Splitter | Entrada `16`, Saída `0-5,6-8,9-15`. Entrada no `Q` do IR |
| Decoder | `Bits de seleção` = 3, `sel` ← saída `6-8` |
| Túneis | `F0` a `F7` |

### A porta de guarda

As linhas `Fn` acendem em **todas** as instruções, porque os bits 8-6 carregam
imediatos e endereços quando o opcode não é zero. Cada sub-instrução é uma porta
**AND** de `D0` com a linha `Fn`.

O `F0` nunca se usa. `funct`=`000` tem de continuar a ser `NOP`, porque o flush
do delay slot depende de `0x0000` não fazer nada.

### Limitação

Instruções tipo F não podem ter imediatos nem endereços — os bits 8-6 estão
ocupados. Só registos. Foi por isso que o `CALL` teve de ser indireto, com o
destino num registo, como o `jalr` do RISC-V.

---

## 5. A pilha

### Convenção

Cresce para baixo a partir do fim da memória. O `SP` arranca em 15.

| Operação | Endereço usado | `SP` |
|---|---|---|
| `PUSH` / `CALL` | `SP − 1`, do somador | desce |
| `POP` / `RET` | `SP`, do `Q` do registo | sobe |

O endereço e a atualização do `SP` acontecem no mesmo flanco, por isso a escrita
usa o valor **já decrementado** e a leitura o valor **ainda não incrementado**.
Este desencontro foi a origem do erro mais difícil da montagem: o `CALL` escrevia
em E e o `RET` lia de F.

Consequência: a posição 15 da RAM nunca é usada pela pilha.

### O registo `SP`

| Componente | Ligação |
|---|---|
| `Q` do `SP` | → entrada `a` do Adder de 16 bits |
| `c_in` | → Ground |
| `b` | → saída do mux `+1`/`−1` |
| mux `+1`/`−1` | entrada 0 = `1`, entrada 1 = `0xFFFF`, seletor = `OR(S1,S3)` |
| `s` do Adder | → entrada 0 do mux de reset |
| mux de reset | entrada 1 = `15`, seletor = `Reset`, saída → `D` do `SP` |
| `EN` do `SP` | → `OR(S1,S2,S3,S4,Reset)` |

O `−1` é `0xFFFF` porque em complemento para dois são 16 bits a 1. O `Reset` tem
de estar na porta do `EN`, senão o registo não captura e o 15 nunca entra.

---

## 6. O registo `HI`

A MDU sempre calculou duas coisas: na divisão o quociente e o resto, na
multiplicação os 16 bits de baixo e os 16 de cima. Só uma tinha caminho para os
registos; a outra saía no `Out_HI/Rest` e ninguém a apanhava.

**Porque é que não bastava ligar o `Out_HI/Rest` ao mux.** Essa saída é
combinatória: acompanha as entradas da MDU em tempo real. No ciclo do `MFHI` a
MDU já está a calcular com outros operandos — os campos da própria instrução
`MFHI` — e o valor anterior desapareceu.

A primeira tentativa dava sempre 0, porque `MFHI R2` tem os campos de registo a
zero e a MDU estava a dividir R0 por R0.

**A solução:** um `Registro_16bits` a segurar o valor.

| Pino | Ligação |
|---|---|
| `D` | túnel `Out_High/Rest` |
| `Clk` | relógio comum |
| `EN` | `OR(D3, D4)` — só no `MUL` e no `DIV` |
| `Q` | → entrada 2 do mux do `Data_In` |

É exatamente por isto que o MIPS tem registos `HI` e `LO`.

---

## 7. O `HLT`

O `EN` do registo interno do `program_counter` estava preso a VDD. Passou a pino
exposto, e é o único ficheiro já testado que foi preciso alterar.

### A malha de retenção

Um `HLT` que só desligasse o `EN` durante um ciclo não serviria: no ciclo
seguinte o IR já teria outra instrução, o `S6` apagava, e o PC recomeçava. O
sinal tem de se segurar a si próprio.

```
S6 ────────────┐
               ├─ OU ──▶ E ──┬──▶ NÃO ──▶ EN do program_counter
     ┌─────────┘        ▲    │
     └──────────────────┼────┘  realimentação
                        │
Reset ──▶ NÃO ──────────┘
```

**A realimentação tem de sair de depois da porta E**, não da porta OU. Se sair da
OU, o `Reset` gate a saída mas nunca limpa a malha — ela prende-se a 1 para
sempre e o `HLT` deixa de ter efeito.

| Situação | E | EN |
|---|---|---|
| arranque, `S6`=0 | 0 | 1, PC anda |
| `HLT` executa | 1 | 0, PC para |
| ciclo seguinte, `S6`=0 | 1, a malha segura | 0 |
| `Reset`=1 | 0, a malha limpa | 1 |

O `HLT` não é um ciclo — o PC fica imóvel, sem gastar ciclos. Só o reset o
liberta. É assim em todas as arquiteturas que têm a instrução.

---

## 8. Reset de arranque

Um `Counter` nativo do Digital conta os primeiros ciclos e segura o `Reset`.

| Componente | Ligação |
|---|---|
| `Counter`, `Bits`=16 | `C` ← relógio, `clr` ← Ground |
| `out` | → Splitter `16` → `0-1,1,3-15` |
| bit 2 | → porta **Não** |
| saída do Não | → `en` do `Counter` **e** → porta **Ou** com o botão `Reset` |
| saída dessa Ou | → tudo o que o `Reset` alimenta |

O contador arranca em 0, conta 0 a 3 com o reset ativo, e ao chegar a 4 o bit 2
sobe, o `en` desliga e ele congela. O reset larga nesse momento.

### Porque é que o `Counter` é nativo

A primeira versão usava o `Registro_16bits` construído de raiz. Funcionava às
vezes: um latch SR feito de transístores não tem estado inicial definido, e o
valor em que assenta depende da ordem de avaliação do simulador.

É o problema circular deste circuito — aquilo que existe para pôr a máquina num
estado conhecido arrancava ele próprio num estado desconhecido.

Nos chips reais resolve-se fora do domínio digital, com um circuito analógico que
segura o reset até a tensão de alimentação estabilizar. O Digital não simula
tensões, portanto não há equivalente construível. **É por isso que esta é uma
exceção defensável ao "de raiz": não é lógica que tenha sido evitada, é lógica
que não pode existir.**

O `sel` da ROM e o `EN` do IR estão ligados a VDD — não há razão para os
desligar alguma vez.

---

## 9. Sinais de controlo

| Sinal | Entradas | Túneis |
|---|---|---|
| `WE` do banco | 13 | D1..D11, S2, S5 |
| `S` | 9 | D1..D9 |
| `Sub` | 3 | D2, D13, D14 |
| `MDU_op` | — | D4 direto (1 = divisão) |
| `ALU_Op[0]` | 4 | D3, D4, D6, D8 |
| `ALU_Op[1]` | 3 | D5, D6, D9 |
| `ALU_Op[2]` | 3 | D7, D8, D9 |
| `WE` da RAM | 3 | D15, S1, S3 |
| `Jump_EN` | 5 | D12, AND(D13,ZF), AND(D14,~ZF), S3, S4 |
| `IR_Reset` | 2 | Reset, Jump_EN |
| `EN` do `HI` | 2 | D3, D4 |
| `EN` do `SP` | 5 | S1, S2, S3, S4, Reset |

**Porque é que o `LOAD`, o `POP` e o `MFHI` entram no `WE` mas não no `S`:**
escrevem num registo, logo precisam de `WE`=1. Mas o valor vem do `Data_In`, não
da ALU, e dentro do `datapath` é o `S` que faz essa escolha.

**Porque é que o `STORE`, o `PUSH`, o `CALL` e o `HLT` não entram em nenhum:** não
escrevem em registo nenhum.

---

## 10. Os seis multiplexadores

### `Data_In` do `datapath` — 16 bits, 2 bits de seleção

| Entrada | Fonte | Usado por |
|---|---|---|
| 0 | imediato, do Splitter B | `LDI` |
| 1 | `Data_Out` da RAM | `LOAD`, `POP` |
| 2 | `Q` do registo `HI` | `MFHI` |
| 3 | Ground | — |

Seletor: Splitter `1,1` → `2`, bit 0 = `OR(D10,S2)`, bit 1 = `S5`.

### `Adress` da RAM — 4 bits, 2 bits de seleção

| Entrada | Fonte | Usado por |
|---|---|---|
| 0 | Splitter E, do `RegA_Out` | `LOAD`, `STORE` |
| 1 | saída do Adder do `SP`, bits 0-3 | `PUSH`, `CALL` |
| 2 | `Q` do `SP`, bits 0-3 | `POP`, `RET` |
| 3 | Ground | — |

Seletor: bit 0 = `OR(S1,S3)`, bit 1 = `OR(S2,S4)`.

### `Data_In` da RAM — 16 bits, 1 bit

Entrada 0 = `RegB_Out`, entrada 1 = `PC_Out`. Seletor: `S3`.

### `Jump_Addr` — 16 bits, 2 bits de seleção

| Entrada | Fonte | Usado por |
|---|---|---|
| 0 | Splitter D, `addr8` | `JMP`, `BEQ`, `BNE` |
| 1 | `Data_Out` da RAM | `RET` |
| 2 | `RegA_Out` | `CALL` |
| 3 | Ground | — |

Seletor: bit 0 = `S4`, bit 1 = `S3`.

### Mais dois no `SP`

O mux `+1`/`−1` e o mux de reset, descritos na secção 5.

---

## 11. Extração dos campos

| Splitter | Configuração | Fonte | Produz |
|---|---|---|---|
| campos | `12` → `2,2,2,2,4` | IR, bits 0-11 | RA1, RA2, WA |
| A | `16` → `0-5,6-11,12-15` | `Q` do IR | imediato de 6 bits |
| B | `6,10` → `16` | A + Const 10 a 0 | imediato estendido |
| C | `16` → `0-3,4-11,12-15` | `Q` do IR | endereço de 8 bits |
| D | `8,8` → `16` | C + Const 8 a 0 | endereço estendido |
| E | `16` → `0-3,4-15` | `RegA_Out` | endereço da RAM |
| funct | `16` → `0-5,6-8,9-15` | `Q` do IR | campo `funct` |
| SP | `16` → `0-3,4-15` | `Q` do `SP` | endereço de leitura da pilha |
| arranque | `16` → `0-1,1,3-15` | `Counter` | bit 2 |

As constantes de extensão a zero não são opcionais: sem elas os pinos ficam
soltos e a simulação não arranca.

Nota sobre a sintaxe do Digital: os campos da "Saída do distribuidor" são
**larguras**, não índices. `1` quer dizer um bit; a notação `0-1` quer dizer dois
bits. As etiquetas no símbolo é que mostram índices.

---

## 12. Ordem dos pinos do `datapath`

**Entradas:** `RA1`, `RA2`, `WA`, `WE`, `Data_In`, `MDU_op`, `Sub`, `ALU_Op`,
`Clk`, `S`

**Saídas:** `Flag_RZ`, `Flag_DZ`, `Flag_N`, `Flag_Z`, `OF`, `ZF`, `Cout`, `SF`,
`Out`, `Out_HI/Rest`, `RegA_Out`, `RegB_Out`

O `Data_In` subiu para quinto lugar quando as saídas novas foram acrescentadas. O
Digital ordena os pinos pela posição dos símbolos `In`/`Out` no ficheiro, e uma
alteração aí faz os fios do circuito-pai apontarem para os sítios errados. O
mesmo cuidado se aplicou ao expor o `EN` do `program_counter`: o `In` novo tem de
ficar abaixo de todos os outros.

---

## 13. O delay slot

O IR faz do processador um pipeline de dois andares:

- No flanco que fecha o ciclo *n*: `IR ← ROM[P_n]` e `PC ← salto ? destino : P_n+1`
- A instrução que executa no ciclo *n* é `ROM[P_{n-1}]`

Quando um salto executa, o IR já capturou a instrução seguinte em sequência. Sem
correção, ela executaria antes de se chegar ao destino.

**A correção:** `IR_Reset = Reset | Jump_EN`.

Funciona porque o `Registo16bits_reset` tem reset síncrono que carrega zero, e
`0x0000` é `NOP`. Foi por isso que o `NOP` ficou no opcode `0000` com `funct` 0.

O `program_counter` mantém a ligação direta ao `Reset` e não passa por esta porta
— é ele que tem de receber o endereço de destino nesse flanco.

Nota: o PC continua a passar pelo endereço do slot, é só o IR que fica a zeros.

---

## 14. O `BLT`, tentado e abandonado

O `F7` ficou livre com a intenção de recuperar o `BLT`, perdido para o `STORE`.
Não foi possível, e vale a pena registar porquê.

**O problema de codificação.** Instruções tipo F não podem ter endereços, logo o
destino teria de vir de um registo. Mas os campos disponíveis são `RA1`, `RA2` e
`WA`, e a comparação já consome dois deles. O `RegA_Out` está ocupado pela
comparação e é ele que alimenta o mux do `Jump_Addr`.

**O problema de fundo.** Ao ligar o `S7` aos dois bits do seletor do mux do
`Jump_Addr`, fechou-se um laço combinatório:

```
SF → (S7 & SF) → Jump_EN → IR_Reset → limpa o IR → muda o opcode → muda o S7
```

Tudo combinatório, tudo dentro do mesmo ciclo. O Digital acusou "oscilação
aparente" e recusou-se a simular.

A condição do salto depende do IR, e o IR depende da condição do salto através do
flush. É estrutural, não é um erro de ligação.

Resolver exigiria separar os dois caminhos — por exemplo, não limpar o IR nos
saltos condicionais, ou registar a condição antes de a usar. Fica em aberto.

O `F7` continua livre e a porta AND que produzia o `S7` ficou no circuito sem
consumidores.

---

## 15. Programas de validação

### Fetch
ROM `0x1000`, `0x2000`, `0x3000`, `0x4000`. O splitter `12-15` mostra 1, 2, 3, 4.

### Descodificador e `ALU_Op`
`0x6000` (`SHR`). `D6` acesa, `ALU_Op` = 3.

### Escrita e leitura no banco
`0xBBC0`, `0x1000` → `Out` = 94 no `ADD`.

### Ciclo com decremento
`0xBBC0`, `0xB050`, `0x2004`, `0xC020` → `Out` desce 46, 45, 44...

### RAM
`0xB1C0`, `0xB050`, `0xF001`, `0xA021`, `0x103A` → `Out` = 14.

### Pilha
`0xB1C0`, `0x0040`, `0x0090`, `0x1011` → `SP` faz F → E → F, `Out` = 14.

### Chamada de função
`0xB140`, `0x00C0`, `0xB1C1`, `0xC030`, `0x0000`, `0x0100`
→ `PC_Out`: `0, 1, 2, 5, 6, 2, 3, 4, 3, 4...`

### `MFHI`
`0xB1C0`, `0xB150`, `0x4004`, `0x0160`, `0x103A`, `0xC040`
→ `Out`: 1 (quociente), 2 (resto), 4 (resto a dobrar).

### `HLT`
`0xB1C0`, `0x0180`, `0xB150` → o `PC_Out` para no 2 e fica parado. O reset faz
arrancar de novo e parar no mesmo sítio.

**Nota sobre a leitura dos testes:** o `Out` é a saída da ALU, que é combinatória
e nunca pára. Em ciclos de `LOAD`, `STORE`, `JMP`, `PUSH` ou `NOP` mostra somas de
valores arbitrários. Um `LOAD`, um `POP` ou um `MFHI` nunca se verificam pelo
`Out` diretamente — é preciso uma instrução seguinte que leia o registo de
destino.

---

## 16. Como codificar à mão

### Tipo R — `SUB R0, R0, R1`

```
opcode  SUB  = 0010
WA      R0   =   00   (bits 5-4)
RA2     R1   =   01   (bits 3-2)
RA1     R0   =   00   (bits 1-0)

0010 0000 0000 0100  =  0x2004
```

O `datapath` calcula `R[RA1] − R[RA2]`, portanto `RA1` é o minuendo.

### Tipo F — `MFHI R2`

```
opcode        = 0000
funct  MFHI   = 101    (bits 8-6)
WA     R2     =  10    (bits 5-4)

0000 0001 0110 0000  =  0x0160
```

O erro mais fácil é trocar o `WA` com o `RA2`. Produz uma instrução válida que
escreve no registo errado, e nos testes com `LOAD` isso destrói o registo que
guarda o endereço. É a principal razão para usar o assemblador.

---

## 17. Exceções ao "de raiz"

| Exceção | Onde | Justificação |
|---|---|---|
| Mux 16:1 nativo | `ALU.dig` | escala |
| `Add` nativo | `program_counter.dig` | escala |
| `ROM` nativa | topo | memória de instruções real |
| `Counter` nativo | gerador de reset | o power-on reset é analógico nos chips reais; não há equivalente digital construível |

---

## 18. Limitações conhecidas

- **Sem `BLT`** — ver secção 14.
- **Sem `CLR`.** Redundante: `XOR rd, rd, rd` faz o mesmo.
- **Sem offset no endereçamento.** `LOAD rd, (ra)` usa o registo tal e qual.
  `LOAD rd, off(ra)` precisaria de um somador dedicado, porque o da ALU está
  ocupado com a operação da instrução.
- **`CALL` indireto apenas.** Obriga a um `LDI` antes de cada chamada.
- **RAM de 16 palavras.** Os 12 bits de cima do endereço são ignorados. A pilha
  ocupa o topo e não há proteção contra colisão com os dados.
- **Banco de registos sem reset.** Arranca com valores sem significado. Cada
  programa tem de escrever num registo antes de o ler, como nos processadores
  reais — o ARM, o RISC-V e o x86 também não limpam os registos gerais.
- **Imediato de 6 bits.** Constantes de 0 a 63. Para mais, `LDI` + `SHL` + `OR`.
- **Endereço de salto de 8 bits.** Programas até 256 palavras.
- **Sem I/O.** A máquina calcula mas não comunica com o exterior. É o que falta
  para deixar de ser um exercício fechado.
- **Flags por usar:** `Cout`, `Flag_RZ`, `Flag_DZ`, `Flag_N`, `Flag_Z`, `OF`, `SF`.
- **Sem interrupções.** Do `HLT` só se sai por reset.

### Espaço que resta

Um slot de `funct` livre, o `F7`. E os bits 11-9 do tipo F estão reservados, o
que dá margem para alargar o campo `funct` a 6 bits e ter 64 sub-instruções.

---

## 19. Ponto de situação

Data desta revisão: 13 de setembro de 2026.

### O que está feito

A cadeia completa, do transístor ao assemblador, sem caixas pretas exceto as
quatro exceções da secção 17.

| Camada | Estado |
|---|---|
| Transístores e portas lógicas | completo |
| Multiplexers, descodificadores, barrel shifters | completo |
| Somador/subtrator 16 bits com flags | completo |
| MDU: multiplicador 32 bits, divisor com resto | completo |
| ALU 16 bits, 8 operações | completo |
| Cadeia sequencial até ao banco de registos | completo |
| `program_counter`, com `EN` exposto | completo |
| `datapath`, com `RegA_Out` e `RegB_Out` | completo |
| RAM 16 × 16 bits | completo |
| Descodificação em dois níveis | completo |
| Pilha com `SP`, `PUSH`/`POP`/`CALL`/`RET` | completo |
| Registo `HI` e `MFHI` | completo |
| `HLT` com malha de retenção | completo |
| Reset de arranque automático | completo |
| Assemblador com etiquetas | completo |

Como processador está fechado: busca, descodifica, executa aritmética e lógica,
acede a memória, salta condicionalmente, chama funções, arranca sozinho e sabe
terminar.

### A transição de "controlador" para CPU

O ficheiro nasceu como o ecrã onde se montava a unidade de controlo, e o nome
`Unidade_de_controlo.dig` refletia isso: a única coisa que lá havia de novo eram
o descodificador e as portas que substituíam os interruptores manuais.

Isso deixou de ser verdade em três passos.

**A RAM entrou ao lado do `datapath`**, e com ela os multiplexadores de endereço
e de dados. O ficheiro passou a conter a memória de dados.

**A pilha trouxe o `SP`**, com o seu somador e os seus dois muxes. Passou a haver
estado arquitetural a viver neste nível, e não só lógica combinatória.

**O registo `HI` e a malha do `HLT`** acrescentaram mais estado ainda.

Neste momento o ficheiro contém a ROM, o IR, o PC, os dois descodificadores, o
`datapath`, a RAM, o `SP`, o `HI`, o gerador de reset e seis multiplexadores. É o
processador inteiro, e a unidade de controlo é uma parte dele.

Daí a mudança de nome para `CPU.dig`. O nome tem de dizer o que lá está dentro
quando o ficheiro for reaberto daqui a meses, e "controlo" já enganava.

Se um dia fizer sentido separar, a divisão natural seria um `controlo.dig` só com
os descodificadores e as portas de geração de sinais, e um `CPU.dig` que
instanciasse esse controlo junto com o `datapath`, a ROM e a RAM. Não muda nada
funcionalmente; é arrumação.

### O que vem a seguir

Por ordem de valor, e com a nota de que **nenhum destes passos é preciso para o
processador estar completo** — são capacidade e periferia.

**1. I/O.** É o próximo passo e o mais importante. Neste momento a máquina
calcula mas não comunica: para ver um resultado é preciso espreitar fios no
simulador. Precisa de um registo de saída ligado a um mostrador de 7 segmentos ou
hexadecimal, e de um registo de entrada ligado a interruptores. Usaria o `F7`, ou
dois novos slots se o campo `funct` for alargado.

Com I/O, a máquina deixa de ser um exercício fechado e passa a poder fazer coisas
— a calculadora de quatro operações, por exemplo, cujo cálculo já está todo feito
em hardware.

**2. Mais memória.** A RAM de 16 palavras e o imediato de 6 bits apertam
qualquer programa sério. Crescer implica resolver primeiro o endereçamento: com
4 bits de opcode e 6 de campos de registo, não há bits livres para endereços
maiores na palavra de 16.

**3. Offset no endereçamento.** `LOAD rd, off(ra)` precisa de um somador
dedicado ao cálculo de endereço, porque o da ALU está ocupado com a operação da
instrução. É o que aproxima o acesso à memória do que fazem as arquiteturas
reais.

**4. Acesso ao `Out_HI/Rest` na escrita.** O `MFHI` resolveu a leitura. Falta um
`MTHI` para o sentido inverso, se algum dia for útil.

**5. Proteção da pilha.** Ela cresce por cima dos dados sem aviso. Uma flag de
colisão seria realista.

**6. Interrupções.** Do `HLT` só se sai por reset. Uma linha externa que desvie o
PC para um vetor fixo, guardando o contexto, é o que falta para a máquina
responder a eventos. É também o primeiro degrau a sério em direção a software de
sistema.

### O que não é alcançável, e porquê

Correr um sistema operativo está fora de alcance, e é honesto registá-lo.

**A memória.** Um SO mínimo precisa de centenas de kilobytes; a máquina tem 32
bytes de RAM e 512 de ROM. São três a quatro ordens de grandeza.

**O endereçamento.** O campo de endereço tem 8 bits. O limite está na ISA, não na
memória que se consiga construir.

**A arquitetura.** Faltam interrupções, modo privilegiado separado do modo
utilizador, e proteção de memória. Sem isso não há multitarefa nem isolamento.

**A simulação.** O Digital simula transístor a transístor. A RAM de 16 palavras
já são 256 flip-flops; uma máquina capaz de correr um SO seria impossível de
simular em tempo útil.

O degrau realista nessa direção é um **monitor**: um programa residente que
aceita comandos, lê e escreve memória, carrega outros programas e os executa. É o
que existia antes dos sistemas operativos, e com I/O e algumas centenas de
palavras é alcançável.

### Onde a máquina se situa

É um microcontrolador rudimentar, da família do que existia nos anos 70. O Intel
4004 tinha 4 bits de dados e 46 instruções; este tem 16 bits, multiplicação e
divisão em hardware, e chamadas de função com pilha.

O que faz na prática: qualquer algoritmo que caiba em 256 instruções e 16
palavras de dados. Contagens, aritmética, ordenar meia dúzia de números, procurar
um valor, sequências, funções reutilizáveis e recursão.

---

## 20. Nomenclatura

Ficheiros que fogem à convenção do repositório e precisam de correção na
passagem lib→repo, incluindo as strings `<elementName>` dos pais:

| Atual | Deveria ser |
|---|---|
| `Unidade_de_controlo.dig` | `CPU.dig` |
| `RAM 16x16 bits.dig` | `RAM.dig` — tem espaços |
| `Register_final.dig` | `register_file.dig` |
| `Registo16bits_reset.dig` | `register_16bits_reset.dig` |
| `Registro_16bits.dig` | `register_16bits.dig` |
