# 18 — Vec&lt;T&gt; — Specification

std::vector from scratch. The point is the memory story: raw storage +
placement new + explicit destructor calls. `new T[cap]` is disqualified — it
default-constructs every slot, and Vec must work for a T with no default
constructor.

## Interface

```cpp
template <typename T>
class Vec {
  // size, capacity, empty, reserve(n)
  // push_back(const T&), push_back(T&&)
  // emplace_back(Args&&... args)
  // pop_back, operator[], front, back, clear
  // begin/end — T* is a legitimate iterator; range-for must work
  // destructor, copy ctor, copy assign, move ctor, move assign  (rule of five)
};
```

## Constructors (slot into the phases as noted)

- `Vec()` — empty (P1).
- `Vec(size_t n, const T& value)` — n copies of value (P2 — same
  placement-new loop as the copy ctor; they reinforce each other).
- `Vec(size_t n)` — n default-constructed elements (P2). The ONE member
  that requires default-constructible T — and Vec<no-default-ctor-T> still
  works if nobody calls it, because template members instantiate lazily.
  Same mechanism as the move-only note below.
- `Vec(std::initializer_list<T>)` (P4) — and the interview gotcha it
  creates: `Vec<int> v{5, 42}` is TWO elements; `Vec<int> v(5, 42)` is
  five 42s. Braces prefer the initializer_list overload. Test both.
- P5 option: `template <class It> Vec(It first, It last)` — unconstrained,
  it HIJACKS `Vec<int>(5, 42)` (It=int is an exact match; the fill ctor
  needs int→size_t). Reproduce the compile error, then fix it with a
  C++20 constraint (`requires std::input_iterator<It>`). The best 20 lines
  of template-overload practice on this list.

## Required behavior

1. **Leak-freedom, proven.** Test with an instrumented Canary type that
   counts live instances (ctor/copy/move ++, dtor --). After every test
   block: live == 0. During: live == vec.size(). ASan is the other half of
   the harness — build every test run with
   `-std=c++17 -g -fsanitize=address,undefined`. For this problem the
   sanitizer IS the test suite; asserts can't see a double-destroy.
   KNOWN ISSUE on this machine (found 2026-08-04): ASan binaries hang at
   100% CPU in dyld initializers before main — toolchain/OS bug, not your
   code. Fallback that works: Guard Malloc —
   `DYLD_INSERT_LIBRARIES=/usr/lib/libgmalloc.dylib ./test_vec`
   (or the same env var inside lldb to get the crashing line). It puts each
   allocation against a protected page, so heap overruns become instant
   crashes.
2. Must instantiate and pass with: `int`, `std::string`, and
   `std::unique_ptr<int>` (move-only — a stray copy anywhere in the
   push_back/grow path becomes a compile error; that error is the lesson).
3. Growth doubles (0 → 1 → 2 → 4 ...); reserve never shrinks; growth
   invalidates pointers and iterators — document it, then write the test
   that would have caught YOU holding one across a push_back.
4. Oracle: seeded random op sequence (push/pop/clear/copy/move) applied to
   Vec<int> and std::vector<int> in lockstep; contents equal after every op.

## Phases

- P1: int-only DynArray, no templates — get the
  allocate / placement-new / destroy-loop / free story right in the simple
  world first.
- P2: templatize; rule of three. Copy ctor copies only [0, size), never
  capacity.
- P3: rule of five. Move ctor/assign leave the source empty-but-valid.
  `unique_ptr<int>` instantiates from here on.
- P4: emplace_back — variadic template + std::forward (this is the
  function-template rep); begin/end + range-for.
- P5 (stretch, pick one): `SmallVec<T, N>` — non-type template parameter,
  inline storage for the first N elements, spill to heap after (the
  interview flex); or the strong exception guarantee on grow via
  `std::move_if_noexcept`.

## Where the bugs live

- mirrors (category 2): copy ctor and move ctor are twins — the move that
  forgets to null the source's pointer double-frees in BOTH destructors.
  Test the second twin first. Self-assignment (`v = v`) is the classic
  second-operation bug.
- boundaries: pop_back on empty; growth from capacity 0; the operator[]
  contract — decide (UB like std, or assert) and write it down.
- order of teardown: destroy elements [0, size) THEN release raw storage —
  in the dtor, in assign, in grow. Three places, one fact (category 4).
