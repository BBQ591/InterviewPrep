// Best Time to Buy and Sell Stock  (LeetCode 121)
// ===============================================
// prices[i] is the price on day i. Buy on one day, sell on a LATER day (one
// transaction). Return the best possible profit, or 0 if no profitable trade
// exists. Think per-day: what is the best profit if you sell TODAY? Then
// aggregate over the days.
//   maxProfit([7,1,5,3,6,4]) == 5   (buy at 1, sell at 6)
//   maxProfit([7,6,4,3,1]) == 0

public class Solution15 {

    static int maxProfit(int[] prices) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(maxProfit(new int[]{7,1,5,3,6,4}), 5);
        check(maxProfit(new int[]{7,6,4,3,1}), 0);
        check(maxProfit(new int[]{2,10}), 8);
        check(maxProfit(new int[]{3,8,1,2}), 5);
        check(maxProfit(new int[]{5}), 0);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want)
            throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
