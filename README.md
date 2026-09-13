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

demux_decoder/                  (standalone; CPU.dig's own two-level decoding
├─ decoder_4to16bits/            uses Digital's native Decoder directly, not
└─ decoder_3to8/                 these hand-built blocks)

bus/
├─ tristate_16bits.dig          16-bit tri-state bus driver (Enable -> drive / high-Z)
└─ switch_1bit/                 1-bit CMOS transmission gate (leaf of tristate_16bits)

registers/   (sequential storage)
├─ register_file/               4 x 16-bit register file, 2 read + 1 write port
│  └─ register_16bits/          16-bit register, load enable (4 x register_4bits)
│     └─ register_4bits/        4-bit register, D-vs-Q mux for load enable
│        └─ flip_flop_d/        edge-triggered D flip-flop (master-slave)
│           └─ d_latch/         gated D latch
│              └─ latch_sr/     NOR SR latch (the bistable cell)
├─ register_16bits_reset/       register_16bits + a data-vs-0 mux -> synchronous reset
└─ program_counter/             PC: register_16bits_reset + native Add (+1) + jump mux

memory/
├─ ROM.dig                      4-word demonstration ROM (mux + constants);
│                               the real instruction memory uses Digital's native ROM
└─ RAM.dig                      16 x 16-bit data memory, decoder + one register
                                per word, 16 x tristate_16bits on a shared output bus

datapath/   (register file + ALU + write-back)
└─ datapath.dig                 RA1/RA2 -> ALU -> write-back to WA, plus
                                RegA_Out/RegB_Out taps used by the CPU's
                                address and store logic

cpu/   (everything joined: fetch, decode, execute)
└─ CPU.dig                      ROM + IR + PC + two-level decoder (opcode + funct)
                                + datapath + RAM + stack pointer + HI register +
                                auto-reset + HLT latch -> a complete processor

