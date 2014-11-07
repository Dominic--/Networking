#include <cstdio>

/*
 * Init matrix from file :
 * 		first line means number of nodes;
 *     	from 2nd line to N+1 line means graph matrix;
 *
 *     	for example : 
 *
 * 		3
 * 		1 2 3
 * 		3 4 4
 * 		5 4 2
 *
 */
int init_matrix_with_file(double **, int *);

/*
 * Print matrix for debug
 */
void print_matrix(double *, int, int);

/*
 * Get the second smallest eigenvalue
 */
double get_eigenvalue(double *, int);

