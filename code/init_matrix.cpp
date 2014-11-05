#include <cstdio>
#include <cstdlib>

void init_matrix_with_debug(double *matrix, int n) {
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
      		if (abs(i - j) == 0) {
				matrix[i * n + j] = 1;

			} else if (abs(i - j) == 1) {
				matrix[i * n + j] = 2;

			} else {
				matrix[i * n + j] = 0;
			}
    	}
  	}
}

int init_matrix_with_file(FILE* in, double* matrix, int n) {
	// check file if exist
  	if (!in) {
    	printf("No file\n");
    	return -1;
  	}

	// check array which store the matrix if exist
  	if (matrix == NULL) {
    	printf("No matrix\n");
    	return -2;
  	}

	// read value, save to matrix
  	int res = 0;
  	for (int i = 0; i < n; i++) {
    	for (int j = 0; j < n; j++) {
			// address of matrix[i][j] = matrix + i * n + j
      		res = fscanf(in, "%lf", matrix + i * n + j);
      		if (!res) {
				printf("Failed to read from file!\n");
				return -3;
      		}
    	}
  	}
  	
	return 0;
}
