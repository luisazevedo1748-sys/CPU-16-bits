# NOR gate

Building a NOR gate needs 4 transistors: 2 P-type FETs (PMOS) and 2 N-type FETs
(NMOS).

The 2 PMOS are wired in **series** and connected to VCC (so they pass 1s).
Below, both connect to a node shared with the 2 NMOS, which are wired in
**parallel**; the output is taken from that same node, and GND is connected
below the last NMOS. Each of the 2 inputs drives the gates of one PMOS and one
NMOS.

Full truth table:

| A | B | PMOS A | PMOS B | NMOS A | NMOS B | Output |
|---|---|--------|--------|--------|--------|--------|
| 0 | 0 | ON  | ON  | OFF | OFF | 1 |
| 0 | 1 | ON  | OFF | OFF | ON  | 0 |
| 1 | 0 | OFF | ON  | ON  | OFF | 0 |
| 1 | 1 | OFF | OFF | ON  | ON  | 0 |

Which reduces to the NOR truth table:

| A | B | Output |
|---|---|--------|
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 0 |
