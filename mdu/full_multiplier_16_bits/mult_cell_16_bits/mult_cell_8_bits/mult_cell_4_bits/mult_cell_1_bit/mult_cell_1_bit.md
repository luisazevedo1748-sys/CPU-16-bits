# 1-bit multiplier cell

This circuit is the base block of a combinational array multiplier.

It has 2 stages:

1. **Stage 1** — computes the partial product of 2 bits.
2. **Stage 2** — adds that product to the incoming carry values.

## Note on dependencies

This cell uses the `full_adder.dig` block, which lives under
`adder_subtractor/adder_16_bits/adder_4_bits/full_adder/`. To simulate this
circuit in Digital, add that folder as a library path
(Edit → Settings → *Custom component search path*), or keep a copy of
`full_adder.dig` next to this file.
