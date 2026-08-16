# 31 — In-Memory File System — Specification (M, interview sim)

Protocol: parts in order; don't read Part N+1 until Part N is green.
Python + pytest (or C++ if you want the rep).

## Part 1 — the tree

`mkdir(path)` ; `write(path, content)` — creates or overwrites a file;
`read(path) -> content` ; `ls(path) -> list[str]` — for a directory, its
entries sorted by name; for a file, just its name.
Paths are absolute, `/`-separated.

## Part 2 — usage and quotas

`du(path) -> int` — total size in bytes of the file, or of everything
under the directory.
`set_quota(dir_path, max_bytes)` — a write that would push any
directory with a quota above its limit fails, and a failed write
changes nothing.

## Part 3 — move

`mv(src, dst)` — files or whole directory subtrees. The operation is
atomic: it either fully succeeds or changes nothing, including when the
destination's quotas could not absorb the moved content.

## Part 4 (stretch) — hard links

`link(existing_file_path, new_path)` — two paths, one file: writes
through either path are visible through both. Decide and document what
`du` and quotas mean once a file has two homes, and what `mv` and
deletion do to a linked file.

## Deliverables

Implementation + tests. Test design is part of the work.
Deliberately underspecified in places — finding the ambiguities and
deciding those contracts is part of the work.
