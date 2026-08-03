// Daily Temperatures  (LeetCode 739)
// ===================================
// For each day, how many days until a WARMER temperature? 0 if none.
//   dailyTemperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]
//   dailyTemperatures([30,40,50,60]) == [1,1,1,0]

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class Solution06 {

    static int[] dailyTemperatures(int[] temps) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(dailyTemperatures(new int[]{73,74,75,71,69,72,76,73}), new int[]{1,1,4,2,1,1,0,0});
        check(dailyTemperatures(new int[]{30,40,50,60}),             new int[]{1,1,1,0});
        check(dailyTemperatures(new int[]{30,60,90}),                new int[]{1,1,0});
        System.out.println("all passed");
    }

    static void check(int[] got, int[] want) {
        if (!Arrays.equals(got, want))
            throw new AssertionError("FAIL got " + Arrays.toString(got) + " want " + Arrays.toString(want));
        System.out.println("  PASS  " + Arrays.toString(got));
    }
}
