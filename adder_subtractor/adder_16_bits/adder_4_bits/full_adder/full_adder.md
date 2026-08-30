# Full-adder

The full-adder overcomes the half-adder's limitation by adding 3 bits at once:
A, B and the carry-in (Cin). The carry-in is a bit coming from behind — in a
previous column, if we added 1+1 the result was 0 and generated a carry-out,
and that carry-out feeds this carry-in. It is made of 3 inputs (A, B, Cin),
2 half-adders and 2 outputs (Sum and Cout).

The full-adder has 3 stages:

**Stage 1** — the first half-adder takes inputs A and B, computes their sum, and
raises its carry-out if it gets 1+1.

**Stage 2** — the second half-adder takes the first half-adder's sum on one
input and Cin on the other, producing the final sum.

**Stage 3** — the final sum comes out of the second half-adder's sum output. The
carry-out signals from both half-adders go into an OR gate, which raises the
final Cout if either the first or the second addition was 1+1. (Both blocks can
never have their carry-out active at the same time: if the first addition is
1+1, it passes a 0 to input A of the second half-adder.)

Truth table:

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |
