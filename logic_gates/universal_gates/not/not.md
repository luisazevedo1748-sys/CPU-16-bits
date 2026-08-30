# NOT gate (inverter)

Building a NOT gate needs 2 transistors: 1 P-type FET (PMOS) and 1 N-type FET
(NMOS).

VCC connects to the PMOS (so it passes 1s), and the NMOS sits in series below
it. The output is taken from a node between the two transistors, and the input
drives the gates of both the PMOS and the NMOS.

Full truth table:

| A | PMOS | NMOS | Output |
|---|------|------|--------|
| 0 | ON  | OFF | 1 |
| 1 | OFF | ON  | 0 |

Which reduces to the NOT truth table:

| A | Output |
|---|--------|
| 0 | 1 |
| 1 | 0 |
