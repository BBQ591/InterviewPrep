-- Merge Intervals  (LeetCode 56)
-- ===============================
-- Merge all overlapping intervals. Return them sorted by start.
--   merge [(1,3),(2,6),(8,10),(15,18)] == [(1,6),(8,10),(15,18)]
--   merge [(1,4),(4,5)] == [(1,5)]

module Main where

import Data.List (sortBy)
import Data.Ord (comparing)

merge :: [(Int, Int)] -> [(Int, Int)]
merge [] = []
merge intervals@(start : remaining) = reverse (last : merged)
  where
    (merged, last) = foldl (\(merged, prev) interval -> if fst interval <= snd prev then (merged, (fst prev, max (snd interval) (snd prev))) else (prev : merged, interval)) ([], start) (sortBy (comparing fst) intervals)

-- ---- tests ----
main :: IO ()
main = do
  check (merge [(1, 3), (2, 6), (8, 10), (15, 18)]) [(1, 6), (8, 10), (15, 18)]
  check (merge [(1, 4), (4, 5)]) [(1, 5)]
  check (merge [(1, 4), (2, 3)]) [(1, 4)]
  check (merge []) []
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
