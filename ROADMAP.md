# Roadmap — 16-bit CPU

Build plan, from the lowest layers up to the top. Each item is a candidate for
its own commit once it works.

## 0. Fundamentals — done

- [x] Transistors (N/P silicon, MOSFET, threshold voltage)
- [x] Universal gates: NAND, NOR, NOT
- [x] Derived gates: AND, OR, XOR, XNOR

## 1. Combinational blocks

- [x] Multiplexers 2:1, 4:1, 8:1, 16:1
- [x] Half-adder, full-adder
- [x] Ripple-carry adder, 4-bit and 16-bit
- [x] 16-bit adder/subtractor with two's complement and SF / ZF / OF flags
- [ ] Demultiplexer / decoder (for register and memory selection)
- [ ] 16-bit barrel shifter (logical/arithmetic, left/right)
- [x] MDU — 16-bit multiplier (16x16 combinational array → 32-bit product)
  - [x] 1-bit and 4-bit multiplier cells
  - [x] row-cell width extension: 4 → 8 → 16 bits
  - [x] stack 16 rows into the full 16x16 array
- [~] MDU — 16-bit divider (restoring array, quotient + remainder)
  - [x] 1-bit / 4-bit / 8-bit / 16-bit divider cells, width-extended
  - [x] stack 16 rows into the full array
  - [ ] fix the div_cell_* pin-order bug (undefined wire in div_cell_8_bits)
  - [ ] verify against a test program
- [ ] **16-bit ALU** — combine add/subtract, logic, shift and MDU under an
      operation selector

## 2. Sequential blocks

- [ ] SR latch
- [ ] D flip-flop (clocked)
- [ ] 16-bit register
- [ ] Register file (register count defined by the ISA)
- [ ] Program counter (counter with load)
- [ ] RAM

## 3. Control

- [ ] Define the ISA — see `docs/isa.md` (to be created):
  - number and width of registers
  - 16-bit instruction format (opcode bits vs. operand bits)
  - addressing modes
  - load/store or not
- [ ] Instruction decoder
- [ ] State machine / control signals (fetch → decode → execute)

## 4. Integration

- [ ] Full datapath (PC → memory → registers → ALU → write-back)
- [ ] Execute the first instruction
- [ ] Test program in memory
- [ ] CPU running a complete program

## Technical debt / cleanup

- [x] Rename folders and files to English, no spaces or accents
- [x] Convert all notes from `.txt` to `.md`
- [x] Fix broken `.dig` cross-references (`full_adder.dig` / `half_adder.dig`)
- [x] Fix the XNOR truth table (it previously showed the XOR table)
- [ ] Reorganise into layers: `00_transistors/`, `01_gates/`, `02_combinational/`,
      `03_sequential/`, `04_control/`, `05_cpu/`
- [x] Fill in `mult_cell_4_bits.md` (was a stub) under `mdu/.../mult_cell_4_bits/`
- [ ] Resolve the cross-tree `mult_cell_1_bit.dig` → `full_adder.dig` dependency
