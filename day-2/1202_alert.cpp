#include<iostream>
#include<sstream>
#include<vector>

void handle_state_1(std::vector<int>& code, int start) {
  int fst_idx = code[start+1];
  int snd_idx = code[start+2];
  int res_idx = code[start+3];
  int res = code[fst_idx] + code[snd_idx];
  code[res_idx] = res;
}

void handle_state_2(std::vector<int>& code, int start) {
  int fst_idx = code[start+1];
  int snd_idx = code[start+2];
  int res_idx = code[start+3];
  int res = code[fst_idx] * code[snd_idx];
  code[res_idx] = res;
}

void execute_program(std::vector<int>& code) {
  for(int i = 0; i < code.size(); i += 4) {
    if(code[i] == 99) return;
    else if(code[i] == 1) handle_state_1(code, i);
    else if(code[i] == 2) handle_state_2(code, i);
  }
}

int main() {
  std::string num_as_str;
  std::vector<int> vec_org;
  while(std::getline(std::cin, num_as_str, ',')) {
    vec_org.push_back(std::stoi(num_as_str));
  }
  std::vector<int> vec(vec_org);
  for(int noun = 0; noun <= 99; noun++) {
    for(int verb = 0; verb <= 99; verb++) {
      vec = vec_org;
      vec[1] = noun;
      vec[2] = verb;
      execute_program(vec);
      if(vec[0] == 19690720) {
        std::cout << "noun: " << noun << std::endl;
        std::cout << "verb: " << verb << std::endl;
        return 1;
      }
    }
  }
}
