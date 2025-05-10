// main.c
#include <stdio.h>
#include <dlfcn.h>

int main() {
    void *handle;
    int (*add)(int, int);
    char *error;

    // Load the shared library
    handle = dlopen("./libsecrete.so", RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "dlopen error: %s\n", dlerror());
        return 1;
    }

    // Clear any existing errors
    dlerror();

    // Get a pointer to the 'hello' function
    *(void **) (&add) = dlsym(handle, "_Z3addii");
    if ((error = dlerror()) != NULL) {
        fprintf(stderr, "dlsym error: %s\n", error);
        dlclose(handle);
        return 1;
    }

    // Call the function
    int res = add(10, 20);
    printf("res: %d\n", res);

    // Close the library
    dlclose(handle);
    return 0;
}