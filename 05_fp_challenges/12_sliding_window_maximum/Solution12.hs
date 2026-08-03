-- Sliding Window Maximum  (LeetCode 239)
-- ======================================
-- Given a window size k and a list, return the maximum of every contiguous
-- window of length k, left to right. Assume 1 <= k <= length nums.
--   maxSlidingWindow 3 [1,3,-1,-3,5,3,6,7] == [3,3,5,5,6,7]
--
-- Re-scanning each window is O(n*k): the two big tests (n = 100000,
-- k = 50000) will not finish. Aim for amortized O(n) -- still pure,
-- no mutation.

module Main where

import Data.List

maxSlidingWindow :: Int -> [Int] -> [Int]
maxSlidingWindow = undefined -- TODO

-- ---- tests ----
main :: IO ()
main = do
  check (maxSlidingWindow 3 [1,3,-1,-3,5,3,6,7]) [3,3,5,5,6,7]
  check (maxSlidingWindow 1 [1]) [1]
  check (maxSlidingWindow 2 [9,8,7,1]) [9,8,7]
  check (maxSlidingWindow 2 [1,2,3,4]) [2,3,4]
  check (maxSlidingWindow 3 [4,4,4]) [4]
  checkQuiet "ascending n=100000 k=50000" (maxSlidingWindow 50000 [1 .. 100000]) [50000 .. 100000]
  checkQuiet "descending n=100000 k=50000" (maxSlidingWindow 50000 [100000, 99999 .. 1]) [100000, 99999 .. 50000]
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
    checkQuiet name got want
      | got == want = putStrLn ("  PASS  " ++ name)
      | otherwise = error ("  FAIL  " ++ name)
