// Sliding Window Maximum  (LeetCode 239)
// ======================================
// Given a list and a window size k, return the maximum of every contiguous
// window of length k, left to right. Assume 1 <= k <= nums.length.
//   maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]
//
// Re-scanning each window is O(n*k): the two big tests (n = 100000,
// k = 50000) will not finish. Aim for amortized O(n).

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class Solution12 {

    static int[] maxSlidingWindow(int[] nums, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(maxSlidingWindow(new int[]{1,3,-1,-3,5,3,6,7}, 3), new int[]{3,3,5,5,6,7});
        check(maxSlidingWindow(new int[]{1}, 1),                 new int[]{1});
        check(maxSlidingWindow(new int[]{9,8,7,1}, 2),           new int[]{9,8,7});
        check(maxSlidingWindow(new int[]{1,2,3,4}, 2),           new int[]{2,3,4});
        check(maxSlidingWindow(new int[]{4,4,4}, 3),             new int[]{4});

        int n = 100000, k = 50000;
        int[] asc = new int[n], desc = new int[n];
        for (int i = 0; i < n; i++) { asc[i] = i + 1; desc[i] = n - i; }
        int[] ascWant = new int[n - k + 1], descWant = new int[n - k + 1];
        for (int i = 0; i <= n - k; i++) { ascWant[i] = i + k; descWant[i] = n - i; }
        checkQuiet("ascending n=100000 k=50000", maxSlidingWindow(asc, k), ascWant);
        checkQuiet("descending n=100000 k=50000", maxSlidingWindow(desc, k), descWant);
        System.out.println("all passed");
    }

    static void check(int[] got, int[] want) {
        if (!Arrays.equals(got, want))
            throw new AssertionError("FAIL got " + Arrays.toString(got) + " want " + Arrays.toString(want));
        System.out.println("  PASS  " + Arrays.toString(got));
    }

    static void checkQuiet(String name, int[] got, int[] want) {
        if (!Arrays.equals(got, want))
            throw new AssertionError("FAIL " + name);
        System.out.println("  PASS  " + name);
    }
}
