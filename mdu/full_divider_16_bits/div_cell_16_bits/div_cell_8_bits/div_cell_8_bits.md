# 8-bit division cell

Two `div_cell_4_bits` slices stacked into an 8-bit divider row.

## Interface

- **Rin** — 8 bits of the partial remainder.
- **Din** — 8 bits of the divisor.
- **Cin** — borrow in.
- **Restore** — row-wide restore control.
- **Rout** — 8 bits of the updated remainder.
- **Cout** — borrow out.

## How it works

`Rin` and `Din` are split `8 → 4, 4`. The low slice takes `Cin`; its `Cout`
feeds the high slice's `Cin`; the high slice's `Cout` leaves the block. `Rout`
is the two 4-bit results rejoined.

## Structure

```
div_cell_8_bits
└─ 2 × div_cell_4_bits     ripple borrow chain, shared Restore
```

## Pin order

`div_cell_4_bits` exposes its inputs, by symbol position, as
`Cin, Rin, Din, Restore`; this circuit's own input order is
`Rin, Din, Cin, Restore`. The wiring between the two is drawn to match those
positions (the 1-bit `Cin` and the 4-bit `Rin` / `Din` buses each land on the
right port). See `div_cell_1_bit.md`. Verified in the full array
(`100 ÷ 7` → 14 r 2).
