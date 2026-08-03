// Partition Array into Disjoint Intervals  (LeetCode 915)
// =======================================================
// Split nums into non-empty left ++ right so that every element of left is
// <= every element of right. Return the length of the SMALLEST such left.
// A valid split is guaranteed to exist.
//   partitionDisjoint([5,0,3,8,6]) == 3     (left [5,0,3], right [8,6])
//   partitionDisjoint([1,1,1,0,6,12]) == 4  (left [1,1,1,0])

public class Solution16 {

    static int partitionDisjoint(int[] nums) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(partitionDisjoint(new int[]{5,0,3,8,6}), 3);
        check(partitionDisjoint(new int[]{1,1,1,0,6,12}), 4);
        check(partitionDisjoint(new int[]{1,2}), 1);
        check(partitionDisjoint(new int[]{2,1,3}), 2);
        check(partitionDisjoint(new int[]{1,1}), 1);
        check(partitionDisjoint(new int[]{3,3,3}), 1);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want)
            throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
