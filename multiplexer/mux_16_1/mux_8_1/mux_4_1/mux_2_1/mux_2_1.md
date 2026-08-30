# 2:1 Multiplexer

A multiplexer works as a digital selector: its job is to take several input data
channels and let only one through to the output, blocking the rest.

A 2:1 mux has 2 data inputs (D0 and D1), 1 select pin (S) and 1 output (Y). The
rule: if S = 0 then Y = D0 (only D0 reaches the output); if S = 1 then Y = D1.

The behaviour of a 2:1 mux is described by the logic equation:
`Y = (D0 · ¬S) + (D1 · S)`

Truth table:

| S | D1 | D0 | Output |
|---|----|----|--------|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

If a 2:1 mux were built exactly like this in real hardware it would use 20
transistors. In practice, to save space and power, the AND and OR gates are
dropped and replaced with **transmission gates**, which act as bidirectional
switches. This shrinks the circuit to just 6 transistors: 2 transmission gates
and 1 inverter for the select signal.

## Files

- `mux_2_1.dig` — logic-gate version
- `mux_2_1_real.dig` — transmission-gate (transistor-level) version
