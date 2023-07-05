#include <iostream>
#include <vector>

int main() {
    std::vector<char> charList;

    // Adding upper case alphabet (A to Z)
    for (char ch = 'A'; ch <= 'Z'; ++ch) {
        charList.push_back(ch);
    }

    // Adding lower case alphabet (a to z)
    for (char ch = 'a'; ch <= 'z'; ++ch) {
        charList.push_back(ch);
    }

    // Adding characters 0 to 9
    for (char ch = '0'; ch <= '9'; ++ch) {
        charList.push_back(ch);
    }

    // Adding '+' and '|'
    charList.push_back('+');
    charList.push_back('|');

    // Display the generated list
    std::cout << "[";
    for (char ch : charList) {
        std::cout << "''" << ch << "'',";
    }
    std::cout << "]" << std::endl;

    return 0;
}
