# register_16bits_reset — 16-bit register with load enable and synchronous reset

The `register_16bits` word with one extra input: a `Reset` line that clears the
stored value to zero. This is the **"with reset" variant** — the project keeps
two versions of the register (plain `register_16bits` and this one) and the
choice of which to use where is made later (see ROADMAP §2). The program counter
uses this variant so it has a defined start address of 0.

> Byte-for-byte copy of the Digital library file `Registo16bits_reset.dig`.
> Renamed to `register_16bits_reset`; the only edit is the `<elementName>`
> reference to its child, now `register_16bits.dig`. `program_counter.dig`
> references this file as `register_16bits_reset.dig`.

## Interface

| Pin | Width | Meaning |
|---|---|---|
| `Data_In` | 16 | value to load |
| `Clk` | 1 | clock |
| `EN` | 1 | `1` = load on the next edge; `0` = hold |
| `Reset` | 1 | `1` = load `0` instead of `Data_In` on the next edge |
| `Q` | 16 | stored word |

## How it works

- Inside is one plain `register_16bits` (4 × `register_4bits`, load-enable mux
  per slice). `Clk`, `EN` and `Q` pass straight through to it.
- A 16-bit 2:1 `Multiplexer` sits in front of the register's `D` input. Its two
  data sides are `Data_In` and a 16-bit `Ground` (constant `0`); the select is
  `Reset`.
- `Reset = 0` → `Data_In` reaches the register, normal load-enable behaviour.
- `Reset = 1` → `0` reaches the register; the next clock edge (with `EN = 1`)
  stores zero.
- The reset is therefore **synchronous and enable-gated**: it needs a clock edge
  and `EN = 1`. It does not asynchronously force `Q` to 0.

## Structure

```
register_16bits_reset
├─ register_16bits              16-bit register with load enable
│  └─ 4 × register_4bits → flip_flop_d → d_latch → latch_sr
└─ Multiplexer (16-bit, 1 select bit) + Ground (16-bit constant 0)
```

`Multiplexer` and `Ground` are Digital primitives.

## Notes

- The reset is a data-vs-zero mux rather than one AND gate per bit — same effect,
  fewer parts, and it reuses the native `Multiplexer` already used in the ALU
  result mux.
- To make `Reset` override a stall (`EN = 0`), OR `Reset` into the enable line;
  as wired, a reset only lands when the register is also enabled.
- The inner `register_16bits` is **not** copied into this folder — it lives at
  `registers/register_file/register_16bits/`. Add that folder and the ones below
  it as custom component search paths when opening this block from the repo.
- Pin order follows the vertical position of the `In` / `Out` symbols;
  `program_counter` is wired to match.

## Status

Saved from Digital. Verify in simulation: `Reset = 1`, `EN = 1` clears `Q` to 0
on the edge; `Reset = 0` behaves exactly like `register_16bits`.
