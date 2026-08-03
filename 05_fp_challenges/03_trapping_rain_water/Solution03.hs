-- Trapping Rain Water  (LeetCode 42)
-- ===================================
-- Given bar heights, compute how much water is trapped after raining.
--   trap [0,1,0,2,1,0,1,3,2,1,2,1] == 6
--   trap [4,2,0,3,2,5] == 9

module Main where

trap :: [Int] -> Int
trap heights = sum (zipWith (-) amount heights)
  where
    left_maxes = scanl1 max heights
    right_maxes = scanr1 max heights
    amount = zipWith min left_maxes right_maxes

-- ---- tests ----
main :: IO ()
main = do
  check (trap [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) 6
  check (trap [4, 2, 0, 3, 2, 5]) 9
  check (trap []) 0
  check (trap [5]) 0
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
