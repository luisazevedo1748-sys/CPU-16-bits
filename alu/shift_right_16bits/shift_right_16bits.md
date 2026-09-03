# 16-bit barrel shifter — right

Shifts a 16-bit word right by 0–15 positions in one combinational pass. Used by
the ALU for `ALU_Op = 3`.

> Byte-for-byte copy of the Digital library file; the name `shift_right_16bits`
> is what `ALU.dig` references.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Data_In` | 16 | value to shift |
| `Shamt` | 4 | shift amount, 0–15 |
| `Out` | 16 | `Data_In >> Shamt`, zero-filled from the left |

Logical shift right: bits shifted out of the bottom are discarded, vacated high
bits are filled with `0` (from `Ground`). No sign extension — an arithmetic
right shift would need the top bit fed in instead of `Ground`.

## How it works

Mirror image of the left shifter. Four cascaded `mux_2_1_16bits` stages, one per
`Shamt` bit, each passing straight through or shifting right by a fixed
power-of-two.

| Stage | Select bit | Shift when the bit is 1 |
|---|---|---|
| 1 | `Shamt[0]` | >> 1 |
| 2 | `Shamt[1]` | >> 2 |
| 3 | `Shamt[2]` | >> 4 |
| 4 | `Shamt[3]` | >> 8 |

Each stage's shifted input is the bus re-indexed (bit `i` → bit `i − k`) with
the top `k` bits tied to `Ground`.

## Structure

```
shift_right_16bits
└─ mux_2_1_16bits   x4   (one per Shamt bit)
   └─ mux_2_1_4b
      └─ mux_2_1
```

## Cross-references

`shift_right_16bits.dig` references `mux_2_1_16bits.dig`
(`multiplexer/mux_2_1_16bits/`). Add that folder to Digital's custom component
search path when opening this block.

## Status

Saved from Digital. Verify: `Shamt = 0` is a pass-through; `Shamt = 1` halves an
unsigned value; `Shamt = 15` leaves only the old bit 15 in bit 0; a `1` in the
low bits falls off the end.
