# 16-bit tri-state buffer

Drives a 16-bit word onto a bus when `Enable = 1`, releases the bus (all 16
lines high impedance) when `Enable = 0`. The building block that lets several
units — ALU, registers, memory — share one result bus without conflict, as long
as only one buffer is enabled at a time.

> Byte-for-byte copy of the Digital library file (`tristate_16bits.dig`).

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Data_In` | 16 | word to place on the bus |
| `Enable` | 1 | `1` = drive `Out` with `Data_In`; `0` = `Out` high-Z |
| `Out` | 16 | driven copy of `Data_In`, or all lines floating |

## How it works

Sixteen `switch_1bit` cells in parallel, one per bit, all sharing the same
`Enable`. `Data_In` is split into 16 lines, each line passes through its own
switch, and the outputs are merged back into the `Out` bus.

With `Enable = 0` every switch is open, so `Out` contributes nothing to the bus
and another buffer can drive it. With `Enable = 1` this buffer wins the bus.

## Structure

```
tristate_16bits
└─ switch_1bit   x16   (shared Enable)
   └─ NFET / PFET / Not
```

## Cross-references

`tristate_16bits.dig` references `switch_1bit.dig` (`bus/switch_1bit/`). Add
that folder to Digital's custom component search path when opening this block.

## Status

Saved from Digital. Verify: `Enable = 1` copies all 16 bits; `Enable = 0`
releases the bus; two instances on one bus never both enabled.
