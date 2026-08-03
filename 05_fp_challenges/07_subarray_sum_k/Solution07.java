// Subarray Sum Equals K  (LeetCode 560)
// ======================================
// Count the number of contiguous subarrays whose elements sum to exactly k.
//   subarraySum([1,1,1], 2) == 2
//   subarraySum([1,2,3], 3) == 2
//   subarraySum([1,-1,0], 0) == 3

import java.util.HashMap;
import java.util.Map;

public class Solution07 {

    static int subarraySum(int[] nums, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(subarraySum(new int[]{1,1,1}, 2),   2);
        check(subarraySum(new int[]{1,2,3}, 3),   2);
        check(subarraySum(new int[]{1,-1,0}, 0),  3);
        check(subarraySum(new int[]{3,4,7,2,-3,1,4,2}, 7), 4);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want) throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
