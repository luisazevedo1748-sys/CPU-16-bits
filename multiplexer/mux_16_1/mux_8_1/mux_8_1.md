# 8:1 Multiplexer

The 8:1 mux works like the 4:1 and 2:1, but selects 1 data path out of 8 inputs
(D0 to D7) for a single output (Y). This needs 3 control bits (S2, S1, S0).

Following the same logic as the 4:1 mux, the process has 2 stages:

**Stage 1 (pre-selection)** — two 4:1 mux blocks operate in parallel, sharing
the 2 least significant select bits (S1 and S0). The upper block picks between
D0 and D3, the lower block picks between D4 and D7.

**Stage 2 (final decision)** — a 2:1 mux block takes the 2 filtered signals and
uses the most significant select bit (S2) to make the final decision and route
the chosen input to the output (Y).

Truth table:

| S2 | S1 | S0 | Output |
|----|----|----|--------|
| 0 | 0 | 0 | D0 |
| 0 | 0 | 1 | D1 |
| 0 | 1 | 0 | D2 |
| 0 | 1 | 1 | D3 |
| 1 | 0 | 0 | D4 |
| 1 | 0 | 1 | D5 |
| 1 | 1 | 0 | D6 |
| 1 | 1 | 1 | D7 |
