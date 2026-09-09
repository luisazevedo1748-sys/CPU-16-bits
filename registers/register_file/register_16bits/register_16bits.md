# register_16bits — 16-bit register with load enable

The datapath's basic storage word: sixteen bits latched together on one clock
edge, with a load enable so it only changes when told to. Built by stacking four
`register_4bits` slices — the same 4 → 16 width extension as everything else in
this project. This is the cell that will hold `PC`, the instruction, and each
entry of the register file.

> Byte-for-byte copy of the Digital library file `Registro_16bits.dig`. Renamed
> to `register_16bits`; the only edit is the `<elementName>` reference to its
> child, now `register_4bits.dig`. Nothing references this file yet — it is a
> top-level block for now.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `D` | 16 | data in |
| `Clk` | 1 | clock, common to all 16 bits |
| `EN` | 1 | `1` = load `D` on the next edge; `0` = hold |
| `Q` | 16 | stored word |

## How it works

- `D` is split into four nibbles (`Splitter` `16 → 4,4,4,4`); nibble *i* goes to
  the *i*-th `register_4bits`; the four `Q` nibbles are re-joined
  (`Splitter` `4,4,4,4 → 16`).
- `Clk` and `EN` are broadcast to all four slices, so the whole 16-bit word
  loads or holds as one.
- Each slice already carries its own `D`-vs-`Q` load-enable mux, so this level
  is purely wiring — no extra logic.

## Structure

```
register_16bits
└─ 4 × register_4bits
   ├─ 4 × flip_flop_d  →  d_latch  →  latch_sr
   └─ Multiplexer (4-bit) + Splitters
```

Plus two `Splitter` primitives (`16 ↔ 4,4,4,4`).

## Notes

- The nibble grouping is only for wiring convenience; sixteen individual
  `flip_flop_d` with a 16-bit enable mux would be logically identical.
- Pin order follows the vertical position of the `In` / `Out` symbols
  (`D, Clk, EN` → `Q`). Any future parent (register file, PC) must be wired to
  match, or fixed with *Edit → Order Inputs/Outputs*.
- Opening this block from the repo: add
  `registers/register_file/register_16bits/register_4bits/` and the folders below
  it as custom component search paths, because Digital only searches
  sub-directories of the file it opens.

## Status

Simulated in Digital and works: `EN = 1` loads a 16-bit value on the edge;
`EN = 0` holds it across ticks.
