# 4-bit division cell

One 4-bit slice of a divider row: four `div_cell_1_bit` cells on a shared borrow
chain, all driven by the same `Restore`.

## Interface

- **Rin** — 4 bits of the partial remainder.
- **Din** — 4 bits of the divisor.
- **Cin** — borrow in from the slice below.
- **Restore** — row-wide restore control, broadcast to all four cells.
- **Rout** — 4 bits of the updated remainder.
- **Cout** — borrow out of the top cell.

## How it works

`Rin` and `Din` are split to individual bits and paired into the four cells,
least-significant first. Each cell's `Cout` feeds the next cell's `Cin`, so the
subtraction ripples across the slice. `Rout` is reassembled from the four cell
outputs.

## Structure

```
div_cell_4_bits
└─ 4 × div_cell_1_bit     ripple borrow chain, shared Restore
```

## Known issue

`div_cell_1_bit`'s pins are ordered by position as `Restore, Rin, Din, Cin`,
but this circuit wires the cells as `Rin, Din, Cin, Restore`, so every cell
receives the wrong signal on every pin. See `div_cell_1_bit.md`.
