#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SIZE (8)

typedef enum color {
    empty,
    black,
    white
} COLOR;

int ctoi(char c) {
	if (c >= '0' && c <= '9') {
		return c - '0';
	}
	return 0;
}

// 盤を入力
void init(COLOR board[SIZE][SIZE], char* buf) {
    int x, y;

    // 盤面の初期化
    for (y = 0; y < SIZE; y++) {
        for (x = 0; x < SIZE; x++) {
            board[y][x] = ctoi(buf[y * 8 + x]);
        }
    }
}

int main(int argc, char *argv[]) {
    COLOR board[SIZE][SIZE];

    // 黒白の入力
    COLOR myturn;
    if(!strcmp(argv[1], "-b")) {
        myturn = 1;
    }
    if(!strcmp(argv[1], "-w")) {
        myturn = 2;
    }

    // 盤面の初期化などのコードを追加
    init(board, argv[2]);

    return 0;
}
