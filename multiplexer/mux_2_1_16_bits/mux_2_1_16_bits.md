# 16-bit-wide 2:1 multiplexer

A full 16-bit bus 2:1 multiplexer: it selects one of two 16-bit words and puts
it on a 16-bit output, all bits switched by one common select line. This is the
building block used to steer 16-bit datapaths (operand routing, result
selection) in the MDU and, later, the ALU.

## Interface

- **In_0** — 16-bit input, passed through when `S = 0`.
- **In_1** — 16-bit input, passed through when `S = 1`.
- **S** — 1-bit select.
- **Out** — 16-bit output.

## How it works

Each 16-bit input is split into four nibbles (`Splitter` `16 → 4,4,4,4`).
Nibble *i* of `In_0` and nibble *i* of `In_1` feed a `mux_2_1_4_bits`, and all
four share the same `S`. The four selected nibbles are re-joined into the
16-bit `Out` bus. Purely a width extension over `mux_2_1_4_bits`.

## Structure

```
mux_2_1_16_bits
└─ 4 × mux_2_1_4_bits
   └─ 4 × mux_2_1
```

## Notes

- Pin order in Digital is set by the vertical position of the `In`/`Out`
  symbols. Parents wire this as `In_0, In_1, S` → `Out`; if the order ever comes
  out wrong, fix it with *Edit → Order Inputs/Outputs* and re-check every
  parent.
- The nibble grouping (`4,4,4,4`) is only for wiring convenience; a single
  `16 → 1×16` split into sixteen `mux_2_1` would be logically identical.
