# flip_flop_d — edge-triggered D flip-flop

A clocked 1-bit store that samples `D` only on a **clock edge**, not for the
whole time the clock is high. This is the cell every register in the CPU is made
of: on each tick it latches one new bit and holds it steady for the rest of the
cycle, which is what makes a synchronous datapath work.

> Byte-for-byte copy of the Digital library file `flip_flop_D.dig`. Renamed to
> `flip_flop_d`; the only edit is the `<elementName>` reference to its child,
> now `d_latch.dig`. `register_4bits.dig` references this file as
> `flip_flop_d.dig`.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `D` | 1 | data input, sampled at the clock edge |
| `Clk` | 1 | clock |
| `Q` | 1 | value captured at the last edge |
| `¬Q` | 1 | its complement |

## How it works

Two `d_latch` stages in series (master–slave), with the clock **inverted**
between them so the two latches are never transparent at the same time:

- One latch is transparent while `Clk = 0` and follows `D`; the other is
  transparent while `Clk = 1`.
- On the clock transition the first latch freezes the value it had and the
  second one opens and passes it to `Q`.
- The result is that `Q` changes **once per clock period**, at the edge, and is
  immune to any `D` activity between edges.

Because only one latch is ever open, there is never a transparent path from `D`
to `Q`; that is the whole point of going master–slave.

## Structure

```
flip_flop_d
├─ 2 × d_latch
│  └─ latch_sr
└─ Not            (clock inverter between the two latches)
```

## Notes

- Pin order follows the vertical position of the `In` / `Out` symbols
  (`D, Clk` → `Q, ¬Q`); `register_4bits` is wired to match.
- Which physical edge (rising or falling) captures the data is set by which
  latch gets the inverted clock — confirm it in simulation and note it here.
- No asynchronous set/reset and no explicit enable: holding a value across a
  tick is done one level up, by `register_4bits` feeding `Q` back through a mux.

## Status

Saved from Digital. Verify: `Q` takes the value of `D` only at the clock edge
and ignores changes on `D` between edges; note whether it triggers on the rising
or the falling edge.
