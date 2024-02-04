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

// 指定された位置が盤面内かどうかを判定
int isValidPosition(int x, int y) {
    return (x >= 0 && x < SIZE && y >= 0 && y < SIZE);
}

// 指定された位置に石を置けるかどうかを判定
int flipStones(int x, int y, COLOR myturn, COLOR board[SIZE][SIZE]) {
    // 8方向の移動量
    int dx[] = {-1, 0, 1, -1, 1, -1, 0, 1};
    int dy[] = {-1, -1, -1, 0, 0, 1, 1, 1};

    COLOR other;
    
    if(myturn == white) {
        other = black;
    } else {
        other = white;
    }

    for (int dir = 0; dir < 8; dir++) {
        int nx = x + dx[dir];
        int ny = y + dy[dir];
        int count = 0;

        if (isValidPosition(nx, ny) && board[ny][nx] != empty) {
            if(board[ny][nx] != other) {
                continue;
            }
            nx += dx[dir];
            ny += dy[dir];
            count++;

            while (isValidPosition(nx, ny)) {
                if (board[ny][nx] == empty) {
                    break;
                }

                if (board[ny][nx] == myturn) {
                    count = 0;
                    break;
                }

                if (board[ny][nx] == other) {
                    count++;
                    nx += dx[dir];
                    ny += dy[dir];
                }
            }

            if(isValidPosition(nx, ny) && count) {
                printf("%d,%d\n", nx, ny);
                return count;
            }
        }
    }

    return 0;
}

// 指定された位置に石を置けるかどうかを判定
int isValidMove(int x, int y, COLOR board[SIZE][SIZE], COLOR myturn) {
    if (!isValidPosition(x, y) || board[y][x] != myturn) {
        return 0; // 位置が盤面外または既に石がある場合は無効
    }

    // 指定された位置に石を置けるかどうかを判定
    if(!flipStones(x, y, myturn, board)) {
        return 0;
    }

    return 1;
}

// ランダムに手を選ぶCPUプレイヤー
void cpuRandomMove(COLOR board[SIZE][SIZE], COLOR myturn) {
    int x, y;
    int z = 0;
    do {
        x = rand() % SIZE;
        y = rand() % SIZE;
        z++;
    } while (!isValidMove(x, y, board, myturn) && z < 100);

    if(z == 100) {
        printf("pass\n");
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
    srand(time(NULL)); // 乱数の初期化

    // CPUプレイヤーの手を選択
    cpuRandomMove(board, myturn);

    return 0;
}
