#include<iostream>
#include<sstream>
#include<vector>
#include<utility>
#include<tuple>
#include<unordered_map>
#include<string>

class IntcodeComputer {
    private:
        std::vector<long long> code;
        int relative_base;
        int current_position;

        void write_to_memory(int position, long long what) {
            if(position >= code.size()) {
              code.resize(position+1);
            }
            code[position] = what;
        }

        long long get_value(long long mode, int position) const {
            if(mode == 0) {
                return code[code[position]];
            } else if(mode == 1) {
                return code[position];
            } else {
              return code[relative_base + code[position]];
            }
        }

        std::pair<std::tuple<long long, long long, long long>, long long>
          extract_modes_and_instruction(long long encoded) const {
            long long opt = (encoded % 100);
            long long without_opt = encoded / 100;
            long long fst = without_opt % 10;
            long long snd = (without_opt / 10) % 10;
            long long trd = (without_opt / 100) % 10;
            return std::make_pair(std::make_tuple(fst, snd, trd), opt);
        }

        void handle_arithmetic(char op, long long mode_1, long long mode_2, long long mode_3) {
            long long res_idx = mode_3 == 0 ? code[current_position+3] : relative_base + code[current_position+3];
            long long fst = get_value(mode_1, current_position+1);
            long long snd = get_value(mode_2, current_position+2);
            write_to_memory(res_idx, op == '+' ? fst + snd : fst * snd);
            current_position += 4;
        }

        void handle_input(long long mode, long long input = 0) {
            long long write_to = mode == 0 ? code[current_position+1] : relative_base + code[current_position+1];
            write_to_memory(write_to, input); 
            current_position += 2;
        }

        long long handle_output(long long mode) {
            long long output = get_value(mode, current_position+1);
            current_position += 2;
            return output;
        }

        void handle_conditional_goto(long long mode_1, long long mode_2, bool jump_when_zero = true) {
          long long fst = get_value(mode_1, current_position+1);
          long long snd = get_value(mode_2, current_position+2);
          if(jump_when_zero ? (fst == 0) : (fst != 0)) {
            current_position += 3;
          } else {
            current_position = snd;
          }
        }

        void handle_ordering_check(long long mode_1, long long mode_2, long long mode_3, bool equality_checking = false) {
            long long fst = get_value(mode_1, current_position+1);
            long long snd = get_value(mode_2, current_position+2);
            long long trd = mode_3 == 0 ? code[current_position+3] : relative_base + code[current_position+3];
            if(equality_checking ? (fst == snd) : (fst < snd)) {
              write_to_memory(trd, 1);
            } else {
              write_to_memory(trd, 0);
            }
            current_position += 4;
        }

        void handle_base_adjustment(long long mode) {
            relative_base += get_value(mode, current_position+1);
            current_position += 2;
        }

    public:
        IntcodeComputer() : current_position(0), relative_base(0) {}

        IntcodeComputer(const std::vector<long long>& _code) : current_position(0), relative_base(0) {
            code = _code;
        } 
        
        std::tuple<int, int, int> execute(int input) {
            int output_nr = 0;
            int fst = -1;
            int snd = 01;
            while(current_position < code.size()) {
                auto opt_and_modes = extract_modes_and_instruction(code[current_position]);
                auto opt = opt_and_modes.second;
                auto modes = opt_and_modes.first;
                switch (opt) {
                  case 99:
                    return std::make_tuple(-1, -1, -1);
                  case 1:
                    handle_arithmetic('+', std::get<0>(modes), std::get<1>(modes), std::get<2>(modes));
                    break;
                  case 2:
                    handle_arithmetic('*', std::get<0>(modes), std::get<1>(modes), std::get<2>(modes));
                    break;
                  case 3:
                    handle_input(std::get<0>(modes), input);
                    break;
                  case 4:
                    if(output_nr == 0) {
                      fst = handle_output(std::get<0>(modes));
                      output_nr++;
                    } else if(output_nr == 1) {
                      snd = handle_output(std::get<0>(modes));
                      output_nr++;
                    } else {
                      return std::make_tuple(fst, snd, handle_output(std::get<0>(modes)));
                    }
                    break;
                  case 5:
                    handle_conditional_goto(std::get<0>(modes), std::get<1>(modes));
                    break;
                  case 6:
                    handle_conditional_goto(std::get<0>(modes), std::get<1>(modes), false);
                    break;
                  case 7:
                    handle_ordering_check(std::get<0>(modes), std::get<1>(modes), std::get<2>(modes));
                    break;
                  case 8:
                    handle_ordering_check(std::get<0>(modes), std::get<1>(modes), std::get<2>(modes), true);
                    break;
                  case 9:
                    handle_base_adjustment(std::get<0>(modes));
                    break;
                }
            }
            return std::make_tuple(-1, -1, -1);
        }
};

int main() {
  std::string num_as_str;
  std::vector<long long> code;
  while(std::getline(std::cin, num_as_str, ',')) {
    code.push_back(std::stoll(num_as_str));
  }

  IntcodeComputer computer(code);

  int input = 0;
  int result = 0;
  int paddle_x = 0;
  int ball_x = 0;
  while(true) {
      auto triple = computer.execute(input);
      int x = std::get<0>(triple);
      int y = std::get<1>(triple);
      int id = std::get<2>(triple);
      if(x == -1 && y == -1 && id == -1) {
          break;
      } else if(x == -1 && y == 0) {
          result = id;
      } else if(id == 3) {
          paddle_x = x;
      } else if(id == 4) {
          ball_x = x;
      }
      input = (paddle_x < ball_x) - (paddle_x > ball_x);
  }
  std::cout << "RESULT: " << result << std::endl;
}