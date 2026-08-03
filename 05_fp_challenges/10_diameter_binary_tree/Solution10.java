// Diameter of Binary Tree  (LeetCode 543)
// ========================================
// The diameter is the number of EDGES on the longest path between any two nodes
// (the path may or may not pass through the root).
//        1
//       / \
//      2   3
//     / \
//    4   5     diameter = 3
//
//   diameter of the tree above == 3
//   diameter of a single node  == 0

public class Solution10 {

    static class Node {
        int val; Node left, right;
        Node(int v) { val = v; }
        Node(Node l, int v, Node r) { left = l; val = v; right = r; }
    }

    static int diameter(Node root) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        Node t1 = new Node(
            new Node(new Node(4), 2, new Node(5)),
            1,
            new Node(3));
        check(diameter(t1), 3);
        check(diameter(new Node(new Node(2), 1, null)), 1);
        check(diameter(null), 0);
        check(diameter(new Node(1)), 0);
        System.out.println("all passed");
    }

    static void check(int got, int want) {
        if (got != want) throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
