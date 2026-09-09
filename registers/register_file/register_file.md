# register_file — 4 × 16-bit register file (2 read, 1 write)

The CPU's working store: four 16-bit registers with **two independent read
ports** and **one write port**, all addressed by 2-bit register numbers. This is
what the datapath reads operands from and writes results back to every cycle;
the ALU never touches memory directly, only these registers.

> Byte-for-byte copy of the Digital library file `Register_final.dig`. Renamed
> to `register_file` (the standard name for this block); the only edit is the
> `<elementName>` reference to its child, now `register_16bits.dig`.
> `datapath.dig` references this file as `register_file.dig`.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Data_In` | 16 | value to write |
| `WA` | 2 | write address (which of the 4 registers) |
| `WE` | 1 | write enable — `1` = write `Data_In` to register `WA` on the clock edge |
| `RA1` | 2 | read address for port A |
| `RA2` | 2 | read address for port B |
| `Clk` | 1 | clock, common to all four registers |
| `Out_A` | 16 | contents of register `RA1` |
| `Out_B` | 16 | contents of register `RA2` |

## How it works

- **Storage** — four `register_16bits`, each with its own load-enable `EN`.
  `Data_In` and `Clk` are broadcast to all four.
- **Write port** — a `Demultiplexer` (2 select bits) takes `WE` and routes it to
  the `EN` of exactly the register picked by `WA`; the other three see `EN = 0`
  and hold. So one register loads per edge, and only when `WE = 1`.
- **Read ports** — two 16-bit `Multiplexer`s (2 select bits each). One selects a
  register output with `RA1` → `Out_A`, the other with `RA2` → `Out_B`. Reads
  are combinational: `Out_A` / `Out_B` follow the addresses with no clock.
- Reading and writing in the same cycle is fine — the read ports show the *old*
  contents until the edge updates the addressed register.

## Structure

```
register_file
├─ 4 × register_16bits
│  └─ 4 × register_4bits → flip_flop_d → d_latch → latch_sr
├─ Demultiplexer  (2-bit, steers WE to one register's EN by WA)
└─ 2 × Multiplexer (16-bit, 2-bit select — RA1→Out_A, RA2→Out_B)
```

`Demultiplexer` and `Multiplexer` are Digital primitives.

## Notes

- Four registers because the address pins are 2 bits. The final count is an ISA
  decision (see ROADMAP §3); widening `WA` / `RA1` / `RA2` and adding
  `register_16bits` instances scales it.
- Pin order follows the vertical position of the `In` / `Out` symbols; `datapath`
  is wired to match. If it ever comes out wrong, fix with
  *Edit → Order Inputs/Outputs* and re-check `datapath`.
- Opening from the repo: add `registers/register_file/register_16bits/` and the
  folders below it as custom component search paths.

## Status

Saved from Digital. Verify: write a value with `WE = 1`, `WA = k`; read it back
on `RA1 = k` and `RA2 = k`; check the other three registers are untouched and
that `WE = 0` blocks all writes.
