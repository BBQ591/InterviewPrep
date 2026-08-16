#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <ostream>
#include <set>
#include <sstream>
#include <string>
using namespace std;
namespace fs = filesystem;

#ifndef MAIN_H
#define MAIN_H

struct Diff {
  string file_name;
  size_t hash1;
  size_t hash2;
  string diff;
};

struct Commit {
  string message;
  int timestamp;
  size_t curr_hash;
  size_t parent_hash;
};
struct MetadataObject {
  string root_path;
  string curr_branch;
};

enum class FileType { DIRECTORY, FILE };

struct DirectoryEntry {
  string name;
  string hash;
  FileType type;
};

class Git {
  MetadataObject metadata;
  fs::path git_path;

 public:
  Git();
  size_t hash_file(fs::path path);
  void cat_object(string hash);
  pair<size_t, FileType> write_tree(fs::path path);
  void commit(string message, size_t timestamp);
  void log();
  void checkout(string hash, FileType type, fs::path full_path);
  void create_branch(string name);
  vector<string> get_diff(size_t hash1, size_t hash2);

 private:
  MetadataObject parse_metadata(fs::path path);
  MetadataObject read_lines(ifstream& stream);
  string read_file(ifstream& stream);
  void store_file(string stream, fs::path);
  vector<string> split(string str, char splitter);
  pair<string, string> split_by_quote(string line);
  void _checkout(string hash, FileType type, fs::path full_path);
  vector<pair<string, size_t>> get_branches();
  vector<Commit> get_commits();
  unordered_map<string, size_t> get_children(size_t hash1);
  string _diff(Diff diff);
  vector<Commit> get_commit_history_hash(size_t hash);
};

#endif
