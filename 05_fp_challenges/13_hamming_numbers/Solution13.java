// Hamming Numbers / Ugly Number II  (LeetCode 264)
// ================================================
// A Hamming number is a positive integer with no prime factors other than
// 2, 3 and 5. The sequence starts 1,2,3,4,5,6,8,9,10,12,15,16,...
// nthHamming(n) returns the n-th (1-indexed) Hamming number.
//   nthHamming(10) == 12
//
// Testing integers one at a time for smoothness is far too slow for the
// last test -- the sequence has to be generated directly.

public class Solution13 {

    static int nthHamming(int n) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(nthHamming(1), 1);
        check(nthHamming(10), 12);
        check(nthHamming(11), 15);
        check(nthHamming(12), 16);
        check(nthHamming(1500), 859963392);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want)
            throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
