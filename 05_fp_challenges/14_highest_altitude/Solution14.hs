-- Find the Highest Altitude  (LeetCode 1732)
-- ==========================================
-- A biker starts at altitude 0. gain[i] is the net change in altitude between
-- points i and i+1. Compute the altitude at EVERY point, then return the
-- highest one visited.
--   highestAltitude [-5,1,5,0,-7] == 1        (altitudes 0,-5,-4,1,1,-6)
--   highestAltitude [-4,-3,-2,-1,4,3,2] == 0  (never above the start)

module Main where

import Data.List

highestAltitude :: [Int] -> Int
highestAltitude nums = maximum (scanl (+) 0 nums)

-- ---- tests ----
main :: IO ()
main = do
  check (highestAltitude [-5, 1, 5, 0, -7]) 1
  check (highestAltitude [-4, -3, -2, -1, 4, 3, 2]) 0
  check (highestAltitude [2, 2, 2]) 6
  check (highestAltitude []) 0
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
