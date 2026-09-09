# d_latch — gated D latch

Turns the `latch_sr` cell into something that stores a **single data bit** on
command. One data input `D` replaces the separate `Set` / `Reset`, and a `Clk`
(enable) line decides whether the latch listens. While `Clk = 1` the latch is
**transparent** — `Q` follows `D`; while `Clk = 0` it **holds** the last value.

> Byte-for-byte copy of the Digital library file `D_latch.dig`. Renamed to
> `d_latch`; the only edit is the `<elementName>` reference to its child, now
> `latch_sr.dig`. `flip_flop_d.dig` references this file as `d_latch.dig`.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Clk` | 1 | `1` = transparent (follow `D`), `0` = hold |
| `D` | 1 | data input |
| `Q` | 1 | stored bit |
| `¬Q` | 1 | its complement |

## How it works

Two AND gates in front of a `latch_sr`:

```
S = D  · Clk          (from the AND fed by D)
R = ¬D · Clk          (from the AND fed by D through a Not)
```

- `Clk = 0` → `S = R = 0` → the SR latch holds. The value is frozen.
- `Clk = 1` → exactly one of `S` / `R` is `1`, following `D`, so `Q` tracks `D`.
- `D` and `¬D` are complementary, so `S` and `R` are never `1` together — the
  forbidden SR input never occurs.

This is a *level*-sensitive latch: any change on `D` while `Clk` is high passes
straight through. Making it react only at a clock **edge** is the job of
`flip_flop_d`.

## Structure

```
d_latch
├─ 2 × And
├─ Not
└─ latch_sr
```

## Notes

- Pin order follows the vertical position of the `In` / `Out` symbols
  (`Clk, D` → `Q, ¬Q`); `flip_flop_d` is wired to match.
- Transparency is the reason latches are not used directly as register storage
  in a synchronous datapath — a long `Clk`-high window lets data ripple through
  several stages. The edge-triggered flip-flop one level up removes that window.

## Status

Simulated in Digital and works: with `Clk = 1`, `Q` follows `D`; with
`Clk = 0`, `Q` holds regardless of `D`.
