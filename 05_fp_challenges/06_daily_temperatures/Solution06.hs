-- Daily Temperatures  (LeetCode 739)
-- ===================================
-- For each day, how many days until a WARMER temperature? 0 if none.
--   dailyTemperatures [73,74,75,71,69,72,76,73] == [1,1,4,2,1,1,0,0]
--   dailyTemperatures [30,40,50,60] == [1,1,1,0]
--   dailyTemperatures [30,60,90] == [1,1,0]

module Main where

popping :: [(Int, Int)] -> Int -> [(Int, Int)]
popping [] _ = []
popping total@(s : stack) num = if snd s > num then total else popping stack num

dailyTemperatures :: [Int] -> [Int]
dailyTemperatures temps =
  fst
    ( foldr
        ( \(temp, idx) (ans, stack) ->
            ( fst
                ( head
                    ( case popping stack temp of
                        [] -> (idx, 0) : []
                        other -> other
                    )
                )
                - idx
                : ans,
              ((idx, temp) : popping stack temp)
            )
        )
        ([], [])
        (zip temps [0 ..])
    )

-- ---- tests ----
main :: IO ()
main = do
  check (dailyTemperatures [73, 74, 75, 71, 69, 72, 76, 73]) [1, 1, 4, 2, 1, 1, 0, 0]
  check (dailyTemperatures [30, 40, 50, 60]) [1, 1, 1, 0]
  check (dailyTemperatures [30, 60, 90]) [1, 1, 0]
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
