# 16-bit division cell (one divider row)

One row of the array divider: it subtracts the divisor from the shifted partial
remainder, decides on its own whether to restore, and emits the new remainder
plus this row's quotient bit.

## Interface

- **Rin** — 16-bit partial remainder coming in from the row above.
- **Din** — 16-bit divisor (the same on every row).
- **Rout** — 16-bit partial remainder passed to the row below.
- **Cout** — this row's borrow-out, i.e. the quotient bit (`1` = the divisor
  fitted, no restore).

`Cin` and `Restore` are not exposed. The first cell's carry-in is tied to `VDD`
to complete the two's-complement `~Din + 1`, and `Restore` is generated inside
the block by inverting the final `Cout`.

## How it works

`Rin` and `Din` are split `16 → 8, 8` and run through two `div_cell_8_bits`
slices on one borrow chain. The final carry-out is inverted to form `Restore`,
fed back to both slices so the whole row either keeps the subtracted value or
restores `Rin`. The un-inverted carry-out leaves as `Cout`.

## Structure

```
div_cell_16_bits
├─ 2 × div_cell_8_bits     ripple borrow chain
├─ VDD                     first Cin = 1  (two's-complement subtract)
└─ Not                     Restore = ~Cout
```

## Notes

Each cell down the chain orders its pins by symbol position, and every parent is
wired to match (see `div_cell_1_bit.md`); the full array simulates correctly
(`100 ÷ 7` → quotient 14, remainder 2). No screenshot yet
(`div_cell_16_bits.png` still to be exported from Digital).
