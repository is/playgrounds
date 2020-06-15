#include <vector>
#include <unordered_map>
#include <string>

#include <iostream>

using namespace std;

struct S {
public:
    S() {
        cout << "S constuctor" << endl;
    }
    
    std::vector<string> docs;
    std::vector<int32_t> ids;
};


int main(void) {
    unordered_map<int32_t, S> idMap;

    cout << "hello world" << endl;

    S s0;
    s0.docs.push_back("hello");
    s0.ids.push_back(12);
    idMap[12] = std::move(s0);

    cout << idMap[12].ids.at(0) << endl;
}




