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
- [x] Register with synchronous reset — `register_16bits_reset`, a
      `register_16bits` with a data-vs-`0` mux on `D` (`Reset` selects `0`). The
      "with reset" variant; plain `register_16bits` is the "without" one, choice
      made per use.
- [x] Program counter — `registers/program_counter/`, a `register_16bits_reset`
      + Digital's native `Add` for `PC + 1` + a mux picking `PC + 1` vs
      `Jump_Addr` (`Jump_EN`); `Reset` clears to 0. Simulates correctly
      (steps 0, 1, 2, …; jumps on `Jump_EN`; `Reset` → 0). The native `Add` is a
      stated from-scratch exception — the ALU's `add_sub_16_bits` is already
      built and proven.
- [x] Instruction memory (ROM) — `memory/ROM.dig`, a hand-built 4-word demo
      (mux + hardwired constants + an output-enable mux), simulates correctly.
      The CPU will use Digital's native `ROM` for the full 16-bit address space.
- [x] RAM — `memory/RAM.dig`, 16 x 16-bit words: a 4-bit decoder picks one
      one-hot line per word, gating that word's register `EN` (write) and its
      `tristate_16bits` `Enable` (read) independently; all 16 tristates share one
      output bus. Simulates correctly

## 3. Control

- [x] Define the ISA — 4 registers, 16-bit R/I/J/F instruction formats, 16
      opcodes plus an 8-way `funct` field under opcode `0000`, load/store via
      `LOAD`/`STORE`, a stack (`PUSH`/`POP`/`CALL`/`RET`). See `cpu/CPU.md`
- [x] Instruction decoder — two-level, native `Decoder` (4→16 primary on
      opcode, 3→8 secondary on `funct`) gated by an AND per sub-instruction,
      inside `cpu/CPU.dig`. The hand-built `decoder_4to16bits`/`decoder_3to8`
      under `demux_decoder/` stay standalone practice blocks, unused here
- [x] State machine / control signals (fetch → decode → execute) — no
      separate state machine needed: decode is combinational off the
      instruction register, one instruction per clock (with a delay-slot
      fix-up on taken jumps). All signals (`WE`, `S`, `Sub`, `ALU_Op`,
      `MDU_op`, `Jump_EN`, stack/HI enables) generated in `cpu/CPU.dig`

## 4. Integration

- [x] Full datapath (PC → memory → registers → ALU → write-back) —
      `datapath/datapath.dig` (`register_file` → `ALU` → write-back mux, plus
      `RegA_Out`/`RegB_Out` taps) wired into `cpu/CPU.dig` together with the
      native `ROM`, the PC, the RAM, and the two-level decoder. Every control
      line is now generated, none are primary inputs
- [x] Execute the first instruction — fetch test, `0x1000`/`0x2000`/.../`0x4000`
- [x] Test program in memory — RAM and stack programs in `cpu/CPU.md` §15
- [x] CPU running a complete program — function-call test with `PUSH`/`CALL`/
      `RET` in `cpu/CPU.md` §15

## 5. Software

- [x] Assembler — `assembler/asm16.py`, two-pass with label support, all 16
      opcodes and the 6 `funct` sub-instructions; writes Digital's `v2.0 raw`
      hex format. Example programs under `assembler/examples/`

## 6. Beyond a working processor

Not needed for the CPU to be complete — capability and peripherals. See
`cpu/CPU.md` §19 for the reasoning behind the order.

- [ ] I/O — an output register to a display and an input register from
      switches; the next and most important step, since right now reading a
      result means inspecting wires in the simulator
- [ ] More memory — the 16-word RAM and 6-bit immediate cap real programs;
      needs the addressing scheme solved first
- [ ] Offset addressing (`LOAD rd, off(ra)`) — needs an address adder separate
      from the ALU's, which the instruction's own operation keeps busy
- [ ] `MTHI` — write access to the `HI` register (`MFHI` only reads it today)
- [ ] Stack overflow/collision protection — the stack grows over the data
      area with no warning
- [ ] Interrupts — today the only way out of `HLT` is `Reset`

## Technical debt / cleanup

- [x] Rename folders and files to English, no spaces or accents
- [x] Convert all notes from `.txt` to `.md`
- [x] Fix broken `.dig` cross-references (`full_adder.dig` / `half_adder.dig`)
- [x] Fix the XNOR truth table (it previously showed the XOR table)
- [ ] Reorganise into layers: `00_transistors/`, `01_gates/`, `02_combinational/`,
      `03_sequential/`, `04_control/`, `05_cpu/`
- [x] Fill in `mult_cell_4_bits.md` (was a stub) under `mdu/.../mult_cell_4_bits/`
- [ ] Resolve the cross-tree `mult_cell_1_bit.dig` → `full_adder.dig` dependency
