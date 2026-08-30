# Transistors

To start, we need to understand the two types of transistor that feed into the
universal logic gates.

## Doped silicon

It all starts with silicon. A silicon atom has 4 valence electrons, and to reach
the noble-gas configuration closest to it, it needs 4 more. It shares them with
neighbouring silicon atoms in a chain, so every atom ends up with 8 shared
electrons, forming a crystal in which the electrons are locked in place by those
bonds.

Electric current depends on the movement of electrons; if they do not move, no
current flows, so pure silicon is not a conductor. However, if we take out a
silicon atom and replace it with a phosphorus atom, which has 5 valence
electrons, 4 of them form bonds and 1 is left free. Because that electron can
move, silicon doped with phosphorus conducts. This is called **N-type silicon** —
N for negative, because electrons carry negative charge. The material is
electrically neutral; the name only reflects the free electron.

If instead of phosphorus we add boron, which has only 3 valence electrons, it
uses all 3 to satisfy the four-bond condition but is still short one, creating a
**hole**. That hole can be filled by a neighbouring electron, which in turn
creates a new hole, so this doped crystal also conducts — the charge moves
through the holes. This is called **P-type silicon**, because the holes move and
behave like positive charges — P for positive.

## The P–N junction

When we place a P-type piece against an N-type piece, since the P side has holes
and the N side has loose electrons, at the boundary the electrons from the N
piece see the holes and jump across. That jump only happens once, when the
pieces are joined. The boundary is then left with neither free electrons nor
holes and does not conduct. This region is called the **depletion zone** — two
conductors separated by an insulating wall.

## The two universal transistors

**N-type FET** — its structure is `N | P | N`. A current trying to pass through
would have to cross two insulating boundaries, so it does not. We say the switch
is **cut off**, and that is the transistor's resting state. Above the P layer
there is a very thin layer of insulating oxide, and above that a metal plate
called the **gate**. When we apply a 1 (e.g. 5 V) to the gate, the plate becomes
positively charged, and positive charge attracts electrons and repels the holes
in the P layer, the source and the drain. Those electrons stick to the oxide
layer, creating an N path for electrons to flow along, bypassing the P layer. So
the path that was `N | P | N` becomes `N | N | N`: there are no more boundaries,
just one continuous, conductive path from source to drain. With a 0 on the gate
the switch is cut off and nothing passes; with a 1 on the gate it conducts.

**P-type FET** — its structure is `P | N | P`, and it works as the inverse of the
N-type FET. For the N region to behave like P, it needs to accumulate holes
under the insulating oxide, and those holes come from the P layers at the ends
(source and drain). They move to the middle when a 0 is applied to the gate,
i.e. when it is connected to GND. Since holes carry positive charge, applying a
negative charge to the gate attracts them, creating a new path for the holes on
top of the N layer, which then behaves like `P | P | P`. So with a 1 on the gate
the switch is cut off and nothing passes; with a 0 on the gate it conducts.

## Ideal switch vs. real silicon

In the program used to build this CPU, these transistors act as ideal switches:
when they conduct, they connect both sides with no losses. In silicon it is not
like that. In real life the **channel** — the electrons/holes pulled under the
oxide when the gate is active — only exists while the potential difference
between the gate and the channel is greater than the **threshold voltage** (the
minimum potential difference for the channel to form). That is, the channel
exists while `V_gate − V_channel > V_threshold`. If the channel voltage rises,
that difference shrinks, and if it drops below the threshold the channel
collapses. Since the channel is tied to the output, its voltage equals the
output voltage, so if the output voltage rises the channel can collapse. The
output rises because the transistor is there to carry a value from one side to
the other.

In an N-type FET, if the source is at 5 V, the output at 0, and the gate is
active, current flows and the output voltage rises until it reaches about
4.3 V; at that point, with a 0.7 V difference, the channel collapses and the
transistor switches itself off without passing the full 5 V. When passing a 0,
the source is at 0, so the output also settles at 0 V, which does not hurt the
channel. That is why the N-type FET is used to pass a 0 and not a 1 — it is meant
to carry 0 V from source to output. The opposite happens with the P-type FET: it
is used to pass a 1 and not a 0. With this in mind, the circuits here are built
the way they are actually done in real hardware.
