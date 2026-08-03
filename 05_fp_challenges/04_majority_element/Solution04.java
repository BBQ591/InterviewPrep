// Majority Element  (LeetCode 169)
// =================================
// Return the element that appears MORE than n/2 times (guaranteed to exist).
// Aim for O(1) extra space (Boyer-Moore), not a frequency map.
//   majority([3,2,3]) == 3
//   majority([2,2,1,1,1,2,2]) == 2

public class Solution04 {

    static int majority(int[] nums) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(majority(new int[]{3,2,3}),         3);
        check(majority(new int[]{2,2,1,1,1,2,2}), 2);
        check(majority(new int[]{1}),             1);
        check(majority(new int[]{6,6,6,7,7}),     6);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want) throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
