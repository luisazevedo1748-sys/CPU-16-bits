# 4-bit-wide 2:1 multiplexer

A bus version of the plain `mux_2_1`: it routes one of two **4-bit** inputs to a
4-bit output under a single select line. Same selector for all four bits, so the
whole nibble switches together.

## Interface

- **In_0** — 4-bit input, passed through when `S = 0`.
- **In_1** — 4-bit input, passed through when `S = 1`.
- **S** — 1-bit select.
- **Out** — 4-bit output.

## How it works

The two 4-bit inputs are split into individual bits (`Splitter` `4 → 1,1,1,1`).
Bit *i* of `In_0` and bit *i* of `In_1` feed a `mux_2_1`, and every `mux_2_1`
shares the same `S`. The four 1-bit results are re-joined into the 4-bit `Out`
bus. No logic beyond the four leaf muxes — it is purely a width extension.

## Structure

```
mux_2_1_4_bits
└─ 4 × mux_2_1
```

`mux_2_1` is reused from the multiplexer tree
(`multiplexer/mux_16_1/mux_8_1/mux_4_1/mux_2_1/`); in Digital its folder must be
on the component search path when this block is opened on its own.

## Notes

Pin order in Digital follows the vertical position of the `In`/`Out` symbols. If
a parent circuit wires this block as `In_0, In_1, S`, confirm the symbols are
stacked in that order (or fix it with *Edit → Order Inputs/Outputs*).
