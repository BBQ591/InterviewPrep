// Group Anagrams  (LeetCode 49)
// ==============================
// Group strings that are anagrams of each other. Order doesn't matter (the test
// canonicalizes before comparing).
//   groupAnagrams(["eat","tea","tan","ate","nat","bat"])
//     == [["ate","eat","tea"],["bat"],["nat","tan"]]  (up to ordering)

import java.util.*;
import java.util.stream.*;

public class Solution08 {

    static List<List<String>> groupAnagrams(String[] words) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---- tests ----
    public static void main(String[] args) {
        check(groupAnagrams(new String[]{"eat","tea","tan","ate","nat","bat"}),
              List.of(List.of("ate","eat","tea"), List.of("bat"), List.of("nat","tan")));
        check(groupAnagrams(new String[]{""}),  List.of(List.of("")));
        check(groupAnagrams(new String[]{"a"}), List.of(List.of("a")));
        System.out.println("all passed");
    }

    // canonicalize: sort within each group, then sort the groups
    static List<List<String>> canon(List<List<String>> gs) {
        List<List<String>> out = new ArrayList<>();
        for (List<String> g : gs) { List<String> c = new ArrayList<>(g); Collections.sort(c); out.add(c); }
        out.sort(Comparator.comparing(Object::toString));
        return out;
    }

    static void check(List<List<String>> got, List<List<String>> want) {
        if (!canon(got).equals(canon(want)))
            throw new AssertionError("FAIL got " + canon(got) + " want " + canon(want));
        System.out.println("  PASS  " + canon(got));
    }
}
