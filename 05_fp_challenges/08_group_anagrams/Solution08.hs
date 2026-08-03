-- Group Anagrams  (LeetCode 49)
-- ==============================
-- Group strings that are anagrams of each other. Order of groups / within groups
-- doesn't matter for correctness (the test sorts before comparing).
--   groupAnagrams ["eat","tea","tan","ate","nat","bat"]
--     == [["ate","eat","tea"],["bat"],["nat","tan"]]   (up to ordering)

module Main where

import Data.Function (on)
import Data.List (groupBy, sort, sortBy)

groupAnagrams :: [String] -> [[String]]
groupAnagrams ws = map (\x -> map (snd) x) ((groupBy (\x y -> fst x == fst y) (sort (zip freqs ws))))
  where
    freqs = map (sort) ws

-- ---- tests ----
-- Canonicalize both sides (sort groups, sort within groups) before comparing.
canon :: [[String]] -> [[String]]
canon = sort . map sort

main :: IO ()
main = do
  check
    (groupAnagrams ["eat", "tea", "tan", "ate", "nat", "bat"])
    [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
  check (groupAnagrams [""]) [[""]]
  check (groupAnagrams ["a"]) [["a"]]
  putStrLn "all passed"
  where
    check got want
      | canon got == canon want = putStrLn ("  PASS  " ++ show (canon got))
      | otherwise = error ("  FAIL  got " ++ show (canon got) ++ " want " ++ show (canon want))
