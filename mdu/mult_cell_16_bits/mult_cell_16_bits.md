# 16-bit multiplier cell

Width extension of the array-multiplier row cell to a full 16-bit data word:
two `mult_cell_8_bits` blocks chained by ripple carry.

    SumOut , Cout  =  A · B  +  SumIn  +  Cin

## Interface

- **A** — 16-bit slice of the multiplicand.
- **B** — 1 bit of the multiplier; it gates every bit of A to form the partial
  product.
- **SumIn** — 16-bit running sum from the row above.
- **Cin** — carry into the low 8-bit half.
- **SumOut** — 16-bit running sum to the row below.
- **Cout** — carry out of the high 8-bit half.

## Structure

Low `mult_cell_8_bits` = bits 0–7, high = bits 8–15, carry chained low → high.
The 16-bit A and SumIn buses are split `8,8` and SumOut is rejoined.

This block is the **row primitive** of the array multiplier. A complete 16×16
multiplier stacks 16 of these cells: each row is fed the next multiplier bit on
`B` and the previous row's `SumOut` on `SumIn`, with the partial products
shifted one position per row.

## Status

Row-cell width extension 4 → 8 → 16 bits: **done**.
Full 16-row array (`ROADMAP` §1, "MDU — 16-bit multiplier"): still to assemble.

## Note on dependencies

Sub-circuits resolve through the nested folders
(`mult_cell_8_bits/` → `mult_cell_4_bits/` → `mult_cell_1_bit/`). The 1-bit cell
still pulls `full_adder.dig` from the `adder_subtractor/` tree; add that folder
as a *custom component search path* in Digital
(Edit → Settings) to simulate the MDU blocks.
