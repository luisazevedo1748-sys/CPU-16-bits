# 1-bit division cell

One column of a restoring array divider. It computes a single bit of
`Rin − Din` on a borrow chain and then either keeps that result or throws it
away and restores the original `Rin`, depending on the row-wide `Restore`
signal.

## Interface

- **Rin** — one bit of the current partial remainder.
- **Din** — the aligned divisor bit for this column.
- **Cin** — borrow / carry in from the next less-significant cell.
- **Restore** — row-wide control: `1` when the row's subtraction went negative,
  so the old remainder must be kept.
- **Rout** — the remainder bit this cell contributes: the subtracted bit when
  `Restore = 0`, the untouched `Rin` when `Restore = 1`.
- **Cout** — borrow / carry out to the next more-significant cell.

## How it works

1. **Subtract.** `Din` is inverted and fed with `Rin` and `Cin` into a
   `full_adder`, so the cell evaluates `Rin + ~Din + Cin`. With the row's first
   `Cin` tied to `1` the whole row computes two's-complement `Rin − Din`.
2. **Restore mux.** A `mux_2_1` selects between the adder `Sum` and the
   unmodified `Rin`; `Restore` is the select line.
3. **Borrow chain.** `Cout` passes the carry along the row.

## Structure

```
div_cell_1_bit
├─ full_adder     Rin + ~Din + Cin
└─ mux_2_1        Restore ? Rin : Sum
```

## Known issue

The pins do not line up with the wiring. Digital orders a block's pins by the
vertical position of its `In` / `Out` symbols, not by creation order:

- inside this cell the `mux_2_1` is wired as if its pins were `D0, D1, S`, but
  its `S` symbol sits well above `D0` / `D1`, so the real order is `S, D0, D1`.
  As drawn, the mux select is the adder `Sum` instead of `Restore`.
- this cell's own `Restore` symbol is at the top, so its pin order is
  `Restore, Rin, Din, Cin` rather than `Rin, Din, Cin, Restore` — which is how
  `div_cell_4_bits` wires it.

Fix bottom-up with *Edit → Order Inputs/Outputs* (or by realigning the `In`
symbols): `mux_2_1` → `div_cell_1_bit` → `div_cell_4_bits` → `div_cell_8_bits`
→ `div_cell_16_bits`.
