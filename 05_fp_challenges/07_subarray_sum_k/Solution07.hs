-- Subarray Sum Equals K  (LeetCode 560)
-- ======================================
-- Count the number of contiguous subarrays whose elements sum to exactly k.
--   subarraySum [1,1,1] 2 == 2
--   subarraySum [1,2,3] 3 == 2
--   subarraySum [1,-1,0] 0 == 3

module Main where

import Data.Map.Strict qualified as M

subarraySum :: [Int] -> Int -> Int
subarraySum nums k = snd (foldl (\(mapper, total) el -> func mapper total el) (M.empty, 0) prefixes)
  where
    prefixes = scanl (+) 0 nums
    func mapper total el = case M.lookup (el - k) mapper of
      Just num -> case M.lookup el mapper of
        Just num_2 -> (M.insert el (num_2 + 1) mapper, total + num)
        Nothing -> (M.insert el 1 mapper, total + num)
      Nothing -> case M.lookup el mapper of
        Just num_2 -> (M.insert el (num_2 + 1) mapper, total)
        Nothing -> (M.insert el 1 mapper, total)

-- ---- tests ----
main :: IO ()
main = do
  check (subarraySum [1, 1, 1] 2) 2
  check (subarraySum [1, 2, 3] 3) 2
  check (subarraySum [1, -1, 0] 0) 3
  check (subarraySum [3, 4, 7, 2, -3, 1, 4, 2] 7) 4
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
