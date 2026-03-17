// gcc -O3 tiktaktok.c -o tiktaktok -pie -Wl,-z,relro,-z,now -fno-stack-protector -Wl,-z,noexecstack
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

typedef struct game {
	int8_t board[3][3];
	uint32_t nbMoves;
	uint8_t name[32];
} game_t;

char c;

void printBoard(const game_t g) {
	printf("            j=0   j=1   j=2  \n");
	printf("             |     |     |   \n");
	printf("             v     v     v   \n");
	printf("          +-----+-----+-----+\n");
	for (int i = 0; i < 3; ++i) {
		printf("          |     |     |     |\n");
		printf(" i = %d -> |", i);
		for (int j = 0; j < 3; ++j) {
			if      ((g.board[i][j] % 2) ==  1) printf("  X  |");
			else if ((g.board[i][j] % 2) ==  0) printf("  O  |");
			else if ((g.board[i][j]    ) == -1) printf("     |");
		}
		printf("\n");
		printf("          |     |     |     |\n");
		printf("          +-----+-----+-----+\n");
	}
	printf("\n");
	printf("\n");
}

int8_t isFull(const game_t g) {
	int8_t nbEmtpy = 0;
	for (int i = 0; i < 3; ++i) {
		for (int j = 0; j < 3; ++j) {
			if (g.board[i][j] == -1) {
				nbEmtpy++;
			}
		}
	}
	return nbEmtpy == 0;
}

int8_t hasWinner(const game_t g) {

	if        ( (g.board[0][0] != -1) && ((g.board[0][0]%2) == (g.board[0][1]%2)) && ((g.board[0][0]%2) == (g.board[0][2]%2)) ) { /* Row 0 */
		return g.board[0][0];

	} else if ( (g.board[1][0] != -1) && ((g.board[1][0]%2) == (g.board[1][1]%2)) && ((g.board[1][0]%2) == (g.board[1][2]%2)) ) { /* Row 1 */
		return g.board[1][0];

	} else if ( (g.board[2][0] != -1) && ((g.board[2][0]%2) == (g.board[2][1]%2)) && ((g.board[2][0]%2) == (g.board[2][2]%2)) ) { /* Row 2 */
		return g.board[2][0];

	} else if ( (g.board[0][0] != -1) && ((g.board[0][0]%2) == (g.board[1][0]%2)) && ((g.board[0][0]%2) == (g.board[2][0]%2)) ) { /* Column 0 */
		return g.board[0][0];

	} else if ( (g.board[0][1] != -1) && ((g.board[0][1]%2) == (g.board[1][1]%2)) && ((g.board[0][1]%2) == (g.board[2][1]%2)) ) { /* Column 1 */
		return g.board[0][1];

	} else if ( (g.board[0][2] != -1) && ((g.board[0][2]%2) == (g.board[1][2]%2)) && ((g.board[0][2]%2) == (g.board[2][2]%2)) ) { /* Column 2 */
		return g.board[0][2];

	} else if ( (g.board[0][0] != -1) && ((g.board[0][0]%2) == (g.board[1][1]%2)) && ((g.board[0][0]%2) == (g.board[2][2]%2)) ) { /* Diagonal */
		return g.board[0][0];

	} else if ( (g.board[0][2] != -1) && ((g.board[0][2]%2) == (g.board[1][1]%2)) && ((g.board[0][2]%2) == (g.board[2][0]%2)) ) { /* Anti diagonal */
		return g.board[0][2];

	} else {
		return -1;

	}
}

int main() {

	game_t g;
	int8_t player;
	int8_t user;
	int8_t computer;
	int8_t winner;
	int8_t full;
	uint64_t i;
	uint64_t j;

	/* No buffering */
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	/* Initialization */
	srand(getpid());

	/* Get username */
	printf("Hello Player! Welcome to the Tik-Tak-Tok Game Server!\n");
	printf("What is your player name?\n");
	printf(">>> ");

	(void)read(0, g.name, 32);
	g.name[strcspn((char *)g.name, "\n")] = 0;

	printf("Note: to play a move, enter the position, for instance: 0 0\n");

	g.nbMoves = 0;
	do { /* Create new games */

		memset(g.board, -1, sizeof(g.board));

		/* The user plays first */
		user = 1 ^ (g.nbMoves & 1);
		computer = 1 ^ user;
		player = user;

		do { /* One game */

			/* The user is playing */
			if (player) {

				/* Gets position (i, j) */
				printBoard(g);
				printf("\n");
				printf("%s to play.\n", g.name);
				printf(">>> ");
				scanf("%ld %ld", &i, &j);

				g.board[i][j] = g.nbMoves;
				player ^= 1;

			/* Computer to play: random move */
			} else {

				/* Get a random cell empty */
				do {
					i = rand() % 3;
					j = rand() % 3;
				} while(g.board[i][j] != -1);

				/* Play (i, j) */
				g.board[i][j] = g.nbMoves;
				player ^= 1;
			}

			g.nbMoves++;
			winner = hasWinner(g);
			full = isFull(g);

		} while( (winner == -1) && !full );

		printBoard(g);

		if (winner == -1) {
			printf("This is a draw.\n");
		} else {
			if ( (winner ^ computer) & 1) {
				printf("Congratulations, you won the game!\n");
			} else {
				printf("The random computer has won the game!\n");
			}
		}

		printf("Do you want to play again? [y/n]\n");
		printf(">>> ");
		do {
			c = getchar();
		} while(!((c == 'y') || (c == 'n')));

		(void)getchar();

	} while(c == 'y');

	printf("Bye bye.\n");

	return 0;
}
