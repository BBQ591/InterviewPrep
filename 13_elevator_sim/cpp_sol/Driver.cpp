#include <algorithm>
#include <vector>

#include "Elevator.h"
using namespace std;

class Driver {
 public:
  int timestamp;
  vector<Elevator> elevators;
  vector<Request> all_requests;
  vector<Request> curr_requests;
  int t_floor;
  int t_stop;
  Driver(int num_elevators, vector<Request> requests, int t_floor, int t_stop)
      : elevators(num_elevators),
        all_requests(requests),
        t_floor(t_floor),
        t_stop(t_stop) {
    timestamp = 0;
  }

  void execute() {
    while (true) {
      timestamp += 1;
      for (auto& request : all_requests) {
        if (request.start_time == timestamp) {
          curr_requests.push_back(request);
        }
      }
      for (auto& elevator : elevators) {
        vector<Request> to_add = elevator.get_next(curr_requests, timestamp);
        for (auto& add : to_add) {
          curr_requests.erase(
              std::remove(curr_requests.begin(), curr_requests.end(), add),
              curr_requests.end());
        }
      }
    }
  }
};
