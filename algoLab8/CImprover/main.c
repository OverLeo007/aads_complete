#include <stdio.h>
#include <stdlib.h>
#include "io_funcs.h"

#define SETT_COUNT 6137
#define MATRIX_FP "..\\dist_matrix.csv"
#define WAY_FP "..\\way.csv"
#define UPD_WAY_FP "best_way.csv"



double dist(double **matrix, int id1, int id2) {
    return matrix[id1][id2];
}


double get_path_len(double **matrix, int *way, int length) {
    double res = 0;
    for (int i = 0; i < length - 1; ++i) {
        res += dist(matrix, way[i], way[i + 1]);
    }
    return res / 100;
}


void swap(int *way, int idx_1, int idx_2) {
    int tmp = way[idx_1];
    way[idx_1] = way[idx_2];
    way[idx_2] = tmp;
}

void reverse(int *way, int idx_1, int idx_2) {
    while (idx_1 < idx_2) {
        swap(way, idx_1, idx_2);
        idx_1++;
        idx_2--;
    }

}


void opt2(double **matrix, int *way, int len, int max_iter) {
    int iter = 0;
    while (iter < max_iter) {
        int best_i = -1, best_j = -1;
        double best_gain = 0;
        for (int i = 0; i < len - 1; ++i) {
            for (int j = i + 1; j < len; ++j) {
                int from1 = way[i], to1 = way[(i + 1) % len];
                int from2 = way[j], to2 = way[(j + 1) % len];
                double gain =
                        (dist(matrix, from1, to1) +
                         dist(matrix, from2, to2))
                        - (dist(matrix, from1, from2) +
                        dist(matrix, to1, to2));
                if (gain > best_gain) {
                    best_i = i;
                    best_j = j;
                    best_gain = gain;
                }
            }

        }
        if (best_gain <= 0) {
            break;
        }
        reverse(way, best_i + 1, best_j);
        printf("%d/%d Укоротили на %lf\n", iter + 1, max_iter, best_gain);
        iter++;
    }
    printf("Найден за %d итераций\n", iter);
}



int main() {
    system("chcp 65001 > nul");

    double **matrix = read_csv(MATRIX_FP, SETT_COUNT);
    puts("Матрица считана!");

    int *way = read_way(WAY_FP, SETT_COUNT + 1);
    puts("Путь считан!");

    printf("Путь до улучшения: %lf\n",
           get_path_len(matrix, way, SETT_COUNT + 1));
    opt2(matrix, way, SETT_COUNT + 1, 1000);
    printf("Путь после улучшения: %lf\n",
           get_path_len(matrix, way, SETT_COUNT + 1));

    save_way(UPD_WAY_FP, way, SETT_COUNT + 1);

    for (int i = 0; i < SETT_COUNT; i++) {
        free(matrix[i]);
    }
    free(matrix);
    free(way);
    return 0;
}
