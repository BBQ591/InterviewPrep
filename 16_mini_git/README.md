# 16 — Mini Git — Specification

## System

A content-addressed version control system for one directory tree, stored
under `.minigit/` inside that directory. Single user, no network.

Three object kinds, each stored under a hash of its content:
- **blob** — the bytes of one file
- **tree** — one directory level: names mapping to blob/tree hashes
- **commit** — a tree hash, zero or one parent commit hash, a message, and a
  timestamp (the timestamp is *supplied as input*, never read from a clock)

Identical content must produce an identical hash and be stored exactly once.

## Input

Verbs (as a CLI or as library calls — your choice, decide and write it down):

- `init`
- `hash-object <file>` → prints the hash after storing the blob
- `cat-file <hash>` → prints the stored content (pretty-print trees)
- `write-tree` → snapshots the working directory, prints the tree hash
- `commit -m <msg> --time <t>` → prints the new commit hash
- `log` → commits from HEAD back to the root
- `checkout <hash>` → restores that commit's tree into the working directory
- `diff <hashA> <hashB>` → files added / removed / modified between commits

## Required behavior

1. **Round trip:** any stored object is retrievable by its hash, byte-identical.
2. **Immutability:** committing never modifies or deletes an existing object;
   re-storing identical content is a no-op (dedup by hash).
3. `log` always terminates (the parent chain never loops); `checkout` restores
   the snapshot exactly, including files that must disappear.
4. **Reproducibility:** identical directory contents + identical inputs
   (messages, timestamps) produce identical hashes and identical output,
   every run, byte for byte.

## Deliverables

1. The object store and all verbs above.
2. `diff` at file granularity (line-level diff is a P5 stretch).
3. Tests. Their design is part of the work — round-trip and dedup properties
   are natural candidates.

## Later phases (same spec, growing scope)

- P1: `init`, `hash-object`, `cat-file` — the blob store. Choose and write
  down the hash function and the on-disk format.
- P2: trees — `write-tree` snapshots nested directories; `cat-file` shows them.
- P3: commits, HEAD, `log`.
- P4: `checkout`, plus `branch <name>` (named refs to commits).
- P5: `diff`; three-way merge as a stretch goal.

## Notes

- Deliberately underspecified. What exactly goes into the bytes that get
  hashed? In what order do a tree's entries appear? What does HEAD point to —
  a hash, or a branch name? What happens to untracked files on checkout?
  Finding these questions, deciding them, and writing the decisions down is
  part of the work.
- Hashing: any deterministic content hash is fine (e.g. FNV-1a 64-bit,
  rendered as hex). Cryptographic strength is explicitly out of scope.
- Process gate (your protocol): skeleton — stubs, one-sentence contracts,
  call graph, edge list — reviewed before any bodies are written. The
  critical layering decision: Repository → ObjectStore → Blob/Tree/Commit —
  the same parent-delegates-to-layer shape you spotted in the skip list.
