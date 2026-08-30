# 16×16-bit multiplier (full array)

A purely combinational 16×16 array multiplier. It does in silicon exactly what
long multiplication does on paper: build one shifted partial product per bit of
the multiplier and add them all up. No clock, no state — the 32-bit product
settles as soon as the inputs are stable.

## Interface

- **A** — 16-bit multiplicand.
- **B** — 16-bit multiplier.
- **LO** — low 16 bits of the product (bits 0–15).
- **HI** — high 16 bits of the product (bits 16–31).

`HI:LO` is the full 32-bit result, so any product of two unsigned 16-bit values
(up to 65535 × 65535) fits without loss. Operands are treated as unsigned; the
signed interpretation is left to software.

## How it works

The array is **16 rows**, each one a `mult_cell_16_bits` block.

1. **Conditional partial product.** A is fed to every row. Row *i* looks at a
   single bit `B[i]`: inside the cell that bit gates A (AND), so the row emits
   either A (when `B[i] = 1`) or all zeros (when `B[i] = 0`).
2. **Vertical accumulation.** Each row adds its partial product to the running
   sum inherited from the row above through `SumIn` (`SumOut,Cout = A·B + SumIn
   + Cin`). Row 0's `SumIn` and every `Cin` are tied to ground, so the sum
   starts at zero.
3. **One-place shift.** To reproduce the leftward shift of each line in paper
   multiplication, the bus is re-cut at the output of every row: bit 0 of that
   row's sum leaves the array as one settled result bit, the remaining 15 bits
   slide down one position, and the row's `Cout` is packed into the top bit
   (splitter pattern `16 → 1,15` then `15,1 → 16`).
4. **LO / HI split.** The 16 bits that dropped out one per row, reassembled in
   order, form **LO**. The full 16-bit bus that comes out of the last row (row
   15) is **HI**. Concatenating them gives the 32-bit product.

## Structure

```
full_multiplier_16_bits
└─ 16 × mult_cell_16_bits          one array row each
   └─ 2 × mult_cell_8_bits         ripple-carry width extension
      └─ 2 × mult_cell_4_bits
         └─ 4 × mult_cell_1_bit
```

This is a ripple array: worst-case delay grows with the carry and
accumulation chain across all 16 rows. It is the simplest correct structure;
faster schemes (carry-save trees, Booth encoding) are a later optimisation.

## Note on dependencies

Sub-circuits resolve through the nested folders down to `mult_cell_1_bit`,
which still pulls `full_adder.dig` from the `adder_subtractor/` tree. Add that
folder as a *custom component search path* in Digital (Edit → Settings) before
simulating.
