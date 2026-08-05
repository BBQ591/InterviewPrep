#include <iostream>

#include "Solution.h"
using namespace std;
int main() {
  Vec<int> tmp(5);
  for (int i = 0; i < 5; i++) {
    tmp[i] = i;
  }
  for (int i = 0; i < 5; i++) {
    cout << tmp[i] << endl;
  }
  tmp.clear();
  for (int i = 0; i < 100000; i++) {
    tmp.push_back(i);
  }
  for (int i = 0; i < 100000; i++) {
    cout << tmp[i] << endl;
  }
  for (int i = 0; i < 20; i++) {
    tmp.pop();
  }
  for (int i = 0; i < tmp.length(); i++) {
    cout << tmp[i] << endl;
  }
}
