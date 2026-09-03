# 4-to-16 decoder

Takes a 4-bit code and drives exactly one of 16 output lines high — the classic
one-hot decoder used for register / memory / opcode selection.

> Byte-for-byte copy of the Digital library file (`decoder_4to16bits.dig`).

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `OpCode` | 4 | binary index, 0–15 |
| `Out` | 16 | one-hot: bit `OpCode` is `1`, the other 15 are `0` |

`Out` is a 16-bit bus; reading it as a number gives `1 << OpCode`.

## How it works

1. **Split.** The 4-bit `OpCode` is split into its four lines `a b c d`.
2. **Complements.** A `Not` on each line gives `a' b' c' d'`.
3. **Minterms.** Sixteen 4-input `And` gates, one per output. Output `k` is
   wired to the true/complement mix that is high only for `OpCode = k`
   (e.g. `Out[0] = a'·b'·c'·d'`, `Out[15] = a·b·c·d`).
4. The 16 AND outputs are merged back into the `Out` bus.

Purely combinational, no enable line — one output is always active.

## Structure

Built directly from primitives: `Splitter`, `Not` (x4), `And` (x16). No
sub-circuits.

## Status

Saved from Digital. Verify: sweep `OpCode` 0→15 and check `Out` is `1 << OpCode`
at every step (a single bit set, walking up the bus).
