-- Best Time to Buy and Sell Stock  (LeetCode 121)
-- ===============================================
-- prices[i] is the price on day i. Buy on one day, sell on a LATER day (one
-- transaction). Return the best possible profit, or 0 if no profitable trade
-- exists. Think per-day: what is the best profit if you sell TODAY? Then
-- aggregate over the days.
--   maxProfit [7,1,5,3,6,4] == 5   (buy at 1, sell at 6)
--   maxProfit [7,6,4,3,1] == 0

module Main where

import Data.List

maxProfit :: [Int] -> Int
maxProfit input = maximum (zipWith (\x y -> y - x) input suffixes)
  where
    suffixes = scanr1 (max) input

-- ---- tests ----
main :: IO ()
main = do
  check (maxProfit [7, 1, 5, 3, 6, 4]) 5
  check (maxProfit [7, 6, 4, 3, 1]) 0
  check (maxProfit [2, 10]) 8
  check (maxProfit [3, 8, 1, 2]) 5
  check (maxProfit [5]) 0
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
