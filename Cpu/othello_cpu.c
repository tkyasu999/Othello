#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SIZE (8)

// 石の色を表す列挙型
typedef enum color {
    empty,
    black,
    white
} COLOR;

// 文字を整数に変換する関数
int ctoi(char c) {
	if (c >= '0' && c <= '9') {
		return c - '0';
	}
	return 0;
}

// 盤面を初期化する関数
void init(COLOR board[SIZE][SIZE], const char* buf) {
    // 盤面の初期化
    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE; x++) {
            board[y][x] = ctoi(buf[y * SIZE + x]);
        }
    }
}

// 指定された位置が盤面内かどうかを判定する関数
int isValidPosition(int x, int y) {
    return (x >= 0 && x < SIZE && y >= 0 && y < SIZE);
}

// 指定された位置に石を置けるかどうかを判定し、石をひっくり返す関数
int flipStones(int x, int y, COLOR myturn, COLOR board[SIZE][SIZE]) {
    // 8方向の移動量
    int dx[] = {-1, 0, 1, -1, 1, -1, 0, 1};
    int dy[] = {-1, -1, -1, 0, 0, 1, 1, 1};

    COLOR other = (myturn == white) ? black : white;
    int totalFlips = 0;

    for (int dir = 0; dir < SIZE; dir++) {
        int nx = x + dx[dir];
        int ny = y + dy[dir];
        int count = 0;

        // ひっくり返せる石があるかどうかを確認
        while (isValidPosition(nx, ny) && board[ny][nx] == other) {
            nx += dx[dir];
            ny += dy[dir];
            count++;
        }

        // 自分の石で挟める場合、ひっくり返す
        if (isValidPosition(nx, ny) && board[ny][nx] == myturn && count > 0) {
            totalFlips += count;
        }
    }

    return totalFlips;
}

// 指定された位置に石を置けるかどうかを判定
int isValidMove(int x, int y, COLOR board[SIZE][SIZE], COLOR myturn) {
    if (!isValidPosition(x, y) || board[y][x] != empty) {
        return 0; // 位置が盤面外または既に石がある場合は無効
    }

    // 指定された位置に石を置けるかどうかを判定
    return flipStones(x, y, myturn, board) > 0;
}

// ランダムに手を選ぶCPUプレイヤー
void cpuRandomMove(COLOR board[SIZE][SIZE], COLOR myturn) {
    int x, y;
    int attempts = 0;

    do {
        x = rand() % SIZE;
        y = rand() % SIZE;
        attempts++;
    } while (!isValidMove(x, y, board, myturn) && attempts < 100);

    if(attempts == 100) {
        printf("pass\n");
    } else {
        printf("%d,%d\n", x, y);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s -b|-w <board>\n", argv[0]);
        return EXIT_FAILURE;
    }

    COLOR board[SIZE][SIZE];
    COLOR myturn;

    // 黒白の入力
    if(strcmp(argv[1], "-b") == 0) {
        myturn = black;
    } else if(strcmp(argv[1], "-w") == 0) {
        myturn = white;
    } else {
        fprintf(stderr, "Invalid turn option. Use -b for black or -w for white.\n");
        return EXIT_FAILURE;
    }

    // 盤面の初期化
    init(board, argv[2]);
    srand(time(NULL)); // 乱数の初期化

    // CPUプレイヤーの手を選択
    cpuRandomMove(board, myturn);

    return EXIT_SUCCESS;
}
