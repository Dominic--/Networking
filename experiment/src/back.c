#include "tools.h"

int main(int argc, char **argv) {
	int node = 0;
	double *matrix = NULL;
	init_matrix_with_file(&matrix, &node);

	double second = get_eigenvalue(matrix, node);
	printf("%.4lf\n", second);

	free(matrix);
	return 0;
}

