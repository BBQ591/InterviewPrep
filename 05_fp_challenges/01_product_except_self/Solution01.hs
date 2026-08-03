-- Product of Array Except Self  (LeetCode 238)
-- =============================================
-- Given `nums`, return `out` where out[i] = product of every element EXCEPT nums[i].
-- No division. O(n).
--   productExceptSelf [1,2,3,4] == [24,12,8,6]
--   productExceptSelf [-1,1,0,-3,3] == [0,0,9,0,0]

module Main where

import Data.ByteString (isSuffixOf)

iteration :: [Int] -> [Int] -> [Int]
iteration _ [] = []
iteration (p : pref) (s : suf) = (p * s) : iteration pref suf

productExceptSelf :: [Int] -> [Int]
productExceptSelf nums = iteration pref (tail suf)
  where
    pref = scanl (*) 1 nums
    suf = reverse (scanl (*) 1 (reverse nums))

-- ---- tests ----
main :: IO ()
main = do
  check (productExceptSelf [1, 2, 3, 4]) [24, 12, 8, 6]
  check (productExceptSelf [-1, 1, 0, -3, 3]) [0, 0, 9, 0, 0]
  check (productExceptSelf [2, 3]) [3, 2]
  check (productExceptSelf [5]) [1]
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
