#include <vector>
#include <unordered_map>
#include <string>

#include <iostream>

using namespace std;

struct S {
public:
    S() {
        cout << "S constructor" << endl;
    }

    S(const S& s): docs(s.docs), ids(s.ids) {
        cout << "S copy constructor" << endl;
    }

    S(S&& s): docs(move(s.docs)), ids(move(s.ids)) {
        cout << "S move constructor" << endl;
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
    
    S s2;
    s2.docs.push_back("hello");
    s2.ids.push_back(12);

    S s3 = move(s2);
    cout << s3.ids.size() << endl;
}




