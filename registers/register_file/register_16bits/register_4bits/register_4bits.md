# register_4bits — 4-bit register with load enable

Four `flip_flop_d` cells clocked together, plus a load-enable so the register
only takes new data on the ticks you choose. This is the width-extension step
between the single-bit flip-flop and the full 16-bit register — the same trick
used in the adder and multiplier trees (1 → 4 → 16).

> Byte-for-byte copy of the Digital library file `Registo_4bits.dig`. Renamed to
> `register_4bits`; the only edit is the `<elementName>` reference to its child,
> now `flip_flop_d.dig`. `register_16bits.dig` references this file as
> `register_4bits.dig`.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `D` | 4 | data in |
| `Clk` | 1 | clock, common to all four bits |
| `EN` | 1 | `1` = load `D` on the next edge; `0` = keep the current value |
| `Q` | 4 | stored word |

## How it works

- `D` is split into four bits (`Splitter` `4 → 1,1,1,1`); each bit has its own
  `flip_flop_d`; the four `Q` bits are re-joined (`Splitter` `1,1,1,1 → 4`).
- All four flip-flops share `Clk`, so the whole word updates on the same edge.
- **Load enable.** A 4-bit `Multiplexer` sits in front of the flip-flop inputs.
  Its two data ports are the incoming `D` and the register's own `Q` fed back;
  `EN` is the select. `EN = 0` routes `Q` back into the flip-flops (they
  re-latch what they already hold — a hold), `EN = 1` routes `D` in (a load).
  The flip-flops are clocked every cycle; `EN` only decides *what* they latch.

## Structure

```
register_4bits
├─ 4 × flip_flop_d
│  └─ d_latch → latch_sr
├─ Multiplexer   (4-bit, D vs. Q-feedback, selected by EN)
└─ 2 × Splitter  (4 ↔ 1,1,1,1)
```

`Multiplexer` and `Splitter` are Digital primitives.

## Notes

- Feeding `Q` back through a mux is the standard way to build a load-enable out
  of plain edge-triggered flip-flops that have no enable pin of their own.
- Pin order follows the vertical position of the `In` / `Out` symbols
  (`D, Clk, EN` → `Q`); `register_16bits` is wired to match.
- Gating the data path with `EN` (rather than gating the clock) keeps every
  flip-flop on the same clean clock — no clock-enable glitches.

## Status

Simulated in Digital and works: `EN = 1` loads `D` on the edge; `EN = 0` holds
across any number of ticks; all four bits change on the same edge.
