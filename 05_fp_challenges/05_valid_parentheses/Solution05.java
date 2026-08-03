// Valid Parentheses  (LeetCode 20)
// =================================
// Given a string of just ()[]{}, return true iff every bracket is closed by the
// matching type in the correct order.
//   isValid("()[]{}") == true
//   isValid("([)]") == false
//   isValid("{[]}") == true

import java.util.ArrayDeque;
import java.util.Deque;

public class Solution05 {

    static boolean isValid(String s) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(isValid("()"),     true);
        check(isValid("()[]{}"), true);
        check(isValid("(]"),     false);
        check(isValid("([)]"),   false);
        check(isValid("{[]}"),   true);
        check(isValid("("),      false);
        check(isValid(""),       true);
        System.out.println("all passed");
    }

    static void check(boolean got, boolean want) {
        if (got != want) throw new AssertionError("FAIL got " + got + " want " + want);
        System.out.println("  PASS  " + got);
    }
}
