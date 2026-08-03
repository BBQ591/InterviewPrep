// Trapping Rain Water  (LeetCode 42)
// ===================================
// Given bar heights, compute how much water is trapped after raining.
//   trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
//   trap([4,2,0,3,2,5]) == 9

public class Solution03 {

    static int trap(int[] heights) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(trap(new int[]{0,1,0,2,1,0,1,3,2,1,2,1}), 6);
        check(trap(new int[]{4,2,0,3,2,5}),             9);
        check(trap(new int[]{}),                        0);
        check(trap(new int[]{5}),                       0);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want) throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
