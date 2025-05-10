#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp;
    char path[1035];

    fp = popen("ls -l", "r");
    if (fp == NULL) {
        perror("Failed to run command");
        exit(1);
    }

    while (fgets(path, sizeof(path), fp) != NULL) {
        printf("%s", path);
    }

    if (pclose(fp) == -1) {
        perror("Error closing pipe");
        return 1;
    }
    return 0;
}
