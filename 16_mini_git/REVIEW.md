# 16 — Mini Git — Review (2026-08-03)

Read main.h / main.cpp / cli.cpp against the spec. Closing these out is
problem #1 of this week's five — do it before starting `diff`.

## What's solid

- Blob + tree round trip works end to end; the recursive write_tree/checkout
  shape is right.
- Root discovery by walking up to find `.git` is the real-git behavior.
- Format decisions were made and are consistent between writer and reader.

## Correctness vs spec (ordered by severity)

1. **Tree hashes are nondeterministic — spec req 4 violated.**
   `write_tree` hashes entries in `fs::directory_iterator` order, which is
   unspecified. The same directory can hash differently across runs/machines.
   Fix: collect entries, sort by name, then hash. *(Principle 6:
   nondeterminism entered silently — iteration order is an input you didn't
   choose.)*

2. **Commits have no parent chain and there is no HEAD — P3 isn't to spec.**
   `commit` appends a line to `commit.txt`; the Commit struct has no parent
   hash; `log` just reads the file backward. Spec: a commit is an object
   (tree hash, parent-hash-or-none, msg, timestamp) stored under ITS content
   hash; HEAD points at the tip; log walks HEAD → root. This also unlocks
   `branch` (P4) — a flat commit.txt can't represent two branches.

3. **checkout doesn't delete — spec req 3 violated.**
   Files present in the working tree but absent from the snapshot survive
   checkout. Works on a fresh dir, silently wrong on a dirty one.
   *(Category 5: the second operation.)* Decide the untracked-file contract
   while you're here — the spec's Notes already flag it.

4. **Snapshot root is the cwd, not the repo root.**
   `Git::commit` calls `write_tree(fs::current_path())` (main.cpp:65) — run
   from a subdirectory and you commit the subtree as if it were the whole
   repo. Same family: `hash_file` computes `root_path / path` (main.cpp:13),
   so from a subdir `minigit hash_object f.txt` resolves against the ROOT,
   not the cwd. It only works today because write_tree passes absolute paths
   and `/` with an absolute rhs discards the lhs. Decide the contract (git's
   answer: CLI args relative to cwd; snapshots always from root) and test
   both from a subdirectory.

5. **cat_object reads the object and prints nothing** (main.cpp:23–28).

6. **Formats are injectable — undecided contracts (category 6).**
   A filename containing a space or comma corrupts the tree parse; a commit
   message containing `"` corrupts the log parse. Decide: forbid + assert,
   escape, or length-prefix. Write the decision into the README.

7. **No tests.** Deliverable 3. Start with the two the spec names: round trip
   (store → cat, byte-identical) and dedup/reproducibility (same content
   twice → same hash, same object count). Then: checkout-deletes-files,
   subdir behavior, log walking a 3-commit chain.

## C++ punch list (this is a "classes in C++" rep — do it as one refactor pass)

- `using namespace std;` in main.h poisons every file that includes it — and
  the includes sit ABOVE the `#ifndef MAIN_H` guard. Guard first, no
  using-directives in headers, explicit `std::` there.
- `vector` is used in main.h without `#include <vector>` — compiles only via
  transitive includes. Include what you use.
- Everything takes `string` / `fs::path` by value — pass `const std::string&`
  / `const fs::path&` for read-only params.
- `metadata.root_path` is a string cast to `fs::path` at every use — store it
  as `fs::path` once.
- `pair<size_t, FileType>` from write_tree is principle 11 waiting to fire —
  name it: `struct TreeResult { size_t hash; FileType type; };`.
- `Git` is one God class. The spec's own layering note: Repository (verbs) →
  ObjectStore (store/load bytes by hash) → object types. ObjectStore is ~4
  functions you already wrote (store_file / read_file / hash) — extracting it
  makes the req-1/req-2 tests one-liners.
- Dead code: `words` in split (main.cpp:133); explicit `file.close()` before
  return is what the destructor is for (RAII).

## Suggested order

sort-entries fix (~15 min) → ObjectStore extraction → commit objects + HEAD +
log chain → checkout deletion → tests as you go → then P5 `diff`, which gets
easy once a tree loads into a `map<name, entry>`.
