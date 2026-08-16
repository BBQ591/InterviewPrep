#include <cstddef>
#include <set>
using namespace std;

struct Job {
  size_t run_at;
  int priority;
  int job_id;
  bool is_recurring = false;
  size_t every;
  bool running = false;
  bool operator<(const Job& other) { return run_at < other.run_at; }
};
class Jobs {
 public:
  Jobs() {}
  void submit(int job_id, int priority, size_t run_at) {
    Job job = Job{run_at, priority, job_id};
    one_time_jobs.insert(job);
    job_id_map[job_id] = job;
  }

  vector<Job> refresh_jobs(size_t timestamp) {
    vector<Job> jobs;
    for (auto job : one_time_jobs) {
      if (job.run_at > timestamp) {
        break;
      }
      if (job.running && job.run_at + 30 < timestamp) {
        jobs.push_back(job);
      }
    }
    return jobs;
  }

  int run_at(size_t timestamp) {
    Job highest_priority{0, 0, -1};
    vector<Job> jobs = refresh_jobs(timestamp);
    for (auto job : jobs) {
      Job new_job = job;
      new_job.running = false;
      one_time_jobs.erase(job);
      one_time_jobs.insert(new_job);
      job_id_map[job.job_id] = new_job;
    }
    for (auto job : one_time_jobs) {
      if (job.run_at > timestamp) {
        break;
      }
      if (!job.running && (highest_priority.job_id == -1 ||
                           job.priority > highest_priority.priority)) {
        highest_priority = job;
      }
    }
    if (highest_priority.job_id == -1) {
      return -1;
    }
    one_time_jobs.erase(highest_priority);
    highest_priority.running = true;
    highest_priority.run_at = timestamp;
    one_time_jobs.insert(highest_priority);
    job_id_map[highest_priority.job_id] = highest_priority;
    return highest_priority.job_id;
  }

  void ack(int job_id, size_t now) {
    Job job = job_id_map[job_id];
    if (!job.running) {
      return;
    }
    one_time_jobs.erase(job);
    if (job.is_recurring) {
      size_t new_time = job.run_at + job.every;
      Job new_job = job;
      new_job.run_at = new_time;
      one_time_jobs.insert(new_job);
      job_id_map[job.job_id] = new_job;
    }
  }

  bool cancel(int job_id) {
    Job job = job_id_map[job_id];
    if (!one_time_jobs.count(job)) {
      return false;
    }
    one_time_jobs.erase(job);
    return true;
  }

  bool reschedule(int job_id, size_t new_run_at) {
    if (!job_id_map.count(job_id)) {
      return false;
    }
    Job job = job_id_map[job_id];
    if (!one_time_jobs.count(job)) {
      return false;
    }
    one_time_jobs.erase(job);
    Job new_job = job;
    new_job.run_at = new_run_at;
    job_id_map[job.job_id] = new_job;
    one_time_jobs.insert(new_job);
    return true;
  }

  void submit_recurring(int job_id, int priority, size_t first_run,
                        size_t every) {
    Job job{first_run, priority, job_id, true, every};
    one_time_jobs.insert(job);
    job_id_map[job_id] = job;
  }

 private:
  set<Job> one_time_jobs;  // includes the runs of recurring jobs
  unordered_map<int, Job> job_id_map;
};
