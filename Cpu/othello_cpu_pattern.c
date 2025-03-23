#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SIZE (8)
#define MAX_PATTERNS (100)
#define MAX_LINE_LENGTH (100)

// 石の色を表す列挙型
typedef enum color {
    empty,
    black,
    white
} COLOR;

// 勝ちパターンを表す構造体
typedef struct {
    COLOR board[SIZE][SIZE];
    int bestX;
    int bestY;
} Pattern;

// 勝ちパターンのリスト
Pattern patterns[MAX_PATTERNS];
int patternCount = 0;

// 文字を整数に変換する関数
int ctoi(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    }
    return -1;
}

// 盤面を初期化する関数
void init(COLOR board[SIZE][SIZE], const char* buf) {
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

// 指定された位置に石を置けるかどうかを判定する関数
int isValidMove(int x, int y, COLOR board[SIZE][SIZE], COLOR myturn) {
    if (!isValidPosition(x, y) || board[y][x] != empty) {
        return 0; // 位置が盤面外または既に石がある場合は無効
    }

    return 1;
}

// 評価関数
int evaluatePosition(int x, int y) {
    // 角の位置は高評価
    if ((x == 0 || x == SIZE - 1) && (y == 0 || y == SIZE - 1)) {
        return 100;
    }
    // X-square (角の斜め隣接位置) は低評価
    if ((x == 1 || x == SIZE - 2) && (y == 1 || y == SIZE - 2)) {
        return -50;
    }
    // C-square (角の隣接位置) は低評価
    if ((x == 0 || x == SIZE - 1) && (y == 1 || y == SIZE - 2)) {
        return -50;
    }
    if ((x == 1 || x == SIZE - 2) && (y == 0 || y == SIZE - 1)) {
        return -50;
    }
    // 辺の位置は中評価
    if (x == 0 || x == SIZE - 1 || y == 0 || y == SIZE - 1) {
        return 10;
    }
    // その他の位置は低評価
    return 1;
}

// 盤面がパターンと一致するかどうかを判定する関数
int matchPattern(COLOR board[SIZE][SIZE], Pattern pattern) {
    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE; x++) {
            if (board[y][x] != pattern.board[y][x]) {
                return 0;
            }
        }
    }
    return 1;
}

// ひっくり返せる石の数と位置の評価を考慮して最適な手を選ぶCPUプレイヤー
void cpuBestMove(COLOR board[SIZE][SIZE], COLOR myturn) {
    int bestX = -1, bestY = -1;
    int maxScore = -100;

    // パターンマッチングによる最適な手の選択
    for (int i = 0; i < patternCount; i++) {
        if (matchPattern(board, patterns[i])) {
            bestX = patterns[i].bestX;
            bestY = patterns[i].bestY;
            printf("%d,%d\n", bestX, bestY);
            return;
        }
    }

    // 通常の評価関数による最適な手の選択
    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE; x++) {
            if (isValidMove(x, y, board, myturn)) {
                int flips = flipStones(x, y, myturn, board);
                if(flips > 0) {
                    int score = flips + evaluatePosition(x, y);
                    if (score > maxScore) {
                        maxScore = score;
                        bestX = x;
                        bestY = y;
                    }
                }
            }
        }
    }

    if (bestX == -1 || bestY == -1) {
        printf("pass\n");
    } else {
        printf("%d,%d\n", bestX, bestY);
    }
}

// 勝ちパターンを追加する関数
void addPattern(const char* buf, int x, int y) {
    if (patternCount < MAX_PATTERNS) {
        // 盤面を初期化
        COLOR board[SIZE][SIZE];
        init(board, buf);

        // 現在の盤面をパターンとして保存
        memcpy(patterns[patternCount].board, board, sizeof(COLOR) * SIZE * SIZE);
        // 最適な手を保存
        patterns[patternCount].bestX = x;
        patterns[patternCount].bestY = y;
        // パターンの数を増やす
        patternCount++;
    }
}

// テキストファイルから勝ちパターンを読み込む関数
void loadPatternsFromFile(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        perror("Failed to open pattern file");
        return;
    }

    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), file)) {
        char buf[SIZE * SIZE + 1];
        int x, y;
        if (sscanf(line, "%64s %d %d", buf, &x, &y) == 3) {
            addPattern(buf, x, y);
        }
    }

    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s -b|-w <board> <pattern_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    COLOR board[SIZE][SIZE];
    COLOR myturn;

    // 黒白の入力
    if (strcmp(argv[1], "-b") == 0) {
        myturn = black;
    } else if (strcmp(argv[1], "-w") == 0) {
        myturn = white;
    } else {
        fprintf(stderr, "Invalid turn option. Use -b for black or -w for white.\n");
        return EXIT_FAILURE;
    }

    // 盤面の初期化
    init(board, argv[2]);

    // 勝ちパターンのファイルからの読み込み
    loadPatternsFromFile(argv[3]);

    // CPUプレイヤーの手を選択
    cpuBestMove(board, myturn);

    return EXIT_SUCCESS;
}