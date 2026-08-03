# Game Implementation Queue

Stateful-engine practice: model a world, evolve it with actions.
Every one of these has the same skeleton — design it yourself each time:

```
State                  # the board/world
Action                 # the move
is_valid(state, action)  # propose -> validate
apply(state, action)     # -> commit
is_terminal(state)       # won / lost / draw
```

**Workflow (the point of the exercise):**
1. Design the API first — types, then operations and their signatures. No bodies.
2. Write the adversarial tests *before* implementing. Ask: *what input breaks this?*
   (empty, single element, boundary, duplicate, reversed, full board)
3. Then fill in the bodies.

**Done:** `06_tetris`, `07_2048`, `08_snake`

---

## Grid, single-player

### Minesweeper *(medium)* — recommended next
W×H grid with M randomly placed mines. Every non-mine cell shows how many of its
8 neighbors are mines. Revealing a mine loses. Revealing a cell whose count is 0
also reveals all its neighbors, continuing outward for any newly revealed 0-cells.
Cells may be flagged/unflagged; flagged cells can't be revealed. Win when every
non-mine cell is revealed.

Note to self: you dont want something to represent a ton of states. try to minimize that
more states == more complicated. just make more lists

*Teaches: hidden model vs. derived view.*

### Match-3 (Bejeweled) *(medium)*
A grid of colored gems. The player swaps two orthogonally adjacent gems — but the
swap is only legal if it **creates a match**. A match is 3+ of the same color in a
row or column. Matched gems are removed; gems above fall to fill the gaps; new
random gems enter from the top. That may create new matches, which resolve the same
way, repeating until no matches remain. Score accumulates per clear.


### 15-Puzzle *(small)*
A 4×4 grid holds tiles 1–15 plus one blank. A move slides a tile orthogonally
adjacent to the blank into the blank (equivalently: the blank moves up/down/left/right).
Solved when tiles read 1…15 in order with the blank last.

### Sokoban *(medium)*
Push boxes onto goal squares in a walled maze. The player moves orthogonally; moving
into a box pushes it one cell in the same direction, but only if the cell beyond it is
empty (not a wall, not another box). Win when every box sits on a goal.


### Conway's Game of Life *(tiny)*
Grid of live/dead cells; all update simultaneously each tick. A live cell with 2 or 3
live neighbors (of 8) survives, else dies. A dead cell with exactly 3 live neighbors
becomes alive.


---

## Two-player boards

### Connect Four *(small)*
7 columns × 6 rows. Players alternate dropping a disc into a column; it falls to the
lowest empty row. Full columns are unplayable. First to line up four of their discs —
horizontally, vertically, or on either diagonal — wins. Board fills with no winner = draw.

### Othello / Reversi *(medium)*
8×8 board, black and white discs, starting with four in the center (two of each,
diagonally). A legal move places your disc on an empty cell such that in at least one
of the 8 directions, an unbroken line of opponent discs is bracketed between your new
disc and an existing disc of yours. Every bracketed opponent disc, in every such
direction, flips to your color. A player with no legal move passes; if neither can
move, the game ends. Most discs wins.

*Then add minimax — immutable state makes game-tree search trivial (you recurse on new
states and never have to undo).*

### Battleship *(medium)*
Each player secretly places ships of lengths 5, 4, 3, 3, 2 on a 10×10 grid,
horizontally or vertically, non-overlapping. Players alternate firing at a coordinate
on the opponent's grid; the result is hit or miss. A ship sinks when all its cells are
hit. First to sink all enemy ships wins.

---

## Cards & dice

### Yahtzee *(medium — pure rule decomposition)*
Roll 5 dice, up to 3 rolls per turn, keeping any dice between rolls. Then score the
dice into one of 13 categories, each usable once:

- **Ones … Sixes** — sum of the dice showing that number.
- **Three / Four of a Kind** — sum of *all* dice, if at least 3 (or 4) match.
- **Full House** — 25 pts, if three of one number and two of another.
- **Small Straight** — 30 pts, 4 consecutive values.
- **Large Straight** — 40 pts, 5 consecutive values.
- **Yahtzee** — 50 pts, all five equal.
- **Chance** — sum of all dice.
- Upper-section bonus: +35 if Ones–Sixes total ≥ 63.

*13 independent scoring rules — the best pure stub-then-implement drill on this list.*

### Blackjack *(small)*
Player and dealer each get two cards (one dealer card face-up). Number cards = face
value, faces = 10, Ace = 11 **or** 1 (whichever keeps the hand ≤ 21). Player repeatedly
hits or stands; over 21 = bust = loss. Then the dealer reveals and must keep hitting
until reaching 17+, then stands. Closest to 21 without busting wins; equal totals = push.
A two-card 21 ("blackjack") beats an ordinary 21.

*The Ace-as-1-or-11 rule is the decomposition puzzle.*

### Wordle *(small, one nasty rule)*
Secret 5-letter word, 6 guesses. Each guessed letter scores green (right letter, right
spot), yellow (in the word, wrong spot), or gray (not in the word).

**The trap:** duplicates. Yellow/green marks are capped by how many times the letter
actually occurs in the answer — if the answer has one E and your guess has two, only one
gets colored, and greens claim their letter first.

---

## The big one

### Klondike Solitaire *(large)*
52 cards. Seven tableau piles (pile *n* gets *n* cards; only the top card of each is
face-up), four foundation piles (one per suit, built Ace→King), a stock you draw from
into a waste pile.

Legal moves:
- move a face-up card — or a correctly ordered run of them — onto another tableau pile
  if it's one rank lower and the **opposite color**
- move a card to a foundation if it's the next rank up in that suit
- move a King (or a King-led run) onto an empty tableau pile
- draw from stock to waste (playing the top waste card)

Exposing a face-down tableau card flips it up. Win when all 52 cards are on the
foundations.

*Basically `try_move` × 6 — a pile of move-validation predicates.*

---

## Suggested order

1. **Minesweeper** — hidden model vs. derived view
2. **Connect Four** — win-detection in 4 directions
3. **Match-3** — the cascade loop
4. **Yahtzee** — pure rule decomposition
5. **Othello** (+ minimax) — immutable state powers search
6. **Solitaire** — when you want a grind

Also queued elsewhere in this repo: `01_regex_engine`, `02_lisp_interpreter`,
`03_spreadsheet`, `04_rope`.