assembler/                      asm16.py, a two-pass assembler with labels for the ISA
└─ examples/                    sample .asm programs and one assembled .hex
```

## Module status

| Module | Status |
|--------|--------|
| Transistors and logic gates | Complete |
| Multiplexers (2:1 → 16:1) | Complete |
| 16-bit adder / subtractor + flags | Complete |
| Multiply/divide unit (MDU) | 16x16 multiplier done; divider simulates correctly (`100 ÷ 7` → 14 r 2); top-level `MDU.dig` wraps both behind `MDU_op` |
| 16-bit barrel shifters (left / right) | Complete — logical + arithmetic right shift, simulate correctly |
| ALU | Complete — every `ALU_Op` swept in Digital, all operations work |
| Decoders (4→16, 3→8) | Complete |
| Bus primitives (`switch_1bit`, `tristate_16bits`) | Complete |
| Registers and memory | `latch_sr` → `d_latch` → `flip_flop_d` → `register_4bits` → `register_16bits` → `register_file` (4 × 16-bit, 2 read / 1 write), plus `register_16bits_reset` (synchronous reset), `program_counter` (+1 / jump / reset), a 4-word demo `ROM`, and a 16-word `RAM` (decoder + tristate output bus) — all simulate correctly in Digital |
| Control unit | Complete — built into `cpu/CPU.dig`: a two-level decoder (primary opcode, secondary `funct` for opcode `0000`) drives every control signal (`WE`, `S`, `Sub`, `ALU_Op`, `MDU_op`, `Jump_EN`, stack/HI enables) |
| Datapath / CPU | `datapath.dig` (register file + ALU + write-back, plus `RegA_Out`/`RegB_Out`) and `cpu/CPU.dig` (the full processor: ROM, instruction register, PC, decoder, datapath, RAM, stack pointer, `HI` register, auto-reset, `HLT` latch) — validated with hand-assembled test programs (fetch, every ALU op, RAM load/store, the stack, function calls, `MFHI`, `HLT`). See `cpu/CPU.md` for the ISA, encoding, and every design decision |
| Assembler | Complete — `assembler/asm16.py`, a two-pass Python assembler with label support for the ISA in `cpu/CPU.md` |

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
- `registers/` blocks: each block sits one folder above its child, so add the
  nested folders down to `latch_sr/` when opening `register_file.dig`,
  `register_16bits.dig` or `register_4bits.dig`.
- `registers/register_16bits_reset/` and `registers/program_counter/`: both reuse
  `register_16bits` from `registers/register_file/register_16bits/` (it is not
  copied into their folders), so add that folder and the ones below it.
  `program_counter.dig` also needs `registers/register_16bits_reset/`.
- `memory/ROM.dig`: self-contained (only Digital primitives), no search path
  needed.
- `datapath/datapath.dig`: add `registers/register_file/` (and the folders below
  it) plus everything `alu/ALU.dig` needs — `alu/`, `adder_subtractor/`, `mdu/`
  and the two shifter folders under `alu/`.
- `memory/RAM.dig`: add `registers/register_file/register_16bits/` (and the
  folders below it) and `bus/` (for `tristate_16bits.dig`, which itself needs
  `bus/switch_1bit/`).
- `cpu/CPU.dig`: the top of the tree, add `memory/`, `registers/register_16bits_reset/`,
  `registers/register_file/register_16bits/` (and below), `registers/program_counter/`
  (and everything it needs), and `datapath/` (and everything it needs, see above).
  `register_16bits` is instanced twice here — once for the stack pointer, once for
  the `HI` register. The instruction and secondary decoders are Digital's native
  `Decoder`, not `demux_decoder/`'s hand-built blocks; the bus-selection muxes are
  Digital's native `Multiplexer`, not the hand-built `mux_*` blocks.

The wide bus muxes keep their library names (`mux_2_1_16bits`, `mux_2_1_4b`) and
the shifters keep theirs (`shift_left_16bits`, `shift_right_16bits`), so parents
resolve them with no `.dig` edit. The sequential blocks were renamed from their
library names (`Latch_SR`, `D_latch`, `flip_flop_D`, `Registo_4bits`,
`Registro_16bits`, `Register_final`, `Registo16bits_reset`); each parent's
`<elementName>` reference was updated to the new child name, with no other change
to the `.dig`. `datapath.dig` and `program_counter.dig` keep their library names;
`program_counter.dig`'s reference to its child was updated to
`register_16bits_reset.dig`. `ROM.dig` keeps its library name and was not edited
(it uses only Digital primitives). `RAM.dig` was renamed from the library's
`RAM 16x16 bits.dig` (spaces aren't allowed); `cpu/CPU.dig` was renamed from the
library's `cpu.dig` to match the acronym-filename style of `ALU.dig`/`MDU.dig`/`ROM.dig`.
Both parents' `<elementName>` references to their renamed children were updated
the same way.

## Conventions

- File and folder names: lowercase, `snake_case`, no spaces or accents.
- One commit per completed block, with a message describing what was done.
- Tags at important milestones (e.g. `alu-working`, `first-instruction`).

## Exceptions to from-scratch

Nearly every block is built bottom-up from transistors and logic gates. A few
are not, for practical reasons, and each is flagged in its own `.md`:

- **ALU result mux** — the 16-bit, 8-way output multiplexer in `alu/ALU.dig`
  uses Digital's native `Multiplexer`. Building it by hand is 500+ connections
  on one sheet.
- **Program counter increment** — `registers/program_counter/program_counter.dig`
  uses Digital's native `Add` for `PC + 1`. The hand-built `add_sub_16_bits`
  works here bit-for-bit; the adder was already built and proven for the ALU, so
  a second hand-wired one would only repeat that work.
- **Instruction memory** — the CPU uses Digital's native `ROM`. A 16-bit
  address space is 65536 words; `memory/ROM.dig` is a hand-built 4-word demo of
  what a ROM does, not the memory the CPU runs from.
- **Power-on reset generator** — `cpu/CPU.dig` uses Digital's native `Counter`
  to hold `Reset` high for the first few cycles at startup. In real chips this is
  an analog circuit that waits for the supply voltage to stabilize; Digital
  doesn't simulate voltages, so there's no from-scratch digital equivalent to
  build. See `cpu/CPU.md` for why a hand-built register can't do this job.

## Authorship

All circuits in this repository were designed and built by me in the Digital
simulator — the transistor-level gates, the adders, the multiplexers, the
multiplier cells and every wiring decision (bar the few native-component
exceptions noted above). The explanations in each `.md` reflect my own
understanding of how the blocks work.

AI assistance (Claude) was used only for the work around the circuits: tidying
the folder layout, drafting and copy-editing the `.md` documentation, fixing
file names and broken cross-references, and writing commit messages.
AI-assisted commits carry a `Co-Authored-By` trailer.
