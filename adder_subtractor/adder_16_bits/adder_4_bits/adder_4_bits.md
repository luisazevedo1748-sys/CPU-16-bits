# 4-bit adder

The 4-bit adder raises our capacity to start processing packets of data: instead
of adding a single column, this component groups 4 full-adder blocks.

The method is called a **ripple-carry adder**. The main rule is column
isolation: each block's sum goes straight to its own final output, and the only
information carried between blocks is the carry — the Cout of one block connects
to the Cin of the next, and the Cout of the last block goes to a carry-out
output.

The structure has 9 inputs and 5 outputs, in 3 stages:

**Stage 1 (bit 0)** — the first full-adder takes 3 individual bits and adds
them; this is the least significant bit of the final number, and its sum goes to
Sum0. If it gets 1+1 it activates the next block's Cin; if it gets 1+1+1 it
activates both the next block's Cin and Sum0.

**Stage 2 (bits 1 and 2)** — the same logic as stage 1 applies to the second and
third full-adders, but for more significant bits.

**Stage 3 (bit 3)** — the fourth and last full-adder processes the most
significant bit with the same logic. If the result needs 5 bits it activates the
Cout output.
