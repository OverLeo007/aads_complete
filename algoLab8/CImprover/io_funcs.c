#include <stdio.h>
#include <stdlib.h>
#include <string.h>


double **read_csv(char *filepath, int n) {
    double **matrix = (double **) malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        matrix[i] = (double *) malloc(n * sizeof(double));
    }

    FILE *file = fopen(filepath, "r");
    if (file == NULL) {
        printf("Не удалось открыть файл\n");
        return NULL;
    }

    char buffer[61360];
    int row = 0;
    while (fgets(buffer, sizeof(buffer), file)) {
        int col = 0;
        char *token = strtok(buffer, "|");
        while (token != NULL && col < n) {
            sscanf(token, "%lf", &matrix[row][col]);
            token = strtok(NULL, "|");
            col++;
        }
        row++;

    }
    fclose(file);
    return matrix;
}

int *read_way(char *filepath, int len) {
    int *way = malloc(len * sizeof(int));
    FILE *file = fopen(filepath, "r");
    if (!file) {
        printf("Не удалось открыть файл\n");
        return NULL;
    }

    int num;
    for (int i = 0; i < len; ++i) {
        fscanf(file, "%d", &num);
        way[i] = num;

    }
    fclose(file);
    return way;
}

void save_way(char *filepath, int *way, int len) {
    FILE *file = fopen(filepath, "w");
    for (int i = 0; i < len; ++i) {
        fprintf(file, "%d\n", way[i]);
    }
    fclose(file);
}