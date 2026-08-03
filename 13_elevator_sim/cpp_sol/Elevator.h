#include <vector>
using namespace std;
#pragma once
struct Request {
  int start_time;
  int start_floor;
  int end_floor;
  bool reached_start = false;
};
enum class Mode { WAITING, MOVING };

struct Response {
  int direction;  // 0, 1, -1
  vector<Request> add;
  Mode new_mode;
};

class Elevator {
 public:
  int level = 0;
  int t_floor;
  int t_stop;
  int time = 0;
  Mode mode = Mode::WAITING;
  vector<Request> holding;
  Elevator(int t_floor, int t_stop);
  vector<Request> get_next(vector<Request> requests, int timestamp);
  virtual Response handle_new_floor(vector<Request>& available_requests,
                                    int timestamp);
  virtual vector<Request> handle_current_floor(vector<Request> requests,
                                               int timestamp);
};
