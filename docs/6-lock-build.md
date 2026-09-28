# 6. A chessboard lock (hobby build idea) **[open]**

A real chessboard that opens a lock when queens are placed on the right squares. Not built yet.

## Hardware

- 64 reed switches under the squares, and a magnet in the base of each queen.
- Eight daisy-chained 74HC165 shift registers read all 64 switches with 3 microcontroller pins.
- A microcontroller (for example an ESP32).
- A small servo, or a solenoid bolt switched by a MOSFET on its own power supply.
- An LED to show "open".

The whole board reads as one 64-bit number, so checking it is a single comparison.

## Modes

1. **Any valid solution opens it.** A puzzle box, not a lock. Validity can be checked with the XOR-and-count
   test from [part 1](1-flat-board.md).
2. **One secret solution.** Only 92 choices, so a patient person can try them all.
3. **Secret solution plus the order the queens are placed in.** 92 × 8! = 3,709,440 combinations, roughly a
   6 to 7 digit PIN. On a 10 x 10 board it is about 2.6 × 10⁹.

## Security notes

- The puzzle makes the code easier to remember. It does not make it stronger: an attacker only tries
  valid boards.
- Compare against a salted hash, answer only "open" or "closed", give no per-queen feedback, and take the
  same time for every answer.
