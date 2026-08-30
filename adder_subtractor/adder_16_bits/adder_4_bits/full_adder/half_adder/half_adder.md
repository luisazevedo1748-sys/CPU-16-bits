# Half-adder

The half-adder is the elementary combinational arithmetic block in computer
architecture, responsible for adding two individual bits (A and B).

The circuit takes 2 one-bit inputs and produces 2 different outputs. An XOR gate
returns 0 for 0+0 and 1 for 0+1 or 1+0. But 1+1 in binary is `10`, so a single
output is not enough bandwidth — we need a second output called the
**carry-out (Cout)**, which effectively adds a 1 in the next place value. For
that we use an AND gate with its two inputs tied to the two inputs and its
output tied to the carry-out, so when both inputs are 1 the AND sends a 1 to the
carry-out. This is exactly how a half-adder is built in real hardware.

Truth table:

| A | B | Sum | Carry |
|---|---|-----|-------|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
