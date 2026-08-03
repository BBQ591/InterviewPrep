-- Diameter of Binary Tree  (LeetCode 543)
-- ========================================
-- The diameter is the number of EDGES on the longest path between any two nodes
-- (the path may or may not pass through the root).
--        1
--       / \
--      2   3
--     / \
--    4   5      diameter = 3  (path 4-2-5 ... actually 4-2-1-3, length 3)
--
--   diameter (Node (Node (Node Leaf 4 Leaf) 2 (Node Leaf 5 Leaf)) 1 (Node Leaf 3 Leaf)) == 3
--   diameter (Node (Node Leaf 2 Leaf) 1 Leaf) == 1
--   diameter Leaf == 0

module Main where

data Tree = Leaf | Node Tree Int Tree

-- compute_deepest :: Tree -> Int
-- compute_deepest Leaf = -1
-- compute_deepest (Node left value right) = 1 + max (compute_deepest left) (compute_deepest right)
--
-- diameter :: Tree -> Int
-- diameter Leaf = 0
-- diameter (Node left value right) = max best_diameter curr_best
--  where
--    best_diameter = max (diameter left) (diameter right)
--    left_depth = 1 + compute_deepest left
--    right_depth = 1 + compute_deepest right
--    curr_best = left_depth + right_depth

compute_ans :: Tree -> (Int, Int)
compute_ans Leaf = (-1, 0)
compute_ans (Node left val right) = (deepest, best_ans)
  where
    (left_deepest, left_diameter) = compute_ans left
    (right_deepest, right_diameter) = compute_ans right
    deepest = 1 + max left_deepest right_deepest
    best_ans = max (left_deepest + right_deepest + 2) (max left_diameter right_diameter)

diameter :: Tree -> Int
diameter root = snd (compute_ans root)

-- ---- tests ----
main :: IO ()
main = do
  let t1 = Node (Node (Node Leaf 4 Leaf) 2 (Node Leaf 5 Leaf)) 1 (Node Leaf 3 Leaf)
  check (diameter t1) 3
  check (diameter (Node (Node Leaf 2 Leaf) 1 Leaf)) 1
  check (diameter Leaf) 0
  check (diameter (Node Leaf 1 Leaf)) 0
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
