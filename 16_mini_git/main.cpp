#include "main.h"

#include <filesystem>
#include <stdexcept>

using namespace std;
// metadata about git
Git::Git() {
  metadata = parse_metadata(fs::current_path());
  git_path = (fs::path)metadata.root_path / ".git";
}
void handle_delete_line(int line_num, string new_val, fs::path path) {
  vector<string> all_lines;
  ifstream file(path);
  string line;
  while (getline(file, line)) {
    all_lines.push_back(line);
  }
  file.close();
  vector<string> new_set;
  for (int i = 0; i < all_lines.size(); i++) {
    if (i == line_num && new_val != "") {
      new_set.push_back(new_val);
    } else if (i != line_num) {
      new_set.push_back(all_lines[i]);
    }
  }
  ofstream file2(path);
  for (int i = 0; i < new_set.size(); i++) {
    file2 << new_set[i] << endl;
  }
  file2.close();
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
  vector<pair<string, size_t>> branches = get_branches();
  int index = -1;
  for (int i = 0; i < branches.size(); i++) {
    if (branches[i].first == metadata.curr_branch) {
      index = i;
      break;
    }
  }
  pair<size_t, FileType> out = write_tree(fs::current_path());
  size_t hash = out.first;
  ofstream commit_file((fs::path)metadata.root_path / ".git" / "commit.txt",
                       ios::app);
  commit_file << "\"" << message << "\" " << timestamp << " " << hash << " "
              << branches[index].second << endl;
  commit_file.close();

  string new_line = "\"" + metadata.curr_branch + "\" " + to_string(hash);
  handle_delete_line(index, new_line,
                     (fs::path)metadata.root_path / ".git" / "branches.txt");
  // this is a tmp comment
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

pair<string, string> Git::split_by_quote(string line) {
  vector<string> split_quotes = split(line, '\"');
  string message = split_quotes[1];
  string remaining = split_quotes[2];
  return {message, remaining};
}

vector<Commit> Git::get_commits() {
  ifstream commit_file((fs::path)metadata.root_path / ".git" / "commit.txt");
  vector<Commit> commits;
  string line;
  while (getline(commit_file, line)) {
    pair<string, string> out = split_by_quote(line);
    string message = out.first;
    string remaining = out.second;
    vector<string> split_space = split(remaining, ' ');
    string timestamp = split_space[1];
    string curr_hash = split_space[2];
    string parent_hash = split_space[3];
    commits.push_back(Commit{message, static_cast<int>(std::stoull(timestamp)),
                             static_cast<std::size_t>(std::stoull(curr_hash)),
                             static_cast<size_t>(stoull(parent_hash))});
  }
  return commits;
}

void Git::log() {
  unordered_map<size_t, size_t> edges;
  unordered_map<size_t, Commit> map_commits;
  vector<Commit> commits = get_commits();
  for (auto commit : commits) {
    edges[commit.curr_hash] = commit.parent_hash;
    map_commits[commit.curr_hash] = commit;
  }
  vector<pair<string, size_t>> branches = get_branches();
  size_t branch_hash;
  for (int i = 0; i < branches.size(); i++) {
    if (branches[i].first == metadata.curr_branch) {
      branch_hash = branches[i].second;
      break;
    }
  }
  vector<Commit> commit_history;
  while (branch_hash != 0) {
    commit_history.push_back(map_commits[branch_hash]);
    branch_hash = edges[branch_hash];
  }
  for (auto& commit : commit_history) {
    cout << "message: " << commit.message << endl
         << "timestamp: " << commit.timestamp << endl
         << "hash: " << commit.curr_hash << endl
         << endl
         << "------------------" << endl
         << endl;
  }
}

vector<pair<string, size_t>> Git::get_branches() {
  fs::path metadata_path =
      (fs::path)metadata.root_path / ".git" / "branches.txt";
  ifstream file(metadata_path);
  string line;
  vector<pair<string, size_t>> out;
  while (getline(file, line)) {
    pair<string, string> split_quotes = split_by_quote(line);
    string branch = split_quotes.first;
    size_t hash = stoull(split_quotes.second.substr(1));
    out.push_back({branch, hash});
  }
  return out;
}

void Git::_checkout(string hash, FileType type, fs::path full_path) {
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
    _checkout(entry.hash, entry.type, full_path / entry.name);
  }
}

void Git::checkout(string hash, FileType type, fs::path full_path) {
  vector<pair<string, size_t>> branches = get_branches();
  int is_branch = -1;
  for (int i = 0; i < branches.size(); i++) {
    if (branches[i].first == hash) {
      is_branch = i;
      break;
    }
  }
  string tmp_hash = hash;
  if (is_branch != -1) {
    tmp_hash = to_string(branches[is_branch].second);
    handle_delete_line(1, branches[is_branch].first,
                       (fs::path)metadata.root_path / ".git" / "metadata.txt");
  } else {
    for (int i = 0; i < branches.size(); i++) {
      if (branches[i].first == metadata.curr_branch) {
        is_branch = i;
        break;
      }
    }
    string to_write = "\"" + metadata.curr_branch + "\" " + hash;
    handle_delete_line(is_branch, to_write,
                       (fs::path)metadata.root_path / ".git" / "branches.txt");
  }
  _checkout(tmp_hash, type, full_path);
}
MetadataObject Git::read_lines(ifstream& file) {
  MetadataObject obj;
  getline(file, obj.root_path);
  getline(file, obj.curr_branch);
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

void Git::create_branch(string branch_name) {
  vector<pair<string, size_t>> branches = get_branches();
  if (branches[0].first != "master") {
    throw runtime_error("branch state is wrong");
  }
  if (branches[0].second == 0) {
    throw runtime_error(
        "you have not committed. please commit before creating a new branch");
  }
  string write = "\"" + branch_name + "\" " + to_string(branches[0].second);
  ofstream out((fs::path)metadata.root_path / ".git" / "branches.txt",
               ios::app);
  out << write << endl;
  out.close();
}

void Git::diff(string hash1, string hash2) {}
