from typing import List
from dataclasses import dataclass
import copy


@dataclass
class Request:
    start_time: int
    from_floor: int
    to_floor: int
    id: int
    from_fulfilled: bool


class Elevator:
    def __init__(self, id, time_floor, time_elevators):
        self.id = id
        self.floor = 0
        self.queue = []
        self.time = 0
        self.time_floor = time_floor
        self.time_elevators = time_elevators

    def refresh_queue(self, queue: List[Request]) -> List[Request]:
        pass

    def get_queue(self):
        return copy.deepcopy(self.queue)

    def pass_time(self) -> Request | None:
        request = self.queue[0]
        if request.from_fulfilled:
            next_floor = self.queue[0].to_floor
        else:
            next_floor = self.queue[0].from_floor

        self.time += 1
        if self.floor == next_floor:
            if self.time == self.time_elevators:
                self.time = 0
                if request.from_fulfilled:
                    self.queue.remove(request)
                    return request
                else:
                    request.from_fulfilled = True
                    return None
        else:
            if self.time == self.time
        # probably just change the current floor we are on, but tbd. also the current direction
        # on every unit of time, we call this function
        pass


class Controller:
    def __init__(self, elevators: List[Elevator], time_floor: int, time_elevators: int):
        self.elevators = elevators

    def get_elevator(self, request: Request) -> int:
        # only allowed to call get_queue
        pass


class Simulator:
    def __init__(
        self,
        floors: int,
        elevators: int,
        time_floor: int,
        time_elevators: int,
        controller: type[Controller],
        elevator: type[Elevator],
    ):
        self.num_floors = floors
        self.elevators = [elevator(i) for i in range(elevators)]
        self.num_elevators = elevators
        self.time_floor = time_floor
        self.time_elevators = time_elevators
        self.controller = controller(
            self.elevators, self.time_floor, self.time_elevators
        )

    def get_requests_now(self, workload: List[Request], time: int) -> List[Request]:
        out = []
        for request in workload:
            if request.start_time == time:
                out.append(request)
        return out

    def assert_same(self, new_queue, curr_queue):
        for request in curr_queue:
            assert request in new_queue
        assert len(new_queue) == len(curr_queue) + 1

    def execute(self, workload: List[Request]):
        time = 0
        while len(workload) > 0:
            requests_now = self.get_requests_now(workload, time)
            for request in requests_now:
                elevator_num = self.controller.get_elevator(request)
                elevator_tmp = self.elevators[elevator_num]
                new_queue = elevator_tmp.queue.append(request)
                self.assert_same(new_queue, elevator_tmp.get_queue())
                elevator_tmp.queue = new_queue
            for elevator in self.elevators:
                out = elevator.refresh_queue(elevator.get_queue())
                self.assert_same(out, elevator.get_queue())
            passed = []
            for elevator in self.elevators:
                finished = elevator.pass_time()
                if finished is not None:
                    passed.append(finished)
            for request in passed:
                workload.remove(request)
            time += 1
