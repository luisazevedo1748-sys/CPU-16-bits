# ALU — 16-bit arithmetic / logic unit

Top-level block of the `alu/` module. It gathers every data-path operation the
CPU can do on 16-bit words — add / subtract, multiply / divide, shift, and
bitwise logic — behind a single `ALU_Op` selector, and exposes one main result
plus the status flags the control unit needs for conditional branches.

Purely combinational: it inherits the adder/subtractor, the MDU and the two
shifters as-is, adds one output multiplexer and the logic gates, and settles
once the inputs are stable.

> `ALU.dig` is a byte-for-byte copy of the Digital library file; its
> `<elementName>` references are left untouched, so the repo file names have to
> match what it expects. See **Cross-references** below.

## Interface

### Inputs

| Pin | Width | Meaning |
|---|---|---|
| `A` | 16 | First operand. For a shift, the value being shifted. |
| `B` | 16 | Second operand. For a shift, `B[3:0]` is the shift amount (`Shamt`); the upper bits are ignored. |
| `ALU_Op` | 3 | Operation selector for the `Out` multiplexer (0–7, see table). |
| `Sub` | 1 | Adder mode, only meaningful for `ALU_Op = 0`: `0` = `A + B`, `1` = `A − B`. |
| `MDU_op` | 1 | MDU mode, only meaningful for `ALU_Op = 1`: selects multiply vs. divide inside `MDU.dig` (the exact 0/1 polarity is fixed by the MDU wiring). |

> The operation guide written for this block calls `ALU_Op` a 4-bit field. The
> circuit pin is **3 bits** — enough for the eight operations below; opcode 7 is
> currently unused.

### Outputs

| Pin | Width | Meaning |
|---|---|---|
| `Out` | 16 | Main result, chosen by `ALU_Op`. |
| `Out_HI` | 16 | Secondary result, wired straight from the MDU: product high word when `MDU_op` = multiply, **remainder** when `MDU_op` = divide. It follows `A` / `B` / `MDU_op` regardless of `ALU_Op`, so it is only meaningful to read for `ALU_Op = 1`. |

### Operation table

| `ALU_Op` | `Sub` | `MDU_op` | Operation | `Out` | `Out_HI` |
|---:|:---:|:---:|---|---|---|
| 0 | 0 | X | Add | `A + B` | — |
| 0 | 1 | X | Subtract | `A − B` | — |
| 1 | X | mul | Multiply | low 16 bits of `A × B` | high 16 bits of `A × B` |
| 1 | X | div | Divide | quotient of `A ÷ B` | remainder of `A ÷ B` |
| 2 | X | X | Shift left | `A << B[3:0]` | — |
| 3 | X | X | Shift right | `A >> B[3:0]` | — |
| 4 | X | X | AND | `A & B` | — |
| 5 | X | X | OR | `A \| B` | — |
| 6 | X | X | XOR | `A ^ B` | — |

`X` = don't-care.

### Flags

Arithmetic flags — **valid only for `ALU_Op = 0`** (the add/subtract path):

| Flag | Set when |
|---|---|
| `ZF` | result is exactly zero (e.g. `A − B` with `A = B`) |
| `SF` | result is negative (top bit of the result) |
| `Cout` | carry out of the most significant bit |
| `OF` | signed overflow (pos + pos → neg, or neg + neg → pos) |

MDU flags — **valid only for `ALU_Op = 1`** (the multiply/divide path), passed
straight through from `MDU.dig`:

| Flag | Set when |
|---|---|
| `Flag_Z` | product, or quotient, is zero |
| `Flag_RZ` | division remainder is zero — `A` is a multiple of `B` |
| `Flag_N` | product / quotient is negative (signed reading of the top bit) |
| `Flag_DZ` | divide by zero (`B = 0`) — critical error flag |

The flags are not gated by `ALU_Op`; the control unit is expected to read the
arithmetic set or the MDU set only for the matching opcode.

## How it works

1. **Every path computes in parallel.** `add_sub_16_bits` gets `A`, `B`, `Sub`;
   `shift_left_16bits` and `shift_right_16bits` get `A` as data and `B[3:0]` as
   `Shamt`; `MDU.dig` gets `A`, `B`, `MDU_op`; the `And` / `Or` / `XOr` gates
   get `A` and `B` bitwise.
2. **Output select.** One 16-bit `Multiplexer` (Digital primitive, 3 select
   bits) routes one of those results to `Out` according to `ALU_Op`.
3. **Secondary word.** `Out_HI` is taken from the MDU's high / remainder word.
4. **Flags.** The adder's `ZF / SF / Cout / OF` and the MDU's
   `Flag_Z / Flag_RZ / Flag_N / Flag_DZ` are brought straight out.

## Structure

```
ALU
├─ add_sub_16_bits/        A ± B, two's complement, ZF / SF / Cout / OF
├─ shift_left_16bits/      A << Shamt   (barrel, 4 x mux_2_1_16bits)
├─ shift_right_16bits/     A >> Shamt   (barrel, 4 x mux_2_1_16bits)
├─ MDU.dig                 A * B / A / B behind MDU_op → LO / HI + flags
├─ And / Or / XOr          bitwise logic (Digital primitives)
└─ Multiplexer             16-bit, 3-select output selector
```

## Cross-references

`ALU.dig` refers to its sub-circuits by their library names. In this repo they
live in other folders, so add each of these to Digital's custom component
search path when opening the block:

| `ALU.dig` uses | This repo's copy |
|---|---|
| `add_sub_16_bits.dig` | `adder_subtractor/add_sub_16_bits.dig` |
| `shift_left_16bits.dig` | `alu/shift_left_16bits/shift_left_16bits.dig` |
| `shift_right_16bits.dig` | `alu/shift_right_16bits/shift_right_16bits.dig` |
| `MDU.dig` | `mdu/MDU.dig` (which itself pulls the `mdu/` sub-circuits — see `mdu/MDU.md`) |

## Status

Drafted and saved from Digital, and exercised by hand: `A = 100`, `B = 7` gives
`Out = 12800` for `ALU_Op = 2` (`100 << 7`) with `Out_HI = 2` from the MDU
remainder path, and the divider on its own returns `100 ÷ 7` → quotient 14,
remainder 2. The add / subtract, shift and logic paths are straightforward
compositions of blocks that already work.

To verify the rest:

- `ALU_Op = 0`, `Sub = 0`: `A + B`, check `ZF` on `A + B = 0`, `Cout` / `OF` on
  edge cases.
- `ALU_Op = 0`, `Sub = 1`: `A − B`, `ZF` when `A = B`, `SF` when `A < B`.
- `ALU_Op = 2 / 3`: `A` shifted by `B[3:0]`, including `Shamt = 0` and
  `Shamt = 15`.
- `ALU_Op = 4 / 5 / 6`: bitwise `A & B`, `A | B`, `A ^ B`.
- `ALU_Op = 1`: multiply against `full_multiplier_16_bits`; divide
  (`100 ÷ 7` → `Out = 14`, `Out_HI = 2` — remainder path already confirmed;
  `21 ÷ 7` → `Flag_RZ = 1`; `x ÷ 0` → `Flag_DZ = 1`).
