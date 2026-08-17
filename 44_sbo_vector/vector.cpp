#include <cstdlib>
#include <cstring>
template <typename T>
class NewVector {
 public:
  void push_back(T element) {
    if (allocated) {
      // go to heap
      if (num_elements + 1 > frame_size) {
        T* tmp_pointer = malloc(sizeof(T) * frame_size * 2);
        memcpy(tmp_pointer, data_pointer, frame_size * sizeof(T));
        frame_size *= 2;
        data_pointer = tmp_pointer;
      }
      data_pointer[num_elements] = element;
      num_elements += 1;
    } else {
      if (num_elements + 1 <= 10) {
        // stay with stack
        stack_array[num_elements] = element;
        num_elements += 1;
      } else {
        // go to heap, set the bool to true and allocate
        allocated = true;
        frame_size = 16;
        data_pointer = malloc(sizeof(T) * frame_size);
        memcpy(data_pointer, stack_array, 10 * sizeof(T));
        data_pointer[num_elements] = element;
        num_elements += 1;
      }
    }
  }

 private:
  T* data_pointer;
  bool allocated = false;
  int num_elements = 0;
  T stack_array[10];
  int frame_size = 0;
};
