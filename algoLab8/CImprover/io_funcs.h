//
// Created by leva on 08.05.2023.
//

#ifndef CIMPROVER_IO_FUNCS_H
#define CIMPROVER_IO_FUNCS_H

double **read_csv(char *filepath, int n);

int *read_way(char *filepath, int len);

void save_way(char *filepath, int *way, int len);

#endif //CIMPROVER_IO_FUNCS_H
