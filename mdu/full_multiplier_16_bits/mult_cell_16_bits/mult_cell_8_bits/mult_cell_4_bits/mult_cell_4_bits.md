# 4-bit multiplier cell

Four `mult_cell_1_bit` blocks in a carry chain. This is the first real width of
the array-multiplier row cell: it processes a 4-bit slice of the multiplicand
against a single multiplier bit.

The cell computes one row of an array multiplier:

    SumOut , Cout  =  A · B  +  SumIn  +  Cin

## Interface

- **A** — 4-bit slice of the multiplicand.
- **B** — 1 bit of the multiplier; inside each 1-bit cell it gates the matching
  bit of A (AND) to form the partial product.
- **SumIn** — 4-bit running sum coming from the row above.
- **Cin** — carry into bit 0.
- **SumOut** — 4-bit running sum passed to the row below.
- **Cout** — carry out of bit 3.

## Structure

A splitter opens the 4-bit `A` bus into single bits (`4 → 1,1,1,1`) and a second
one does the same to `SumIn`; `B` is broadcast to all four cells. Cell *i* gets
`A[i]`, `B`, `SumIn[i]` and the carry from cell *i−1*, and produces `SumOut[i]`
plus the carry into cell *i+1*. The carry ripples `Cin → 0 → 1 → 2 → 3 → Cout`.
A last splitter recombines the four `SumOut` bits into the 4-bit bus
(`1,1,1,1 → 4`).

Wider cells are just this pattern extended: `mult_cell_8_bits` chains two of
these, `mult_cell_16_bits` chains two 8-bit cells, and the full multiplier
stacks sixteen 16-bit rows.

## Note on dependencies

Each `mult_cell_1_bit` uses `full_adder.dig` from the `adder_subtractor/` tree.
Digital only searches sub-directories, so add that folder as a *custom component
search path* (Edit → Settings) before simulating — see
`mult_cell_1_bit/mult_cell_1_bit.md`.
