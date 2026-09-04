# 16-bit array divider

A purely combinational restoring array divider: `Dividend ÷ Divisor` for two
unsigned 16-bit values. It is the paper-and-pencil long-division algorithm
unrolled into silicon — one row per quotient bit, no clock, no state.

## Interface

- **Dividend** — 16-bit unsigned numerator.
- **Divisor** — 16-bit unsigned denominator.
- **Quotient** — 16-bit quotient.
- **Rest** — 16-bit remainder (`Dividend mod Divisor`).
- **FDZ** — divide-by-zero flag: set when `Divisor = 0` (a 16-input NOR of the
  divisor bits). The array itself is not special-cased, so on `Divisor = 0` the
  quotient still comes out all ones; `FDZ` is what software checks.
- **FRZ** — remainder-zero flag: set when `Rest = 0`, i.e. the division was
  exact (a 16-input NOR of the remainder bits).
- **FN** — negative flag: top bit of the result, provided for a signed
  interpretation of the quotient.

Operands are unsigned; a signed interpretation is left to software. The three
flags are derived combinationally and add no delay to `Quotient` / `Rest`.

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

After 16 rows the surviving partial remainder is `Rest` and the 16 collected
borrow-outs are `Quotient`. `FDZ`, `FRZ` and `FN` are then derived
combinationally from `Divisor`, `Rest` and the result's top bit.

Division by zero is not special-cased inside the array: every trial subtraction
succeeds, so the quotient comes out all ones — `FDZ` is the flag that reports it.

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

