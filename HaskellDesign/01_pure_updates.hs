-- 01: Pure updates — state as values, change as functions.
-- Replace each `todo` body. Run: runghc 01_pure_updates.hs

import Control.Exception (SomeException, evaluate, try)
import Data.Either (isLeft)
import Data.List qualified
import Data.Set qualified

todo :: a
todo = error "TODO"

-- ---------------------------------------------------------------------------
-- Part A: the elevator helpers, in their native tongue.
-- ---------------------------------------------------------------------------

instance Ord Req where
  compare r1 r2 = compare (key r1) (key r2)
    where
      key (Req reqFrom reqTo boarded) = (reqFrom, reqTo, boarded)

data Req = Req {reqFrom :: Int, reqTo :: Int, boarded :: Bool}
  deriving (Eq, Show)

-- 1. The helper we discussed for Elevator::get_next: keep everyone who is
--    NOT getting off at this level (getting off = boarded and reqTo == level).
remainingAfterDropoff :: Int -> [Req] -> [Req]
remainingAfterDropoff level holding = Data.List.filter (filter_func) holding
  where
    filter_func (Req reqFrom reqTo boarded) = (not (boarded)) || (reqTo /= level)

-- 2. Same event, but return BOTH halves: (delivered, stillRiding).
--    Hint: Data.List.partition. Preserve order within each half.
dropoff :: Int -> [Req] -> ([Req], [Req])
dropoff level holding = (stillRiding, remaining)
  where
    remaining = remainingAfterDropoff level holding
    remaining_set = Data.Set.fromList remaining
    stillRiding = filter (\element -> not (Data.Set.member element remaining_set)) holding

-- 3. Board everyone whose reqFrom is this level: boarded becomes True.
--    Record update syntax: r { boarded = True }. Everyone else unchanged.
boardAt :: Int -> [Req] -> [Req]
boardAt level holding = map (new_value) holding
  where
    new_value (Req reqFrom reqTo boarded) = if (not boarded && reqFrom == level) then (Req reqFrom reqTo True) else (Req reqFrom reqTo boarded)

-- ---------------------------------------------------------------------------
-- Part B: a bank ledger — errors as data, history as a return value.
-- ---------------------------------------------------------------------------

data Account = Account {owner :: String, balance :: Int} deriving (Eq, Show)

data Tx = Deposit Int | Withdraw Int deriving (Eq, Show)

-- 4. Apply one transaction. Withdrawing MORE than the balance is a Left
--    (withdrawing exactly the balance is fine). Any Left message you like.
applyTx :: Account -> Tx -> Either String Account
applyTx acct tx = todo

-- 5. Apply many, stopping at the first failure.
--    Write it with explicit recursion first. (Later: compare with foldM.)
applyAll :: Account -> [Tx] -> Either String Account
applyAll acct txs = todo

-- 6. Apply many, SKIPPING failures, and return an event log describing what
--    happened, in order — one line per transaction, applied or rejected.
--    The exact wording is your design; checks only count lines.
--    (This is your elevator event log, miniaturized.)
ledger :: Account -> [Tx] -> (Account, [String])
ledger acct txs = todo

-- ---------------------------------------------------------------------------
-- Checks
-- ---------------------------------------------------------------------------

check :: String -> Bool -> IO ()
check name b = do
  r <- try (evaluate b) :: IO (Either SomeException Bool)
  putStrLn $ case r of
    Left _ -> "TODO " ++ name
    Right True -> "PASS " ++ name
    Right False -> "FAIL " ++ name

main :: IO ()
main = do
  let h = [Req 2 9 True, Req 0 3 True, Req 3 9 False, Req 5 3 True]
  check
    "1 remainingAfterDropoff keeps non-arrivals"
    (remainingAfterDropoff 3 h == [Req 2 9 True, Req 3 9 False])
  check
    "1 remainingAfterDropoff leaves unboarded alone"
    (remainingAfterDropoff 9 h == [Req 0 3 True, Req 3 9 False, Req 5 3 True])
  check
    "2 dropoff returns both halves in order"
    (dropoff 3 h == ([Req 0 3 True, Req 5 3 True], [Req 2 9 True, Req 3 9 False]))
  check
    "3 boardAt flips exactly the waiters here"
    (boardAt 3 h == [Req 2 9 True, Req 0 3 True, Req 3 9 True, Req 5 3 True])
  let a = Account "b" 100
  check "4 deposit" (applyTx a (Deposit 50) == Right (Account "b" 150))
  check "4 withdraw-all ok" (applyTx a (Withdraw 100) == Right (Account "b" 0))
  check "4 overdraft is Left" (isLeft (applyTx a (Withdraw 200)))
  check "5 applyAll success" (applyAll a [Deposit 10, Withdraw 50] == Right (Account "b" 60))
  check
    "5 applyAll stops at failure"
    (isLeft (applyAll a [Deposit 10, Withdraw 50, Withdraw 100]))
  let (a', logLines) = ledger a [Deposit 10, Withdraw 999, Withdraw 50]
  check "6 ledger skips failures" (balance a' == 60)
  check "6 ledger logs every tx" (length logLines == 3)
