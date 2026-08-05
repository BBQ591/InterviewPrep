#ifndef SOLUTION_H
#define SOLUTION_H
#include <stdexcept>
#include <utility>
using namespace std;

template <typename T>
class Vec {
 public:
  Vec(int n) {
    pointer = (T*)malloc(n * sizeof(T));
    size = n;
    array_size = n;
  }
  Vec() {
    size = 0;
    array_size = 2;
    pointer = (T*)malloc(2 * sizeof(T));
  }
  T& operator[](size_t i) { return pointer[i]; }
  void push_back(T obj) {
    if (size + 1 > array_size) {
      pair<T*, int> out = double_size();
      array_size = out.second;
      pointer = out.first;
    }
    pointer[size] = obj;
    size += 1;
  }
  void pop() {
    if (size == 0) {
      throw invalid_argument("size is zero");
    }

    size -= 1;
    pointer[size] = 0;
  }
  int length() { return size; }
  T* data() { return pointer; }
  void clear() {
    for (int i = 0; i < size; i++) {
      pointer[i] = 0;
    }
    size = 0;
  }
  Vec(const Vec& other) {
    clear();
    for (int i = 0; i < other.length(); i++) {
      pointer[i] = other[i];
    }
  }
  ~Vec() { free(pointer); }

 private:
  pair<T*, int> double_size() {
    int old_array_size = array_size;
    array_size *= 2;
    T* new_pointer = (T*)malloc(array_size * sizeof(T));
    memcpy(new_pointer, pointer, old_array_size * sizeof(T));
    free(pointer);
    return {new_pointer, array_size};
  }
  int size = 0;
  int array_size = 0;
  T* pointer;
};

#endif
