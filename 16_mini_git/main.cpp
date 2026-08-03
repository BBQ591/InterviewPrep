#include "main.h"

#include <filesystem>

using namespace std;
// metadata about git
Git::Git() {
  metadata = parse_metadata(fs::current_path());
  git_path = (fs::path)metadata.root_path / ".git";
}

size_t Git::hash_file(fs::path path) {
  fs::path full_path = metadata.root_path / path;
  ifstream file(full_path);
  string out_file = read_file(file);
  hash<string> string_hasher;
  size_t hash_value = string_hasher(out_file);
  store_file(out_file,
             (fs::path)metadata.root_path / ".git" / to_string(hash_value));
  return hash_value;
}

void Git::cat_object(string hash) {
  fs::path path = (fs::path)metadata.root_path / ".git" / hash;
  ifstream file(path);
  string out = read_file(file);
  file.close();
}

pair<size_t, FileType> Git::write_tree(fs::path path) {
  if (fs::is_regular_file(path)) {
    return {hash_file(path), FileType::FILE};
  }
  string file_content;
  for (const auto& entry : fs::directory_iterator(path)) {
    if (entry.path().filename().string()[0] == '.') {
      continue;
    }
    pair<size_t, FileType> out = write_tree(entry.path());
    size_t hash = out.first;
    FileType type = out.second;
    string builder;
    if (file_content.size() > 0) {
      builder = ",";
    }
    builder += entry.path().filename().string() + " " + to_string(hash) + " ";
    if (type == FileType::DIRECTORY) {
      builder += "directory";
    } else {
      builder += "file";
    }

    file_content += builder;
  }
  hash<string> string_hasher;
  size_t hash_value = string_hasher(file_content);
  ofstream file((fs::path)metadata.root_path / ".git" / to_string(hash_value));
  file << file_content;
  file.close();
  return {hash_value, FileType::DIRECTORY};
}

void Git::commit(string message, size_t timestamp) {
  pair<size_t, FileType> out = write_tree(fs::current_path());
  size_t hash = out.first;
  ofstream commit_file((fs::path)metadata.root_path / ".git" / "commit.txt",
                       ios::app);
  commit_file << "\"" << message << "\" " << timestamp << " " << hash << endl;
}

void Git::log() {
  ifstream commit_file((fs::path)metadata.root_path / ".git" / "commit.txt");
  vector<Commit> commits;
  string line;
  while (getline(commit_file, line)) {
    vector<string> split_quotes = split(line, '\"');
    string message = split_quotes[1];
    string remaining = split_quotes[2];
    vector<string> split_space = split(remaining, ' ');
    commits.push_back(
        Commit{message, static_cast<std::size_t>(std::stoull(split_space[1])),
               static_cast<std::size_t>(std::stoull(split_space[2]))});
  }
  reverse(commits.begin(), commits.end());
  for (auto& commit : commits) {
    cout << "message: " << commit.message << endl
         << "timestamp: " << commit.timestamp << endl
         << "hash: " << commit.hash << endl
         << endl
         << "------------------" << endl
         << endl;
  }
}

void Git::checkout(string hash, FileType type, fs::path full_path) {
  fs::path path = (fs::path)metadata.root_path / ".git" / hash;
  if (type == FileType::FILE) {
    fs::path file_path = (fs::path)metadata.root_path / full_path;
    ofstream out(file_path);
    ifstream in(path);
    string file = read_file(in);
    out << file;
    out.close();
    return;
  }

  if (full_path != "") {
    // ensure this isnt the root
    fs::path folder_path = (fs::path)metadata.root_path / full_path;
    fs::create_directory(folder_path);
  }
  ifstream file(path);
  string line;
  getline(file, line);
  vector<string> _entries = split(line, ',');
  vector<DirectoryEntry> entries;
  for (auto& el : _entries) {
    vector<string> fields = split(el, ' ');
    FileType tmp_type =
        fields[2] == "file" ? FileType::FILE : FileType::DIRECTORY;
    DirectoryEntry entry{fields[0], fields[1], tmp_type};
    entries.push_back(entry);
  }
  for (auto entry : entries) {
    checkout(entry.hash, entry.type, full_path / entry.name);
  }
}
vector<string> Git::split(string str, char splitter) {
  vector<string> out;
  stringstream stringer(str);
  string word;
  vector<string> words;
  while (getline(stringer, word, splitter)) {
    out.push_back(word);
  }
  return out;
}

MetadataObject Git::read_lines(ifstream& file) {
  MetadataObject obj;
  getline(file, obj.root_path);
  return obj;
}
MetadataObject Git::parse_metadata(fs::path curr_dir) {
  bool found = false;
  while (fs::exists(curr_dir) && !found) {
    if (!fs::is_directory(curr_dir)) {
      curr_dir = curr_dir.parent_path();
      continue;
    }
    for (const auto& entry : fs::directory_iterator(curr_dir)) {
      if (entry.path().filename().string() == ".git") {
        found = true;
        break;
      }
    }
    if (!found) {
      curr_dir = curr_dir.parent_path();
    }
  }
  if (!found) {
    throw runtime_error(".git file not found in path");
  }
  bool found_metadata = false;
  curr_dir = curr_dir / ".git";
  for (const auto& entry : fs::directory_iterator(curr_dir)) {
    if (entry.path().filename().string() == "metadata.txt") {
      found_metadata = true;
      break;
    }
  }
  if (!found_metadata) {
    throw runtime_error("metadata not found in .git");
  }
  curr_dir = curr_dir / "metadata.txt";
  ifstream file(curr_dir);
  MetadataObject metadata = read_lines(file);
  return metadata;
}

string Git::read_file(ifstream& file) {
  stringstream buffer;
  buffer << file.rdbuf();
  string content = buffer.str();
  return content;
}

void Git::store_file(string content, fs::path path) {
  ofstream file(path);
  file << content;
  file.close();
}
