#include "tools.h"

int init_matrix_with_file(double **matrix, int *node) {
	// check file if exist
	FILE *in = fopen("matrix", "r");
  	if (!in) {
    	printf("No file\n");
    	return -1;
  	}

  	int res = fscanf(in, "%d", node);
	int n = *node;

	// check array which store the matrix if exist
	double *m = *matrix = (double *) malloc(n * n * sizeof(double));
  	if (m == NULL) {
    	printf("No matrix\n");
    	return -2;
  	}

	// read value, save to matrix
  	for (int i = 0; i < n; i++) {
    	for (int j = 0; j < n; j++) {
			// address of matrix[i][j] = matrix + i * n + j
      		res = fscanf(in, "%lf", m + i * n + j);
      		if (!res) {
				printf("Failed to read from file!\n");
				return -3;
      		}
    	}
  	}
  	
	fclose(in);
	return 0;
}


void print_matrix(double * const matrix, int height, int width) {
	for (int i = 0; i < height; i++) { 
		for (int j = 0; j < width; j++) { 
			printf("%6.2lf", matrix[i * width + j]);
		} 
		printf("\n ");
	}
}
