# 4:1 Multiplexer

The 4:1 mux has the same goal as the 2:1 but takes 4 inputs (D0, D1, D2, D3).
Selecting 1 of the 4 needs 2 select signals (S0 and S1). It is built from three
2:1 muxes in cascade, in 2 stages:

**Stage 1 (pre-selection)** — two 2:1 muxes in parallel, both sharing the least
significant select bit (S0). The upper block picks between D0 and D1, the lower
block picks between D2 and D3.

**Stage 2 (final decision)** — the third 2:1 mux takes the two signals chosen in
stage 1, and the most significant select bit (S1) picks which one reaches the
output.

Truth table:

| S1 | S0 | Output |
|----|----|--------|
| 0 | 0 | D0 |
| 0 | 1 | D1 |
| 1 | 0 | D2 |
| 1 | 1 | D3 |

In real hardware this is exactly the same, but using the real
(transmission-gate) 2:1 mux described in `mux_2_1.md`. So instead of 60
transistors for a 4:1 mux, only 18 are used.
