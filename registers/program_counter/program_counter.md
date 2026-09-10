# program_counter — 16-bit program counter with increment, jump and reset

Holds the address of the current instruction and produces the next one every
clock edge: either `PC + 1` (run straight on) or a supplied `Jump_Addr` (branch
/ jump). `Reset` sends it back to address 0.

> Byte-for-byte copy of the Digital library file `program_counter.dig`. The only
> edit is the `<elementName>` reference to its child, now
> `register_16bits_reset.dig`.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Jump_Addr` | 16 | target address for a jump / branch |
| `Jump_EN` | 1 | `1` = load `Jump_Addr` on the next edge; `0` = load `PC + 1` |
| `Reset` | 1 | `1` = load `0` on the next edge (restart at address 0) |
| `Clk` | 1 | clock |
| `PC_Out` | 16 | current program-counter value (shown in decimal) |

## How it works

- **The counter register** is a `register_16bits_reset`. `PC_Out` is its `Q`,
  fed back into the block.
- **Increment** — a 16-bit `Add` computes `PC_Out + 1` (`Const` = 1, carry-in
  tied low). This is the next sequential address.
- **Next-address select** — a 16-bit 2:1 `Multiplexer` picks what the register
  loads next: input 0 = `PC_Out + 1`, input 1 = `Jump_Addr`, select = `Jump_EN`.
  Its output goes to the register's `Data_In`.
- **Reset** drives the register's `Reset`, so a clock edge with `Reset = 1`
  forces `PC_Out` to 0.
- **Enable** — the register's `EN` is tied to `VDD`: the PC loads on every clock
  edge. There is no stall / hold input yet.

Each edge: `PC_Out` becomes `Jump_Addr` if `Jump_EN`, else `0` if `Reset`, else
`PC_Out + 1`.

## Structure

```
program_counter
├─ register_16bits_reset        16-bit register, synchronous reset
│  └─ register_16bits → register_4bits → flip_flop_d → d_latch → latch_sr
├─ Add          (16-bit, PC + 1)              — Digital primitive
├─ Multiplexer  (16-bit, PC+1 vs Jump_Addr)   — Digital primitive
└─ Const 1 / Ground / VDD
```

## Notes

- **Exception to from-scratch.** The increment uses Digital's native `Add` and
  the next-address choice uses the native `Multiplexer`. The hand-built
  `add_sub_16_bits` would work here bit-for-bit; Digital's `Add` was used because
  that adder was already built and proven for the ALU and a second hand-wired
  16-bit adder here would only repeat that work. Flagged like the ALU 16:1 mux.
  (author's note: *"usei o adder do Digital pois já tinha construído o adder que
  usei na ALU mas ficava mais prático usar o do Digital"*)
- `Jump_EN` and `Reset` both act on the clock edge (synchronous). No branch-delay
  handling — the jump target is whatever is on `Jump_Addr` at the edge.
- `Jump_EN`, `Jump_Addr` and `Reset` are primary inputs for now; the control unit
  will drive them, and add a real hold / stall line in place of the `VDD` on
  `EN`.
- Cross-tree dependency: `register_16bits_reset` lives at
  `registers/register_16bits_reset/` and pulls `register_16bits` from
  `registers/register_file/register_16bits/`. Add both (and the folders below
  them) as custom component search paths when opening from the repo.

## Status

Simulated in Digital and works: from `Reset`, `PC_Out` steps 0, 1, 2, 3, … each
edge; `Jump_EN = 1` with `Jump_Addr = k` makes the next value `k`; `Reset = 1`
returns it to 0.
