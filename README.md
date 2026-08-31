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
   structure intact. See "Known issues" below.

## Structure

```
logic_gates/
├─ transistors/        N/P-type silicon and MOSFET operation
├─ universal_gates/    NAND, NOR, NOT  (from transistors)
└─ derived_gates/      AND, OR, XOR, XNOR  (from the universal gates)

multiplexer/
└─ mux_16_1 / mux_8_1 / mux_4_1 / mux_2_1   (logic version + transistor-level version)

adder_subtractor/
├─ add_sub_16_bits     16-bit adder/subtractor (two's complement) with SF / ZF / OF flags
└─ adder_16_bits/
   └─ adder_4_bits/ ── full_adder/ ── half_adder/

mdu/   (multiply / divide unit)
├─ full_multiplier_16_bits/     16x16 combinational array multiplier -> 32-bit product + ZF / SF
│  └─ mult_cell_16_bits/ ── mult_cell_8_bits/ ── mult_cell_4_bits/ ── mult_cell_1_bit/
│     array-multiplier row cell, width-extended 1 → 4 → 8 → 16 bits
└─ full_divider_16_bits/        16-bit restoring array divider -> quotient + remainder
   └─ div_cell_16_bits/ ── div_cell_8_bits/ ── div_cell_4_bits/ ── div_cell_1_bit/
      divider row cell, width-extended 1 → 4 → 8 → 16 bits
```

## Module status

| Module | Status |
|--------|--------|
| Transistors and logic gates | Complete |
| Multiplexers (2:1 → 16:1) | Complete |
| 16-bit adder / subtractor + flags | Complete |
| Multiply/divide unit (MDU) | In progress (16x16 multiplier done; 16-bit divider drafted, has a pin-order bug) |
| ALU | Not started |
| Registers and memory | Not started |
| Control unit | Not started |
| Datapath / CPU | Not started |

See [`ROADMAP.md`](ROADMAP.md) for the detailed plan.

## Known issues

- `mdu/.../mult_cell_1_bit.dig` references `full_adder.dig`, which lives in the
  `adder_subtractor/` tree. Digital only searches sub-directories of the circuit
  being simulated, so add that folder as a custom component search path (or keep
  a local copy) to simulate the MDU blocks.

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
