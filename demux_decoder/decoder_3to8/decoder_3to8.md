# 3-to-8 decoder

Takes a 3-bit code and drives one of 8 output lines high. Same idea as the
4-to-16 decoder, one stage smaller — a candidate building block for the
instruction decoder / control-signal fan-out.

> Byte-for-byte copy of the Digital library file. The library file is named
> `Decoder_3to8.dig`; kept here as `decoder_3to8.dig` (repo lowercase
> convention). Nothing references it yet, so no `<elementName>` fix is needed —
> but if a parent block later imports it, either match this name or keep the
> library name in that parent.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `OpCode` | 3 | binary index, 0–7 |
| `Control_Bus` | 8 | one-hot: bit `OpCode` is `1`, the other 7 are `0` |

## How it works

1. **Split** the 3-bit `OpCode` into lines `a b c`.
2. **Complements** `a' b' c'` from three `Not` gates.
3. **Minterms.** Eight 3-input `And` gates, one per output, wired to the
   true/complement mix that is high only for that index
   (`Control_Bus[0] = a'·b'·c'` … `Control_Bus[7] = a·b·c`).
4. Merge the 8 lines into the `Control_Bus` output.

Purely combinational, no enable line.

## Structure

Built directly from primitives: `Splitter`, `Not` (x3), `And` (x8). No
sub-circuits.

## Status

Saved from Digital. Verify: sweep `OpCode` 0→7, `Control_Bus` should be
`1 << OpCode` at each step.
