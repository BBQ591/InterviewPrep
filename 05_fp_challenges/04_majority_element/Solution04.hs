-- Majority Element  (LeetCode 169)
-- =================================
-- Return the element that appears MORE than n/2 times (guaranteed to exist).
-- Aim for O(1) extra space (Boyer-Moore), not a frequency map.
--   majority [3,2,3] == 3
--   majority [2,2,1,1,1,2,2] == 2

module Main where

func :: (Int, Int) -> Int -> (Int, Int)
func (acc, num) tmp = if num == tmp then (acc + 1, num) else if acc == 0 then (1, tmp) else (acc - 1, num)

majority :: [Int] -> Int
majority nums = num
  where
    (freq, num) = foldl (\acc x -> func acc x) (0, 0) nums

-- ---- tests ----
main :: IO ()
main = do
  check (majority [3, 2, 3]) 3
  check (majority [2, 2, 1, 1, 1, 2, 2]) 2
  check (majority [1]) 1
  check (majority [6, 6, 6, 7, 7]) 6
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
