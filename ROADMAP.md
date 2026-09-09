# Roadmap — 16-bit CPU

Build plan, from the lowest layers up to the top. Each item is a candidate for
its own commit once it works.

## 0. Fundamentals — done

- [x] Transistors (N/P silicon, MOSFET, threshold voltage)
- [x] Universal gates: NAND, NOR, NOT
- [x] Derived gates: AND, OR, XOR, XNOR

## 1. Combinational blocks

- [x] Multiplexers 2:1, 4:1, 8:1, 16:1
- [x] Wide 2:1 bus multiplexers: 4-bit and 16-bit (`mux_2_1_4b`, `mux_2_1_16bits`)
- [x] Half-adder, full-adder
- [x] Ripple-carry adder, 4-bit and 16-bit
- [x] 16-bit adder/subtractor with two's complement and SF / ZF / OF flags
- [~] Demultiplexer / decoder (for register and memory selection)
      — `decoder_4to16bits` (4→16 one-hot) and `decoder_3to8` (3→8 one-hot)
      drafted from Digital under `demux_decoder/`
- [~] 16-bit barrel shifter (logical/arithmetic, left/right)
      — `shift_left_16bits` / `shift_right_16bits` drafted (logical only, 4
      barrel stages from `mux_2_1_16bits`); arithmetic right shift still to do
- [~] Bus primitives — `switch_1bit` (CMOS transmission gate) and
      `tristate_16bits` (16-bit tri-state bus driver) drafted under `bus/`
- [x] MDU — 16-bit multiplier (16x16 combinational array → 32-bit product)
  - [x] 1-bit and 4-bit multiplier cells
  - [x] row-cell width extension: 4 → 8 → 16 bits
  - [x] stack 16 rows into the full 16x16 array
- [x] MDU — 16-bit divider (restoring array, quotient + remainder)
  - [x] 1-bit / 4-bit / 8-bit / 16-bit divider cells, width-extended
  - [x] stack 16 rows into the full array
  - [x] simulates correctly — `100 ÷ 7` → quotient 14, remainder 2 (the stacked
        cells order their pins by symbol position; each parent is wired to match)
- [x] MDU — top-level `MDU.dig`: multiplier + divider behind `MDU_op`, shared
      `LO` / `HI` outputs and `Flag_Z / N / RZ / DZ`
- [~] **16-bit ALU** — combine add/subtract, logic, shift and MDU under an
      operation selector. `alu/ALU.dig` from Digital: `ALU_Op` (3-bit) selects
      add/sub · MDU · shift-left · shift-right · AND · OR · XOR, with
      `Out` / `Out_HI` and the arithmetic (`ZF/SF/Cout/OF`) + MDU
      (`Flag_Z/RZ/N/DZ`) flags. Checked with `A=100, B=7`: `ALU_Op=2` →
      `Out=12800` (`100<<7`), `Out_HI=2` (MDU remainder). Sweep the remaining
      opcodes to finish.

## 2. Sequential blocks

- [x] SR latch — `latch_sr`, cross-coupled NOR pair, under `registers/`
- [x] Gated D latch — `d_latch` (2 AND + Not in front of `latch_sr`)
- [x] D flip-flop (clocked) — `flip_flop_d`, master–slave (two `d_latch`,
      clock inverted between them); simulates correctly
- [x] 16-bit register — `register_4bits` (4 × `flip_flop_d` + a D-vs-`Q`
      load-enable mux), width-extended to `register_16bits` (4 × `register_4bits`)
- [x] Register file — `register_file`, 4 × `register_16bits` with a demux write
      port (`WE` steered by `WA`) and two 16-bit read-port muxes (`RA1`/`RA2`);
      4 registers for now (2-bit addresses), final count is an ISA decision
- [ ] Program counter — 16-bit register with load and increment.
      **Exception to from-scratch:** the PC uses Digital's **native register**
      block for its storage, because it must hold a defined `0` at power-on,
      before any software runs — otherwise the first fetch reads a random
      address and the machine crashes with no chance for code to recover. A
      scratch register plus a hand-drawn 16-bit synchronous reset (16 AND gates
      + a reset net) would do the job but is pure mechanical wiring that adds
      nothing to the exercise; the retention logic itself is already proven by
      `latch_sr` → … → `register_16bits`. Same kind of pragmatic exception as
      the ALU's 16:1 output mux. General-purpose registers stay hand-built and
      reset-free (see `register_16bits.md`).
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

- [~] Full datapath (PC → memory → registers → ALU → write-back)
      — `datapath/datapath.dig` from Digital: `register_file` → `ALU` →
      write-back mux (`S` picks `Data_In` vs ALU `Out`). Register read →
      compute → write-back simulates correctly; PC, instruction memory and the
      decoder still to come, and every control line is a primary input for now
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
