# 16-bit CPU

A **from-scratch** 16-bit processor built in the
[Digital](https://github.com/hneemann/Digital) logic simulator, starting from
semiconductor physics and working up block by block to a complete CPU.

Each block has three files:

| File | What it is |
|------|------------|
| `name.dig` | The circuit, to open in Digital |
| `name.png` | Screenshot of the circuit |
| `name.md`  | Theory: purpose, interface, stage-by-stage operation, truth table, and notes on how it is done in real hardware |

## Opening the circuits

1. Download [Digital](https://github.com/hneemann/Digital/releases) (needs Java).
2. Open the `.dig` file you want.
3. Composite circuits reference their sub-circuits by file name — keep the folder
   structure intact. See "Opening the mirrored circuits" below.

## Structure

```
logic_gates/
├─ transistors/        N/P-type silicon and MOSFET operation
├─ universal_gates/    NAND, NOR, NOT  (from transistors)
└─ derived_gates/      AND, OR, XOR, XNOR  (from the universal gates)

multiplexer/
├─ mux_16_1 / mux_8_1 / mux_4_1 / mux_2_1   (logic version + transistor-level version)
│                                           mux_16_1 takes its 16 data lines as one D_In bus
└─ mux_2_1_16bits/                          16-bit-wide 2:1 bus mux
   └─ mux_2_1_4b/                            4-bit-wide 2:1 bus mux  (both from mux_2_1)

adder_subtractor/
├─ add_sub_16_bits     16-bit adder/subtractor (two's complement) with SF / ZF / OF flags
└─ adder_16_bits/
   └─ adder_4_bits/ ── full_adder/ ── half_adder/

mdu/   (multiply / divide unit)
├─ MDU.dig                      multiplier + divider behind one MDU_op selector -> LO / HI + flags
├─ full_multiplier_16_bits/     16x16 combinational array multiplier -> 32-bit product + ZF / SF
│  └─ mult_cell_16_bits/ ── mult_cell_8_bits/ ── mult_cell_4_bits/ ── mult_cell_1_bit/
│     array-multiplier row cell, width-extended 1 → 4 → 8 → 16 bits
└─ full_divider_16_bits/        16-bit restoring array divider -> quotient + remainder + FDZ/FRZ/FN flags
   └─ div_cell_16_bits/ ── div_cell_8_bits/ ── div_cell_4_bits/ ── div_cell_1_bit/
      divider row cell, width-extended 1 → 4 → 8 → 16 bits

alu/   (16-bit arithmetic / logic unit)
├─ ALU.dig                      add/sub + MDU + shift + logic behind ALU_Op -> Out / Out_HI + flags
├─ shift_left_16bits/           16-bit barrel shifter, left  (4 x mux_2_1_16bits)
└─ shift_right_16bits/          16-bit barrel shifter, right (4 x mux_2_1_16bits)

demux_decoder/
├─ decoder_4to16bits/           4-bit code -> one-hot 16-bit bus (register / opcode select)
└─ decoder_3to8/                3-bit code -> one-hot 8-bit control bus

bus/
├─ tristate_16bits.dig          16-bit tri-state bus driver (Enable -> drive / high-Z)
└─ switch_1bit/                 1-bit CMOS transmission gate (leaf of tristate_16bits)
```

## Module status

| Module | Status |
|--------|--------|
| Transistors and logic gates | Complete |
| Multiplexers (2:1 → 16:1) | Complete |
| 16-bit adder / subtractor + flags | Complete |
| Multiply/divide unit (MDU) | 16x16 multiplier done; divider simulates correctly (`100 ÷ 7` → 14 r 2); top-level `MDU.dig` wraps both behind `MDU_op` |
| 16-bit barrel shifters (left / right) | Drafted from Digital |
| ALU | Drafted (add/sub, shift, logic paths compose working blocks; shift + MDU-remainder paths spot-checked with `A=100, B=7`) |
| Decoders (4→16, 3→8) | Drafted from Digital |
| Bus primitives (`switch_1bit`, `tristate_16bits`) | Drafted from Digital |
| Registers and memory | Not started |
| Control unit | Not started |
| Datapath / CPU | Not started |

See [`ROADMAP.md`](ROADMAP.md) for the detailed plan.

## Opening the mirrored circuits

Every `.dig` here is a byte-for-byte copy of the file in the Digital library
folder, laid out in a folder tree for version control. In the library folder
they all sit side by side, so everything resolves directly. When opening a
composite block **from this repo**, add the folders holding its sub-circuits as
custom component search paths (Edit → Settings), because Digital only searches
sub-directories of the file it opens:

- MDU / multiplier / divider blocks: add `adder_subtractor/` (for
  `full_adder.dig`) and `multiplexer/`.
- `mdu/MDU.dig`: also add `mdu/full_divider_16_bits/` and
  `multiplexer/mux_2_1_16bits/`. `MDU.dig` names the divider `full_division.dig`
  (its library name); this repo's copy of that block is
  `mdu/full_divider_16_bits/full_divider_16_bits.dig`.
- `alu/ALU.dig`: add `adder_subtractor/`, `mdu/`, and the two shifter folders
  under `alu/`.

The wide bus muxes keep their library names (`mux_2_1_16bits`, `mux_2_1_4b`) and
the shifters keep theirs (`shift_left_16bits`, `shift_right_16bits`), so parents
resolve them with no `.dig` edit.

`.png` screenshots for the shifters, `decoder_3to8`, `tristate_16bits` and
`switch_1bit` are still to be exported from Digital.

## Conventions

- File and folder names: lowercase, `snake_case`, no spaces or accents.
- One commit per completed block, with a message describing what was done.
- Tags at important milestones (e.g. `alu-working`, `first-instruction`).

## Authorship

All circuits in this repository were designed and built by me in the Digital
simulator — the transistor-level gates, the adders, the multiplexers, the
multiplier cells and every wiring decision. The explanations in each `.md`
reflect my own understanding of how the blocks work.

AI assistance (Claude) was used only for the work around the circuits: tidying
the folder layout, drafting and copy-editing the `.md` documentation, fixing
file names and broken cross-references, and writing commit messages.
AI-assisted commits carry a `Co-Authored-By` trailer.
