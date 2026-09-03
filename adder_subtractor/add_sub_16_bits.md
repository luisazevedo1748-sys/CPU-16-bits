# 16-bit adder / subtractor (AddSub)

This AddSub module is a 16-bit arithmetic unit that performs addition and
subtraction. The design uses a single 16-bit base adder; subtraction is handled
with two's-complement logic, without needing separate add and subtract circuits.
The module is agnostic about signed vs. unsigned numbers — the final
mathematical interpretation is left to software, which reads the status flags.

## Inputs

- **A** — 16 inputs, carrying a number up to 16 bits.
- **B** — 16 inputs, carrying a number up to 16 bits. In subtract mode the
  operation is always `A − B`.
- **Sub** — a 1-bit control pin that enables two's complement: it inverts every
  bit of B and adds 1.

## Outputs

- **Sum** — 16-bit output, the result of the operation.
- **Cout** — carry-out of the top bit of the 16-bit adder (an unsigned
  carry/borrow indicator).

## Status flags

- **SF** — set if the result is negative.
- **ZF** — set if the result is zero.
- **OF** — set on overflow, i.e. if adding two positive numbers gives a negative
  result or vice versa.
