# datapath — register file + ALU + write-back

The **data path** of the CPU: the register file feeds two operands to the ALU,
the ALU computes, and the result (or an external value) is written back into the
register file. Control still comes from outside — every select and enable line
here is a primary input for now — but this is the whole "read → compute →
write-back" loop in one block.

> Byte-for-byte copy of the Digital library file `datapath.dig`. The only edit
> is the `<elementName>` reference to the register file, now `register_file.dig`;
> `ALU.dig` keeps its name and resolves directly.

## Interface

### Inputs

| Pin | Width | Meaning |
|---|---|---|
| `RA1` | 2 | read address → operand A |
| `RA2` | 2 | read address → operand B |
| `WA` | 2 | write address |
| `WE` | 1 | write enable for the register file |
| `Data_In` | 16 | external write-back value (e.g. an immediate or a load) |
| `S` | 1 | write-back source select: `0` = `Data_In`, `1` = ALU `Out` |
| `ALU_Op` | 3 | ALU operation select |
| `Sub` | 1 | ALU add/subtract |
| `MDU_op` | 1 | ALU multiply/divide select |
| `Clk` | 1 | clock |

### Outputs

| Pin | Width | Meaning |
|---|---|---|
| `Out` | 16 | ALU main result |
| `Out_HI/Rest` | 16 | ALU secondary word (MDU product high / remainder) |
| `ZF` `SF` `Cout` `OF` | 1 | ALU arithmetic flags (valid for `ALU_Op = 0`) |
| `Flag_Z` `Flag_RZ` `Flag_N` `Flag_DZ` | 1 | ALU MDU flags (valid for `ALU_Op = 1`) |

## How it works

1. **Read.** `register_file` puts register `RA1` on `Out_A` and register `RA2`
   on `Out_B`, combinationally.
2. **Compute.** `Out_A` → ALU `A`, `Out_B` → ALU `B`. `ALU_Op` / `Sub` /
   `MDU_op` pick the operation; the ALU drives `Out`, `Out_HI/Rest` and all the
   flags straight to the block outputs.
3. **Write-back.** A 16-bit 2:1 `Multiplexer` chooses between `Data_In` and the
   ALU's `Out` using `S`, and feeds `register_file.Data_In`. On the clock edge,
   if `WE = 1`, that value lands in register `WA`.

One clock edge = one register updated. Choosing `RA1` / `RA2` / `WA` / `ALU_Op`
and toggling `S` / `WE` is exactly the job the control unit will take over next.

## Structure

```
datapath
├─ register_file        (4 × register_16bits + demux write, 2× mux read)
├─ ALU                  (add/sub · MDU · shift · logic)
└─ Multiplexer (16-bit) write-back source select (Data_In vs ALU Out)
```

## Notes

- Cross-tree block: opening `datapath.dig` from the repo needs custom component
  search paths for `registers/register_file/` (and the folders below it) and for
  `alu/`, `adder_subtractor/`, `mdu/` and the two shifter folders that `ALU.dig`
  itself pulls in.
- No program counter, instruction memory or decoder yet — those are the next
  blocks (ROADMAP §2–§3). This block is the target they will drive.
- Pin order follows the vertical position of the `In` / `Out` symbols; any
  parent must be wired to match.

## Status

Simulated in Digital and works: two registers loaded via `Data_In` / `WA` /
`WE` (`S = 0`), then with `S = 1` and `ALU_Op` = add the ALU result written back
to a third register matches `Out_A + Out_B`, with `Out` / `ZF` / `SF`
consistent.
