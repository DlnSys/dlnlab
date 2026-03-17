//gcc -Wall -Wextra -z execstack execut0r.c -o execut0r
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>

#define LEN 1024

int main (int argc, char **argv) {
	if (argc != 2) {
		printf("Usage: %s <shellcode_file>\n", argv[0]);
		exit(1);
	}
	uint8_t *sc = mmap(NULL, LEN, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (sc == MAP_FAILED) {
        fprintf(stderr, "Error: mmap failed.");
        return 2;
    }

	FILE *fp = fopen(argv[1], "r");
	fread(sc, LEN, 1, fp);
	fclose(fp);

    /* Now make it execute-only */
    if (mprotect(sc, LEN, PROT_EXEC) < 0) {
        fprintf(stderr, "Error: mprotect failed.");
        return 2;
    }

	((void (*) (void)) sc) ();

	return EXIT_SUCCESS;
}
