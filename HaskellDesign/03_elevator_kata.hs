-- 03: The elevator kata — your C++ project's P1, but pure. No mutation exists.
-- One elevator, instant doors, 1 floor per tick. The WHOLE simulation is
--     tick :: World -> (World, [Event])
-- Checks below are PROPERTIES, not exact logs — the fine-grained semantics
-- are yours to decide and write down, same as the C++ spec demands.
--
-- Suggested tick order (decide, then document yours):
--   1. time advances by 1
--   2. announce: every pending req with rTime <= new time joins waiting
--   3. deliver:  every rider with rTo == level exits          (Delivered)
--   4. board:    every waiter with rFrom == level gets on     (Boarded)
--   5. move:     pick a target — first rider's rTo, else first waiter's
--                rFrom, else stay put — and step 1 floor toward it (Moved).
--                Emit Moved ONLY when the level actually changes.
--
-- Run: runghc 03_elevator_kata.hs

import Control.Exception (SomeException, evaluate, try)
import Data.List (sort)

todo :: a
todo = error "TODO"

data Req = Req { rid :: Int, rTime :: Int, rFrom :: Int, rTo :: Int }
  deriving (Eq, Show)

data World = World
  { wTime    :: Int
  , wLevel   :: Int
  , wPending :: [Req]   -- not yet announced
  , wWaiting :: [Req]   -- announced, standing at rFrom
  , wRiding  :: [Req]
  } deriving (Eq, Show)

data Event
  = Announced Int Int   -- time, rid
  | Boarded   Int Int   -- time, rid
  | Delivered Int Int   -- time, rid
  | Moved     Int Int   -- time, new level
  deriving (Eq, Show)

-- 1. Split pending: (announced now, still pending).
announceAt :: Int -> [Req] -> ([Req], [Req])
announceAt now pend = todo

-- 2. Split riders: (delivered here, still riding).
deliverAt :: Int -> [Req] -> ([Req], [Req])
deliverAt level riders = todo

-- 3. Split waiters: (boarding here, still waiting).
boardFrom :: Int -> [Req] -> ([Req], [Req])
boardFrom level waiters = todo

-- 4. Where is this elevator headed? (Nothing = nowhere to go.)
targetOf :: World -> Maybe Int
targetOf w = todo

-- 5. One step from `here` toward `there` (equal -> stay).
stepToward :: Int -> Int -> Int
stepToward here there = todo

-- 6. The simulation. Compose 1-5; return the new world and this tick's
--    events, in the order things happened.
tick :: World -> (World, [Event])
tick w = todo

-- Provided: the imperative shell. `runFor` is fueled so a buggy tick makes
-- checks FAIL instead of hanging forever.
done :: World -> Bool
done w = null (wPending w) && null (wWaiting w) && null (wRiding w)

runFor :: Int -> World -> [Event]
runFor 0 _ = []
runFor n w
  | done w    = []
  | otherwise = let (w', evs) = tick w in evs ++ runFor (n - 1) w'

-- ---------------------------------------------------------------------------
-- Checks (properties)
-- ---------------------------------------------------------------------------

check :: String -> Bool -> IO ()
check name b = do
  r <- try (evaluate b) :: IO (Either SomeException Bool)
  putStrLn $ case r of
    Left _      -> "TODO " ++ name
    Right True  -> "PASS " ++ name
    Right False -> "FAIL " ++ name

annT, brdT, delT :: [Event] -> [(Int, Int)]   -- rid -> time
annT evs = [(i, t) | Announced t i <- evs]
brdT evs = [(i, t) | Boarded   t i <- evs]
delT evs = [(i, t) | Delivered t i <- evs]

lifecycleOk :: [Event] -> Int -> Bool
lifecycleOk evs i =
  case (lookup i (annT evs), lookup i (brdT evs), lookup i (delT evs)) of
    (Just a, Just b, Just d) -> a <= b && b <= d
    _                        -> False

main :: IO ()
main = do
  let reqs = [Req 1 0 2 4, Req 2 3 5 1, Req 3 3 0 4]
      w0   = World { wTime = 0, wLevel = 0
                   , wPending = reqs, wWaiting = [], wRiding = [] }
      evs  = runFor 1000 w0
      lvls = wLevel w0 : [f | Moved _ f <- evs]
  check "everyone gets delivered" (sort (map fst (delT evs)) == [1, 2, 3])
  check "announced <= boarded <= delivered, for each rider"
    (all (lifecycleOk evs) [1, 2, 3])
  check "every move is exactly one floor"
    (all (\(a, b) -> abs (a - b) == 1) (zip lvls (tail lvls)))
  check "simulation actually terminates"
    (done (fst (iterateTick 1000 w0)))
  where
    iterateTick :: Int -> World -> (World, ())
    iterateTick 0 w = (w, ())
    iterateTick n w | done w    = (w, ())
                    | otherwise = iterateTick (n - 1) (fst (tick w))
