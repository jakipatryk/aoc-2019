#include<iostream>
#include<sstream>
#include<vector>
#include<utility>
#include<tuple>

std::pair<std::tuple<int, int, int>, int> extract_modes_and_instruction(int encoded) {
    int opt = (encoded % 100);
    int without_opt = encoded / 100;
    int fst = without_opt % 10;
    int snd = (without_opt / 10) % 10;
    int trd = (without_opt / 100) % 10;
    return std::make_pair(std::make_tuple(fst, snd, trd), opt);
}

void handle_state_1(std::vector<int>& code, int start, int m1, int m2) {
  int fst_idx = code[start+1];
  int snd_idx = code[start+2];
  int res_idx = code[start+3];
  int res = (m1 == 0 ? code[fst_idx] : fst_idx) + (m2 == 0 ? code[snd_idx] : snd_idx);
  code[res_idx] = res;
}

void handle_state_2(std::vector<int>& code, int start, int m1, int m2) {
  int fst_idx = code[start+1];
  int snd_idx = code[start+2];
  int res_idx = code[start+3];
  int res = (m1 == 0 ? code[fst_idx] : fst_idx) * (m2 == 0 ? code[snd_idx] : snd_idx);
  code[res_idx] = res;
}

void handle_state_3(std::vector<int>& code, int start, int m) {
  int write_to = m == 0 ? code[start+1] : start+1;
  // PSEUDO INPUT
  int in = 5;
  code[write_to] = in; 
}

void handle_state_4(std::vector<int>& code, int start, int m) {
  int read_from = m == 0 ? code[start+1] : start+1;
  std::cout << code[read_from] << std::endl;
}

int handle_state_5(std::vector<int>& code, int start, int m1, int m2) {
  int fst = m1 == 1 ? code[start+1] : code[code[start+1]];
  int snd = m2 == 1 ? code[start+2] : code[code[start+2]];
  if(fst == 0) {
    return start + 3;
  } else {
    return snd;
  }
}

int handle_state_6(std::vector<int>& code, int start, int m1, int m2) {
  int fst = m1 == 1 ? code[start+1] : code[code[start+1]];
  int snd = m2 == 1 ? code[start+2] : code[code[start+2]];
  if(fst != 0) {
    return start + 3;
  } else {
    return snd;
  }
}

void handle_state_7(std::vector<int>& code, int start, int m1, int m2, int m3) {
  int fst = m1 == 1 ? code[start+1] : code[code[start+1]];
  int snd = m2 == 1 ? code[start+2] : code[code[start+2]];
  int trd = m3 == 1 ? start+3 : code[start+3];
  if(fst < snd) {
    code[trd] = 1;
  } else {
    code[trd] = 0;
  }
}

void handle_state_8(std::vector<int>& code, int start, int m1, int m2, int m3) {
  int fst = m1 == 1 ? code[start+1] : code[code[start+1]];
  int snd = m2 == 1 ? code[start+2] : code[code[start+2]];
  int trd = m3 == 1 ? start+3 : code[start+3];
  if(fst == snd) {
    code[trd] = 1;
  } else {
    code[trd] = 0;
  }
}

void execute_program(std::vector<int>& code) {
  int i = 0;
  while(i < code.size()) {
    auto opt_and_modes = extract_modes_and_instruction(code[i]);
    auto opt = opt_and_modes.second;
    auto modes = opt_and_modes.first;
    switch (opt) {
      case 99:
        return;
      case 1:
        handle_state_1(code, i, std::get<0>(modes), std::get<1>(modes));
        i+=4;
        break;
      case 2:
        handle_state_2(code, i, std::get<0>(modes), std::get<1>(modes));
        i+=4;
        break;
      case 3:
        handle_state_3(code, i, std::get<0>(modes));
        i+=2;
        break;
      case 4:
        handle_state_4(code, i, std::get<0>(modes));
        i+=2;
        break;
      case 5:
        i = handle_state_5(code, i, std::get<0>(modes), std::get<1>(modes));
        break;
      case 6:
        i = handle_state_6(code, i, std::get<0>(modes), std::get<1>(modes));
        break;
      case 7:
        handle_state_7(code, i, std::get<0>(modes), std::get<1>(modes), std::get<2>(modes));
        i+=4;
        break;
      case 8:
        handle_state_8(code, i, std::get<0>(modes), std::get<1>(modes), std::get<2>(modes));
        i+=4;
        break;
    }
  }
}

int main() {
  std::string num_as_str;
  std::vector<int> code;
  while(std::getline(std::cin, num_as_str, ',')) {
    code.push_back(std::stoi(num_as_str));
  }
  execute_program(code);
}
