-- Maximum Subarray  (LeetCode 53)
-- ================================
-- Return the largest sum of any contiguous non-empty subarray.
--   maxSubArray [-2,1,-3,4,-1,2,1,-5,4] == 6   (subarray [4,-1,2,1])
--   maxSubArray [1] == 1
--   maxSubArray [-1,-2,-3] == -1

module Main where

maxSubArray :: [Int] -> Int
maxSubArray nums = sum nums - minimum (zipWith (+) min_suffix prefix_sum)
  where
    prefix_sum = scanl (+) 0 nums
    suffixes = scanl (+) 0 (reverse nums)
    min_suffix = tail (reverse (scanl1 (min) suffixes))

-- ---- tests ----
main :: IO ()
main = do
  check (maxSubArray [-2, 1, -3, 4, -1, 2, 1, -5, 4]) 6
  check (maxSubArray [1]) 1
  check (maxSubArray [-1, -2, -3]) (-1)
  check (maxSubArray [5, 4, -1, 7, 8]) 23
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
