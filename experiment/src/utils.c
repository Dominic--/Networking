#include "tools.h"

int init_matrix_with_file(char *filename, double **matrix, link_t **links, int *nodes_n, int *links_n, bool with_weight) {
	// check file if exist
	FILE *in = fopen(filename, "r");
  	if (!in) {
    	printf("No file\n");
    	return -1;
  	}

  	int res = fscanf(in, "%d %d", nodes_n, links_n);
	int n = *nodes_n, ln = *links_n;

	// check array which store the matrix if exist
	double *m = *matrix = (double *) malloc(n * n * sizeof(double));
	link_t *l = *links = (link_t *) malloc(ln * sizeof(link_t));
  	if (m == NULL) {
    	printf("No matrix\n");
    	return -2;
  	}

	// read value, save to matrix
	int s = 0, d = 0;
	double c = 0.0;
	for (int i = 0; i < ln; i++) {
		res = fscanf(in, "%d %d %lf", &s, &d, &c);
		if (!res) {
			printf("Failed to read from file!\n");
			return -1;
		} else {
			m[s * n + d] = with_weight ? -c : -1;
			m[d * n + s] = with_weight ? -c : -1;
			l[i].s = s;
			l[i].d = d;
			l[i].c = c;
			l[i].impact = 0;
		}
	}
  	
	fclose(in);

	// init diagonal elements with :
	// 		d(ii) = sum a(ij)
	for (int i = 0; i < n; i++) {
		double num = 0;
		for (int j = 0; j < n; j++) {
			num += m[i * n + j];
		}
		m[i * n + i] = -num;
	}

	return 0;
}


void print_matrix(double * const matrix, int nodes_n) {
	for (int i = 0; i < nodes_n; i++) { 
		for (int j = 0; j < nodes_n; j++) { 
			printf("%9.1lf", matrix[i * nodes_n + j]);
		} 
		printf("\n ");
	}
}
