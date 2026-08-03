// Find the Highest Altitude  (LeetCode 1732)
// ==========================================
// A biker starts at altitude 0. gain[i] is the net change in altitude between
// points i and i+1. Compute the altitude at EVERY point, then return the
// highest one visited.
//   highestAltitude([-5,1,5,0,-7]) == 1        (altitudes 0,-5,-4,1,1,-6)
//   highestAltitude([-4,-3,-2,-1,4,3,2]) == 0  (never above the start)

public class Solution14 {

    static int highestAltitude(int[] gain) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(highestAltitude(new int[]{-5,1,5,0,-7}), 1);
        check(highestAltitude(new int[]{-4,-3,-2,-1,4,3,2}), 0);
        check(highestAltitude(new int[]{2,2,2}), 6);
        check(highestAltitude(new int[]{}), 0);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want)
            throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
