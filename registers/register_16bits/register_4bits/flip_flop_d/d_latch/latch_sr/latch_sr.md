# latch_sr — SR latch (NOR)

The smallest storage element in the build: a bistable cell that **holds one
bit**. Two cross-coupled NOR gates feed each other back, so the pair has two
stable states (`Q = 0` and `Q = 1`) and stays in whichever one it was last put.
Every flip-flop, register and RAM cell above this is an elaboration of the same
cross-coupled loop.

> Byte-for-byte copy of the Digital library file `Latch_SR.dig`. Renamed to
> `latch_sr` for the repo convention; `d_latch.dig` now references it by that
> name.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Reset` | 1 | `1` forces `Q → 0` |
| `Set` | 1 | `1` forces `Q → 1` |
| `Q` | 1 | stored bit |
| `¬Q` | 1 | its complement |

## How it works

Two NOR gates, each with one external input and one input taken from the other
gate's output:

```
Q  = NOR(Reset, ¬Q)
¬Q = NOR(Set,  Q)
```

- `Set = 1, Reset = 0` → `¬Q = 0`, which pulls `Q = 1`. **Set.**
- `Reset = 1, Set = 0` → `Q = 0`, which pulls `¬Q = 1`. **Reset.**
- `Set = Reset = 0` → each NOR just inverts the other's output; the loop keeps
  its previous value. **Hold.**
- `Set = Reset = 1` → both outputs go to `0` (not complementary); the state
  when both are released together is undefined. **Forbidden combination.**

It is level-sensitive and un-clocked: the outputs follow `Set` / `Reset` as long
as they are asserted. Clocking and the `D` reduction are added one level up in
`d_latch`.

## Structure

Two `NOr` gates (Digital primitives) cross-coupled. No sub-circuits.

## Notes

- Digital orders the pins of the placed symbol by the vertical position of the
  `In` / `Out` labels. Here that is `Reset, Set` → `Q, ¬Q`; `d_latch` is wired
  to match. If the order is ever changed, fix every parent.
- Real static RAM and register-file bit cells use the same cross-coupled pair,
  usually built from inverters with access transistors rather than NOR gates.

## Status

Saved from Digital. Verify: pulse `Set` → `Q = 1` and stays after `Set`
returns to `0`; pulse `Reset` → `Q = 0` and holds; `Set = Reset = 0` holds the
last value.
