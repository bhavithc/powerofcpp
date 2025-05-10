#include <iostream>

int main(int argc, char** pArgv, char** pEnv) {
    
    char** pTmp = pEnv;

    while (*pTmp != nullptr) {
        std::cout << *pTmp << "\n";
        pTmp++;
    }
    
    std::cout << "End of the list \n";
    return 0;
}