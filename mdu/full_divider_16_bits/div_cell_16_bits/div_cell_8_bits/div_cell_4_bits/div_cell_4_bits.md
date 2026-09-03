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

## Pin order

`div_cell_1_bit` exposes its inputs, by symbol position, as
`Restore, Rin, Din, Cin`; this circuit's own input order is
`Cin, Rin, Din, Restore`. The wiring between the two is drawn to match. See
`div_cell_1_bit.md`. Verified in the full array (`100 ÷ 7` → 14 r 2).
