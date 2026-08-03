-- Hamming Numbers / Ugly Number II  (LeetCode 264)
-- ================================================
-- A Hamming number is a positive integer with no prime factors other than
-- 2, 3 and 5. The sequence starts 1,2,3,4,5,6,8,9,10,12,15,16,...
-- Define `hammings`, the (infinite) sorted list of all of them.
--   take 12 hammings == [1,2,3,4,5,6,8,9,10,12,15,16]
--   nthHamming 10 == 12
--
-- Testing integers one at a time for smoothness is far too slow for the
-- last test -- the sequence has to be generated directly.

module Main where

import Data.List

_hammings :: [Int] -> [Int]
_hammings curr_amount = min_el : _hammings (smallest_arrays ++ (filter (\x -> x /= min_el) curr_amount))
  where
    min_el = minimum curr_amount
    smallest_arrays = [min_el * 2, min_el * 3, min_el * 5]

hammings :: [Int]
hammings = _hammings [1]

nthHamming :: Int -> Int
nthHamming n = hammings !! (n - 1)

-- ---- tests ----
main :: IO ()
main = do
  check (take 12 hammings) [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16]
  check (nthHamming 1) 1
  check (nthHamming 10) 12
  check (nthHamming 11) 15
  check (nthHamming 1500) 859963392
  putStrLn "all passed"
  where
    check :: (Eq a, Show a) => a -> a -> IO ()
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
