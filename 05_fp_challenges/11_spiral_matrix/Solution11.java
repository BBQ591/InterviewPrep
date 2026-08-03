// Spiral Matrix  (LeetCode 54)
// ============================
// Return all elements of the matrix in clockwise spiral order, starting at the
// top-left corner. The matrix is rectangular, not necessarily square.
//   spiralOrder([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]
//   spiralOrder([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) == [1,2,3,4,8,12,11,10,9,5,6,7]

import java.util.Arrays;

public class Solution11 {

    static int[] spiralOrder(int[][] matrix) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(spiralOrder(new int[][]{{1,2,3},{4,5,6},{7,8,9}}),          new int[]{1,2,3,6,9,8,7,4,5});
        check(spiralOrder(new int[][]{{1,2,3,4},{5,6,7,8},{9,10,11,12}}), new int[]{1,2,3,4,8,12,11,10,9,5,6,7});
        check(spiralOrder(new int[][]{{7}}),                              new int[]{7});
        check(spiralOrder(new int[][]{{1},{2},{3}}),                      new int[]{1,2,3});
        check(spiralOrder(new int[][]{{1,2}}),                            new int[]{1,2});
        check(spiralOrder(new int[][]{}),                                 new int[]{});
        System.out.println("all passed");
    }

    static void check(int[] got, int[] want) {
        if (!Arrays.equals(got, want))
            throw new AssertionError("FAIL got " + Arrays.toString(got) + " want " + Arrays.toString(want));
        System.out.println("  PASS  " + Arrays.toString(got));
    }
}
