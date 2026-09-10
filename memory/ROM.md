# ROM — 4-word read-only memory (demonstration)

A hand-built read-only memory with four 16-bit words, addressed by a 2-bit
address. It exists to show what a ROM *is* — an address selecting one of a set of
fixed stored words — before the CPU switches to Digital's native ROM for the real
instruction memory.

> Byte-for-byte copy of the Digital library file `ROM.dig`. It has no
> sub-circuit references (only Digital primitives), so nothing was edited.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Address` | 2 | which of the 4 words to read (0–3) |
| `Sel` | 1 | `0` = drive the addressed word; `1` = force `Data_Out` to 0 (output disable) |
| `Data_Out` | 16 | the selected word |

## How it works

- **The memory** is a 16-bit `Multiplexer` with 2 selector bits. Its four data
  inputs are hardwired `Const` words `0x0001`, `0x0002`, `0x0003`, `0x0004`
  (the first relies on Digital's `Const` default of 1). `Address` drives the
  select, so `Data_Out` is `word[Address]`. Purely combinational — no clock.
- **Output disable** — a second 16-bit 2:1 `Multiplexer` on the way out: input 0
  is the memory word, input 1 is `Ground` (0), select is `Sel`. `Sel = 1` forces
  `Data_Out` to 0 so the ROM can share a bus without a tri-state driver.

## Structure

```
ROM  (4-word demonstration)
├─ Multiplexer (16-bit, 2 select bits) + 4 × Const 0x1..0x4   Address → word
└─ Multiplexer (16-bit, 1 select bit) + Ground (0)            Sel → word / 0
```

All Digital primitives.

## Notes

- **Exception to from-scratch.** The CPU's real instruction memory uses Digital's
  native `ROM` component, not this block. A 16-bit address space is 65536 words —
  impractical to wire as constants by hand, and nothing new is learned past this
  4-word demo. Flagged like the ALU 16:1 mux and the PC's native adder.
  (author's note: *"já tinha feito uma ROM com 4 endereços; como para uma CPU de
  16 bits precisava de muitos endereços, apenas provei que sabia o que era uma
  ROM e usei a do Digital"*)
- A real ROM decodes the address to a one-hot line per word and ORs the selected
  word onto the output; the multiplexer here does the same job in one primitive.
- `Sel` is an output-enable, not a chip-select for addressing — the memory always
  drives *some* word internally.

## Status

Simulated in Digital and works: combinational lookup — `Data_Out` follows
`Address` with no clock and reads back the four words `0x0001`–`0x0004`;
`Sel = 1` zeroes the output.
