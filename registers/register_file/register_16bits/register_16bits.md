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

## Design decision — no reset line

`register_16bits`, and everything built from it (`register_file`, and later any
general-purpose register), has **no reset / clear input**. This is deliberate
and matches how register files are actually built in real RISC-V and ARM cores:

- A global reset routed to every bit of every register is expensive silicon —
  an extra gate on each flip-flop plus a net wide enough to drive all of them
  across the whole file. It makes the block larger, slower and hotter for
  something the hardware does not need.
- Real general-purpose registers have no defined power-on value. They come up
  holding whatever the transistors settled into ("garbage"); the firmware or
  bootloader zeroes the ones it cares about with ordinary writes in its first
  instructions.

So the registers here start undefined and are cleared **in software**: drive
`Data_In = 0`, pick the register with `WA`, pulse `WE = 1`.

### How a synchronous reset would be built, if wanted

One **AND gate per bit** in front of each flip-flop's `D`: one input is the
normal data, the other is the reset signal **inverted**. Reset low → data
passes unchanged; reset high → the AND forces `D = 0` and the next clock edge
latches `0` into every bit. For 16 bits that is 16 AND gates plus a reset net to
all of them; for the file, that again per register. The `Program Counter` is the
one place this matters (it must power up at `0`), and there the project uses
Digital's native register block instead of hand-wiring it — see ROADMAP §2.

## Status

Simulated in Digital and works: `EN = 1` loads a 16-bit value on the edge;
`EN = 0` holds it across ticks.
