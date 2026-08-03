#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <ostream>
#include <sstream>
#include <string>
using namespace std;
namespace fs = filesystem;

#ifndef MAIN_H
#define MAIN_H
struct MetadataObject {
  string root_path;
};

struct Commit {
  string message;
  size_t timestamp;
  size_t hash;
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

 private:
  MetadataObject parse_metadata(fs::path path);
  MetadataObject read_lines(ifstream& stream);
  string read_file(ifstream& stream);
  void store_file(string stream, fs::path);
  vector<string> split(string str, char splitter);
};

#endif
