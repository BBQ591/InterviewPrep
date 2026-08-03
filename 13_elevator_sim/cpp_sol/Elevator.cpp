#include "Elevator.h"

Elevator::Elevator(int t_floor, int t_stop)
    : t_floor(t_floor), t_stop(t_stop) {}

vector<Request> Elevator::get_next(vector<Request> requests, int timestamp) {
  time += 1;
  if (mode == Mode::WAITING && time == t_stop) {
    for (auto& request : holding) {
      if (request.reached_start && request.end_floor == level) {
        holding.erase(std::remove(holding.begin(), holding.end(), request),
                      holding.end());
      }
    }
    for (auto& request : holding) {
      if (request.start_floor == level) {
        request.reached_start = true;
      }
    }
    time = 0;
  }
  if (mode == Mode::MOVING && time == t_floor) {
    time = 0;
  }
  if (time == 0) {
    // reset
    Response out = handle_new_floor(requests, timestamp);
    level += out.direction;
    mode = out.new_mode;
    return out.add;
  } else {
    vector<Request> out = handle_current_floor(requests, timestamp);
    return out;
  }
}
