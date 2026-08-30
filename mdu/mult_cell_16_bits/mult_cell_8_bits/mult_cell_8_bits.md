# 8-bit multiplier cell

Width extension of the array-multiplier row cell: two `mult_cell_4_bits` blocks
chained by ripple carry so the row now spans an 8-bit data word.

The cell computes one row of an array multiplier:

    SumOut , Cout  =  A · B  +  SumIn  +  Cin

## Interface

- **A** — 8-bit slice of the multiplicand.
- **B** — 1 bit of the multiplier; it gates every bit of A (AND) to form the
  partial product.
- **SumIn** — 8-bit running sum coming from the row above.
- **Cin** — carry into the low 4-bit half.
- **SumOut** — 8-bit running sum passed to the row below.
- **Cout** — carry out of the high 4-bit half.

## Structure

The low `mult_cell_4_bits` handles bits 0–3, the high one bits 4–7; the carry
of the low cell feeds the `Cin` of the high cell. Splitters cut the 8-bit A and
SumIn buses into `4,4` and rejoin SumOut.

## Note on dependencies

`mult_cell_4_bits.dig` sits in the sub-folder `mult_cell_4_bits/`, so Digital
resolves it automatically. That cell in turn needs `full_adder.dig` from the
`adder_subtractor/` tree — see
`mult_cell_4_bits/mult_cell_1_bit/mult_cell_1_bit.md`.
