-- 02: ADTs + errors as data. An expression language, no exceptions anywhere.
-- Replace each `todo` body. Run: runghc 02_adts_errors.hs

import Control.Exception (SomeException, evaluate, try)
import Data.Either (isLeft)

todo :: a
todo = error "TODO"

data Expr
  = Num Int
  | Var String
  | Add Expr Expr
  | Mul Expr Expr
  | Div Expr Expr
  | Neg Expr
  deriving (Eq, Show)

type Env = [(String, Int)]

-- 1. render: fully parenthesized, spaces around binary operators.
--      Add (Num 1) (Mul (Num 2) (Var "x"))  ->  "(1 + (2 * x))"
--      Neg (Var "x")                        ->  "(-x)"
render :: Expr -> String
render e = todo

-- 2. eval: an undefined variable or a division by zero is a Left (your
--    message). SPEC DECISION (write it in a comment): what does 7 / 2 mean?
--    The checks assume Haskell's `div` (rounds toward negative infinity).
eval :: Env -> Expr -> Either String Int
eval env e = todo

-- 3. simplify: recursively apply the obvious identities
--      Add (Num 0) e -> e        Mul (Num 1) e -> e
--      e `Add` Num 0 -> e        e `Mul` Num 1 -> e
--      Mul (Num 0) _ -> Num 0    _ `Mul` Num 0 -> Num 0
--    Simplify children FIRST, then look at the node (or an identity hiding
--    inside, like Add (Num 0) (Mul (Var "y") (Num 1)), will escape you).
simplify :: Expr -> Expr
simplify e = todo

-- 4. vars: every variable name, in order of first appearance, no duplicates.
vars :: Expr -> [String]
vars e = todo

-- ---------------------------------------------------------------------------
-- Checks
-- ---------------------------------------------------------------------------

check :: String -> Bool -> IO ()
check name b = do
  r <- try (evaluate b) :: IO (Either SomeException Bool)
  putStrLn $ case r of
    Left _      -> "TODO " ++ name
    Right True  -> "PASS " ++ name
    Right False -> "FAIL " ++ name

main :: IO ()
main = do
  let e1 = Add (Num 1) (Mul (Num 2) (Var "x"))
  check "1 render" (render e1 == "(1 + (2 * x))")
  check "1 render neg" (render (Neg (Var "x")) == "(-x)")
  check "2 eval" (eval [("x", 4)] e1 == Right 9)
  check "2 undefined var is Left" (isLeft (eval [] (Var "x")))
  check "2 div by zero is Left" (isLeft (eval [("x", 1)] (Div (Var "x") (Num 0))))
  check "2 integer division decided" (eval [] (Div (Num 7) (Num 2)) == Right 3)
  check "3 simplify unit" (simplify (Mul (Num 1) (Var "x")) == Var "x")
  check "3 simplify nested" (simplify (Add (Num 0) (Mul (Var "y") (Num 1))) == Var "y")
  check "3 simplify zero" (simplify (Mul (Var "x") (Num 0)) == Num 0)
  check "4 vars in order, no dups"
    (vars (Add (Var "x") (Mul (Var "y") (Var "x"))) == ["x", "y"])
