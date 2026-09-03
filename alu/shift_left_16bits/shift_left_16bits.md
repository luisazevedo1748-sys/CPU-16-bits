# 16-bit barrel shifter — left

Shifts a 16-bit word left by 0–15 positions in one combinational pass. Used by
the ALU for `ALU_Op = 2`.

> Byte-for-byte copy of the Digital library file; the name `shift_left_16bits`
> is what `ALU.dig` references.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Data_In` | 16 | value to shift |
| `Shamt` | 4 | shift amount, 0–15 |
| `Out` | 16 | `Data_In << Shamt`, zero-filled from the right |

Logical shift: bits shifted out of the top are discarded, vacated low bits are
filled with `0` (from `Ground`).

## How it works

A barrel shifter: four cascaded stages, one per bit of `Shamt`, each a
`mux_2_1_16bits` that either passes its input straight through or shifts it by a
fixed power-of-two amount.

| Stage | Select bit | Shift when the bit is 1 |
|---|---|---|
| 1 | `Shamt[0]` | << 1 |
| 2 | `Shamt[1]` | << 2 |
| 3 | `Shamt[2]` | << 4 |
| 4 | `Shamt[3]` | << 8 |

The fixed wiring per stage is just a re-indexing of the bus (bit `i` → bit
`i + k`), with the low `k` bits tied to `Ground`. Summing the enabled stages
gives any shift from 0 (all select bits 0, straight through) to 15.

## Structure

```
shift_left_16bits
└─ mux_2_1_16bits   x4   (one per Shamt bit)
   └─ mux_2_1_4b
      └─ mux_2_1
```

## Cross-references

`shift_left_16bits.dig` references `mux_2_1_16bits.dig`
(`multiplexer/mux_2_1_16bits/`). Add that folder to Digital's custom component
search path when opening this block.

## Status

Saved from Digital. Verify: `Shamt = 0` is a pass-through; `Shamt = 1` doubles;
`Shamt = 15` leaves only the old bit 0 in bit 15; a `1` in the top bits falls
off the end.
