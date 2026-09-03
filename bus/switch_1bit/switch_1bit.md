# 1-bit switch (transmission gate)

A single-bit pass gate: connects `Data_In` to `Out` when `Enable = 1`, and lets
`Out` float (high impedance) when `Enable = 0`. The leaf cell of the 16-bit
tri-state buffer, and the primitive needed to drive a shared bus from more than
one source.

> Byte-for-byte copy of the Digital library file; the name `switch_1bit` is
> what `tristate_16bits.dig` references.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Data_In` | 1 | value to pass |
| `Enable` | 1 | `1` = connect `Data_In` to `Out`; `0` = `Out` high-Z |
| `Out` | 1 | driven copy of `Data_In`, or floating |

## How it works

A CMOS transmission gate: an `NFET` and a `PFET` in parallel between `Data_In`
and `Out`. `Enable` drives the NFET gate directly and, through a `Not`, the PFET
gate. When `Enable = 1` both transistors conduct and pass a full-swing signal in
either direction; when `Enable = 0` both are off and `Out` is isolated.

Unlike a plain mux, an off switch does not force a `0` — it disconnects, so
several switches can share one output node with only one enabled at a time.

## Structure

Built from transistor primitives: `NFET`, `PFET`, `Not`. No sub-circuits.

## Status

Saved from Digital. Verify: `Enable = 1` copies `Data_In` to `Out` for both
levels; `Enable = 0` leaves `Out` floating (in Digital, shown as `Z` / a
"not connected" reading unless another driver holds the node).
