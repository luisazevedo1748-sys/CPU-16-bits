# MDU — multiply / divide unit

Top-level block of the `mdu/` module. It wraps the 16×16 array multiplier and
the 16-bit restoring array divider behind one operation selector, so the rest of
the datapath sees a single unit with one pair of operands and one pair of
result words plus status flags.

Purely combinational: it inherits the multiplier and divider as-is, adds only
multiplexers, and settles once the inputs are stable.

> File name kept as `MDU.dig` (uppercase, unlike the rest of the repo) because
> it is a byte-for-byte copy of the Digital library file — its `<elementName>`
> references were left untouched. See **Cross-references** below.

## Interface

- **A** — 16-bit operand (multiplicand / dividend).
- **B** — 16-bit operand (multiplier / divisor).
- **MDU_op** — 1-bit operation select: chooses whether the multiplier or the
  divider drives the outputs. It also gates the operands, so the unit that is
  not selected sees zeros on its inputs instead of toggling. (The exact 0/1
  polarity is fixed by the selector wiring, not by this block's logic.)
- **LO** — low result word: product bits 0–15 for a multiply, **quotient** for a
  divide.
- **HI** — high result word: product bits 16–31 for a multiply, **remainder**
  (`A mod B`) for a divide.
- **Flag_Z** — result is zero.
- **Flag_N** — result is negative (top result bit, i.e. a signed reading of the
  32-bit product).
- **Flag_RZ** — division remainder is zero (the division was exact). Meaningful
  only for a divide.
- **Flag_DZ** — division by zero (`B = 0`). Meaningful only for a divide. The
  divider array is not special-cased, so on `B = 0` its quotient comes out all
  ones; this flag is what reports the condition.

`HI:LO` is the full 32-bit product for a multiply. Operands are unsigned; a
signed interpretation is left to software (the sign flag is provided for
convenience).

## How it works

1. **Operand gating.** `A` and `B` each pass through a `mux_2_1_16bits` whose
   other input is `Ground`. `MDU_op` decides which unit receives the real
   operands; the idle unit receives 0/0.
2. **Both units compute.** the multiplier produces `HI:LO` and its own
   `ZF`/`SF`; the divider produces `Quotient`/`Rest`.
3. **Result select.** Two more `mux_2_1_16bits` pick `LO` and `HI` between the
   multiplier's product halves and the divider's quotient / remainder,
   controlled by `MDU_op`.
4. **Flag select.** Four `mux_2_1` blocks pick `Flag_Z / Flag_N / Flag_RZ /
   Flag_DZ` between the multiplier-side and divider-side sources (some tied to
   `Ground` where a flag does not apply to that operation).

> `MDU.dig` synthesises the divide-side flags itself, with several inputs tied
> to `Ground`. The standalone `full_divider_16_bits` also exposes `FDZ / FRZ /
> FN` directly, so those can be wired into the flag muxes instead of the
> `Ground` stubs if the flag paths are ever reworked.

## Structure

```
MDU
├─ full_multiplier_16_bits/   16×16 array multiplier → HI:LO + ZF/SF
├─ full_divider_16_bits/      16-bit restoring array divider → quotient + remainder
├─ mux_2_1_16bits             operand gating (×4) and LO/HI result select (×2)
│  └─ mux_2_1_4b
│     └─ mux_2_1
└─ mux_2_1                    flag select (×4)
```

## Cross-references

`MDU.dig` refers to its sub-circuits by their Digital-library names. In the
library folder they sit side by side and all resolve; from this repo's folder
tree, add the folders below as custom component search paths (Edit → Settings).

| `MDU.dig` uses | This repo's copy |
|---|---|
| `full_multiplier_16_bits.dig` | `mdu/full_multiplier_16_bits/full_multiplier_16_bits.dig` |
| `full_division.dig` | `mdu/full_divider_16_bits/full_divider_16_bits.dig` |
| `mux_2_1_16bits.dig` | `multiplexer/mux_2_1_16bits/mux_2_1_16bits.dig` |
| `mux_2_1.dig` | `multiplexer/mux_16_1/mux_8_1/mux_4_1/mux_2_1/mux_2_1.dig` |

## Status

The multiply path matches the standalone `full_multiplier_16_bits`; the divider
simulates correctly on its own (`100 ÷ 7` → quotient 14, remainder 2).

To verify through `MDU.dig`:

- multiply: `A·B` low/high against `full_multiplier_16_bits`, `Flag_Z` on
  `A·B = 0`, `Flag_N` on a product with bit 31 set.
- divide: `100 ÷ 7` → `LO = 14`, `HI = 2`, `Flag_RZ = 0`; `21 ÷ 7` →
  `Flag_RZ = 1`; `x ÷ 0` → `Flag_DZ = 1`.
