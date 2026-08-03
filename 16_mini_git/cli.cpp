#include <filesystem>
#include <fstream>
#include <iostream>
#include <ostream>

#include "main.h"
using namespace std;
namespace fs = filesystem;

void handle_init() {
  fs::path curr_path = fs::current_path();
  fs::create_directories(curr_path / ".git");
  ofstream file(curr_path / ".git" / "metadata.txt");
  file << curr_path.string();
}

void handle_hashing(string file) {
  Git obj;
  size_t hash = obj.hash_file(file);
  cout << "This is the hash of the file: " << hash << endl;
}

void handle_cat(string path) {
  Git obj;
  obj.cat_object(path);
}

void handle_write_tree() {
  Git obj;
  obj.write_tree(fs::current_path());
}

void handle_commit(string message, string timestamp) {
  Git obj;
  obj.commit(message, static_cast<std::size_t>(std::stoull(timestamp)));
}

void handle_log() {
  Git obj;
  obj.log();
}

void handle_checkout(string hash) {
  Git obj;
  obj.checkout(hash, FileType::DIRECTORY, "");
}

int main(int argc, char* argv[]) {
  if (argc <= 1) {
    cout << "No Arguments" << endl;
    return 0;
  }
  if (strcmp(argv[1], "init") == 0) {
    handle_init();
  }
  if (strcmp(argv[1], "hash_object") == 0) {
    handle_hashing(argv[2]);
  }
  if (strcmp(argv[1], "cat_object") == 0) {
    handle_cat(argv[2]);
  }
  if (strcmp(argv[1], "write_tree") == 0) {
    handle_write_tree();
  }
  if (strcmp(argv[1], "commit") == 0) {
    handle_commit(argv[3], argv[5]);
  }
  if (strcmp(argv[1], "log") == 0) {
    handle_log();
  }
  if (strcmp(argv[1], "checkout") == 0) {
    handle_checkout(argv[2]);
  }
}
