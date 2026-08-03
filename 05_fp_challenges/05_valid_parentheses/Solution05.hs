-- Valid Parentheses  (LeetCode 20)
-- =================================
-- Given a string of just ()[]{}, return True iff every bracket is closed by the
-- matching type in the correct order.
--   isValid "()[]{}" == True
--   isValid "(]" == False
--   isValid "([)]" == False
--   isValid "{[]}" == True

module Main where

isValid :: String -> Bool
isValid s = ans && length tmp_stack == 0
  where
    (ans, tmp_stack) =
      foldl
        ( \(bool, stack) x ->
            if bool == False
              then (False, stack)
              else case x of
                '(' -> (bool, x : stack)
                ')' -> if head stack == '(' then (bool, tail stack) else (False, stack)
                '{' -> (bool, x : stack)
                '}' -> if head stack == '{' then (bool, tail stack) else (False, stack)
                '[' -> (bool, x : stack)
                ']' -> if head stack == '[' then (bool, tail stack) else (False, stack)
                _ -> (False, stack)
        )
        (True, [])
        s

-- ---- tests ----
main :: IO ()
main = do
  check (isValid "()") True
  check (isValid "()[]{}") True
  check (isValid "(]") False
  check (isValid "([)]") False
  check (isValid "{[]}") True
  check (isValid "(") False
  check (isValid "") True
  putStrLn "all passed"
  where
    check got want
      | got == want = putStrLn ("  PASS  " ++ show got)
      | otherwise = error ("  FAIL  got " ++ show got ++ " want " ++ show want)
