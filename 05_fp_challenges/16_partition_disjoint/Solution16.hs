-- Partition Array into Disjoint Intervals  (LeetCode 915)
-- =======================================================
-- Split nums into non-empty left ++ right so that every element of left is
-- <= every element of right. Return the length of the SMALLEST such left.
-- A valid split is guaranteed to exist.
--   partitionDisjoint [5,0,3,8,6] == 3     (left [5,0,3], right [8,6])
--   partitionDisjoint [1,1,1,0,6,12] == 4  (left [1,1,1,0])

module Main where

import Data.List

partitionDisjoint :: [Int] -> Int
partitionDisjoint input = length (takeWhile (> 0) (zipWith (-) max_left min_right)) + 1
  where
    max_left = init (scanl1 (max) input)
    min_right = tail (scanr1 (min) input)

-- ---- tests ----
main :: IO ()
main = do
  check (partitionDisjoint [5, 0, 3, 8, 6]) 3
  check (partitionDisjoint [1, 1, 1, 0, 6, 12]) 4
  check (partitionDisjoint [1, 2]) 1
  check (partitionDisjoint [2, 1, 3]) 2
  check (partitionDisjoint [1, 1]) 1
  check (partitionDisjoint [3, 3, 3]) 1
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
