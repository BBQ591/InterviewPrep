// Merge Intervals  (LeetCode 56)
// ===============================
// Merge all overlapping intervals. Return them sorted by start.
//   merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
//   merge([[1,4],[4,5]]) == [[1,5]]

import java.util.*;

public class Solution09 {

    static int[][] merge(int[][] intervals) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(merge(new int[][]{{1,3},{2,6},{8,10},{15,18}}), new int[][]{{1,6},{8,10},{15,18}});
        check(merge(new int[][]{{1,4},{4,5}}),                new int[][]{{1,5}});
        check(merge(new int[][]{{1,4},{2,3}}),                new int[][]{{1,4}});
        check(merge(new int[][]{}),                           new int[][]{});
        System.out.println("all passed");
    }

    static void check(int[][] got, int[][] want) {
        if (!Arrays.deepEquals(got, want))
            throw new AssertionError("FAIL got " + Arrays.deepToString(got) + " want " + Arrays.deepToString(want));
        System.out.println("  PASS  " + Arrays.deepToString(got));
    }
}
