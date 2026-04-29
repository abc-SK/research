#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//結果を手で確認できるようにする
//グラフをランダムで生成できるようにする
#define N 10
#define TRIALS 100

void shuffle(int order[], int n) {
    // 配列の順番をランダムに並び替えるランダム性がない？
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);

        int temp = order[i];
        order[i] = order[j];
        order[j] = temp;
    }
}

int greedy_coloring(int adj[N][N], int order[]) {
    // color[v] は「頂点 v に塗った色」
    int color[N];

    // 最初は全部未彩色(0)
    for (int i = 0; i < N; i++) {
        color[i] = 0;
    }

    // 使った色の最大値
    int max_color = 0;

    // 順番に頂点を塗る
    for (int i = 0; i < N; i++) {
        int v = order[i];

        // used[c] = 1 なら「色 c は使えない」
        // used[c] = 0 なら「色 c は使える」
        int used[N + 1];

        // 最初は全部「使える」
        for (int j = 0; j <= N; j++) {
            used[j] = 0;
        }

        // 隣接していて、すでに色がついている頂点の色を調べる
        for (int u = 0; u < N; u++) {
            if (adj[v][u] == 1 && color[u] != 0) {
                used[color[u]] = 1;
            }
        }

        // 使える最小の色を探す
        int c = 1;
        while (used[c] == 1) {
            c++;
        }

        // 頂点 v に色 c を塗る
        color[v] = c;

        // 最大色を更新
        if (c > max_color) {
            max_color = c;
        }
    }

    return max_color;
}

void print_edges(int adj[N][N]) {
    printf("Edges:\n");
    for (int i = 0; i < N; i++) {
        for (int j = i + 1; j < N; j++) {
            if (adj[i][j] == 1) {
                printf("(%d, %d) ", i, j);
            }
        }
    }
    printf("\n\n");
}

void print_adj_matrix(int adj[N][N]) {
    printf("Adjacency matrix:\n");

    // 列番号を表示
    printf("   ");
    for (int j = 0; j < N; j++) {
        printf("%d ", j);
    }
    printf("\n");

    // 各行を表示
    for (int i = 0; i < N; i++) {
        printf("%d: ", i);
        for (int j = 0; j < N; j++) {
            printf("%d ", adj[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int main(void) {
    // 隣接行列
    int adj[N][N] = {0};

    // グラフを作る
    adj[0][1] = adj[1][0] = 1;
    adj[0][2] = adj[2][0] = 1;
    adj[1][2] = adj[2][1] = 1;
    adj[1][3] = adj[3][1] = 1;
    adj[2][4] = adj[4][2] = 1;
    adj[3][4] = adj[4][3] = 1;
    adj[3][5] = adj[5][3] = 1;
    adj[4][6] = adj[6][4] = 1;
    adj[5][6] = adj[6][5] = 1;
    adj[5][7] = adj[7][5] = 1;
    adj[6][8] = adj[8][6] = 1;
    adj[7][8] = adj[8][7] = 1;
    adj[7][9] = adj[9][7] = 1;
    adj[8][9] = adj[9][8] = 1;

    print_edges(adj);

    // 各試行の結果を保存
    int results[TRIALS];

    // 頂点順を入れる配列
    int order[N];

    // 乱数の初期化
    srand((unsigned)time(NULL));

    // 100回繰り返す
    for (int t = 0; t < TRIALS; t++) {
        // order を 0,1,2,...,9 にする
        for (int i = 0; i < N; i++) {
            order[i] = i;
        }

        // 順番をランダムに並び替える
        shuffle(order, N);

        // 貪欲彩色して、使った色数を保存
        results[t] = greedy_coloring(adj, order);
    }

    // 最小値・最大値・合計を求める
    int min = results[0];
    int max = results[0];
    int sum = 0;

    printf("Color counts:\n");

for (int t = 0; t < TRIALS; t++) {
    printf("%d ", results[t]);

    if ((t + 1) % 20 == 0) {
 
        printf("\n");
    }

    if (results[t] < min) {
        min = results[t];
    }

    if (results[t] > max) {
        max = results[t];
    }

    sum += results[t];
}

printf("\nMinimum colors: %d\n", min);
printf("Maximum colors: %d\n", max);
printf("Average colors: %.2f\n", (double)sum / TRIALS);
    return 0;
}