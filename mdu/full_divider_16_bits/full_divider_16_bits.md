# 16-bit array divider

A purely combinational restoring array divider: `Dividend ÷ Divisor` for two
unsigned 16-bit values. It is the paper-and-pencil long-division algorithm
unrolled into silicon — one row per quotient bit, no clock, no state.

## Interface

- **Dividend** — 16-bit unsigned numerator.
- **Divisor** — 16-bit unsigned denominator.
- **Quotient** — 16-bit quotient.
- **Rest** — 16-bit remainder (`Dividend mod Divisor`).

Operands are unsigned; a signed interpretation is left to software.

## How it works

The array is **16 rows**, each a `div_cell_16_bits` block.

1. **Shift.** Row *i* builds its partial remainder by shifting the previous
   row's remainder up one bit and bringing in dividend bit `15 − i` at the
   bottom (a 15-bit `Ground` supplies the zeros for row 0).
2. **Trial subtract.** The row subtracts `Divisor` from that value.
3. **Restore decide.** If the subtraction is negative the row restores the
   pre-subtraction remainder; otherwise it keeps the subtracted value. Each row
   makes this decision itself from its borrow-out.
4. **Quotient bit.** The row's borrow-out is quotient bit `15 − i`: `1` when the
   divisor fitted.

After 16 rows the surviving partial remainder is `Rest`.

Division by zero is not special-cased: every trial subtraction succeeds, so the
quotient comes out all ones.

## Structure

```
full_divider_16_bits
└─ 16 × div_cell_16_bits
   └─ 2 × div_cell_8_bits
      └─ 2 × div_cell_4_bits
         └─ 4 × div_cell_1_bit
            ├─ full_adder
            └─ mux_2_1
```

This is a ripple array: worst-case delay grows with the borrow chain across a
row and the remainder chain down all 16 rows. It is the simplest correct
structure; faster schemes (carry-save, SRT) are a later optimisation.

## Note on dependencies

`div_cell_1_bit` pulls `full_adder.dig` from the `adder_subtractor/` tree and
`mux_2_1.dig` from the `multiplexer/` tree. Add both folders as custom component
search paths in Digital (Edit → Settings) before simulating, or keep local
copies.

## Known issue

The divider does not simulate cleanly yet. Digital orders a block's pins by the
vertical position of its `In` / `Out` symbols, not by creation order, and
several `div_cell_*` blocks have a pin placed at an odd height, so each cell is
wired to the wrong pins of the cell below it. The visible symptom is a "wire in
undefined state" inside `div_cell_8_bits`. Fix bottom-up with
*Edit → Order Inputs/Outputs*: `mux_2_1` → `div_cell_1_bit` → `div_cell_4_bits`
→ `div_cell_8_bits` → `div_cell_16_bits`. See `div_cell_1_bit.md` for detail.
