// Maximum Subarray  (LeetCode 53)
// ================================
// Return the largest sum of any contiguous non-empty subarray.
//   maxSubArray([-2,1,-3,4,-1,2,1,-5,4]) == 6   (subarray [4,-1,2,1])
//   maxSubArray([-1,-2,-3]) == -1

public class Solution02 {

    static int maxSubArray(int[] nums) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(maxSubArray(new int[]{-2,1,-3,4,-1,2,1,-5,4}), 6);
        check(maxSubArray(new int[]{1}),                     1);
        check(maxSubArray(new int[]{-1,-2,-3}),              -1);
        check(maxSubArray(new int[]{5,4,-1,7,8}),            23);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want) throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
