#include <cstdio>
#include <cstdlib>
#include "tools_eigen.h"

int main(int argc, char **argv) {
	int n = 0;
	double *matrix = NULL;

	// init variables from argc & argv
	if (argc == 3) {
		// fetch number of nodes
		if (!(n = atoi(argv[1]))) {
			printf("Nodes Should Be Number!\n");
			return -1;
		}

		// allocate memory for matrix
		matrix = new double[n * n];
		if (matrix == NULL) {
			printf("Failed to Allocate Memory for Matrix\n");
			return -2;
		}

		// init matrix from input file
		char *name = argv[2];
		FILE *in = fopen(name, "r");
		init_matrix_from_file(in, matrix, n);
		fclose(in);

	} else {
		printf("Usage:\n %s nodes file\n", argv[0]);
		return -1;
	}

	print_matrix(matrix, n, n);

	double *eignvalue = new double[n];
	qrAlmostUpperTriangle(matrix, n);
	double temp = traceMatrix(matrix, n);
	searchEigenValues(matrix, eignvalue, n);
	print_matrix(matrix, n , n);
	temp = traceMatrix(matrix, n);

	for (int i = 0; i < n; i++) {
		printf("Eignvalue %d : %.4lf\n", i, eignvalue[i]);
	}

	// collection garbage
	delete[] a;
	delete[] b;
	return 0;
}
