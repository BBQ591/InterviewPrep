// Product of Array Except Self  (LeetCode 238)
// =============================================
// Given nums, return out where out[i] = product of every element EXCEPT nums[i].
// No division. O(n).
//   productExceptSelf([1,2,3,4]) == [24,12,8,6]
//   productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0]

import java.util.Arrays;

public class Solution01 {

    static int[] productExceptSelf(int[] nums) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(productExceptSelf(new int[]{1,2,3,4}),     new int[]{24,12,8,6});
        check(productExceptSelf(new int[]{-1,1,0,-3,3}), new int[]{0,0,9,0,0});
        check(productExceptSelf(new int[]{2,3}),         new int[]{3,2});
        check(productExceptSelf(new int[]{5}),           new int[]{1});
        System.out.println("all passed");
    }

    static void check(int[] got, int[] want) {
        if (!Arrays.equals(got, want))
            throw new AssertionError("FAIL got " + Arrays.toString(got) + " want " + Arrays.toString(want));
        System.out.println("  PASS  " + Arrays.toString(got));
    }
}
