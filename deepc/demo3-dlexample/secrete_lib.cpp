#include <stdio.h>

int add (int a, int b) 
{
    printf("Its my secrete calc .... lol\n");
    return a + b + 5;
}

// g++ -shared -fPIC secrete_lib.cpp -o libsecrete.so