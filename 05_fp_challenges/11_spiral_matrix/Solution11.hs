-- Spiral Matrix  (LeetCode 54)
-- ============================
-- Return all elements of the matrix in clockwise spiral order, starting at the
-- top-left corner. The matrix is rectangular, not necessarily square.
--   spiralOrder [[1,2,3],[4,5,6],[7,8,9]] == [1,2,3,6,9,8,7,4,5]
--   spiralOrder [[1,2,3,4],[5,6,7,8],[9,10,11,12]] == [1,2,3,4,8,12,11,10,9,5,6,7]

module Main where

import Data.List

_spiralOrder :: [[Int]] -> [[Int]]
_spiralOrder [] = [[]]
_spiralOrder (start : end) = start : _spiralOrder (rotate_matrix end)
  where
    rotate_matrix matrix = reverse (transpose matrix)

spiralOrder :: [[Int]] -> [Int]
spiralOrder [] = []
spiralOrder matrix@(start : end) = concat (_spiralOrder matrix)

-- ---- tests ----
main :: IO ()
main = do
  check (spiralOrder [[1, 2, 3], [4, 5, 6], [7, 8, 9]]) [1, 2, 3, 6, 9, 8, 7, 4, 5]
  check (spiralOrder [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
  check (spiralOrder [[7]]) [7]
  check (spiralOrder [[1], [2], [3]]) [1, 2, 3]
  check (spiralOrder [[1, 2]]) [1, 2]
  check (spiralOrder []) []
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
