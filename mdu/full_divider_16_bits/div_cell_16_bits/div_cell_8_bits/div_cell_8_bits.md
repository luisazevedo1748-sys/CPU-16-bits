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

## Known issue

`div_cell_4_bits`'s pins are ordered by position as `Cin, Rin, Din, Restore`,
but this circuit wires the slices as `Rin, Din, Cin, Restore`. The 1-bit `Cin`
line ends up on the 4-bit `Din` port and the 4-bit `Rin` bus on the 1-bit `Cin`
port, so three bits of that port are left undriven — this is the "wire in
undefined state" Digital reports here. See `div_cell_1_bit.md`.
