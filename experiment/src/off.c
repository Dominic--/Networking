#include "tools.h"


//
//
// ./off threshold input_topology output_topology
//
//
int main(int argc, char **argv) {
	// init matrix
	int nodes_n = 0, links_n = 0;
	double * matrix = NULL;
	link_t * links = NULL;
	bool with_weight = false;
	init_matrix_with_file(argv[2], &matrix, &links, &nodes_n, &links_n, with_weight);

	// 
	double * copy_matrix = (double *) malloc(nodes_n * nodes_n * sizeof(double));
	memcpy(copy_matrix, matrix, nodes_n * nodes_n * sizeof(double));
	double origin = get_eigenvalue(copy_matrix, nodes_n);
	free(copy_matrix);

	for (int i = 0; i < links_n; i++) {
		double backup = matrix[links[i].s * nodes_n + links[i].d];

		matrix[links[i].s * nodes_n + links[i].d] = 0;
		matrix[links[i].d * nodes_n + links[i].s] = 0;
		matrix[links[i].s * nodes_n + links[i].s] += backup;
		matrix[links[i].d * nodes_n + links[i].d] += backup;
		
		double * copy_matrix = (double *) malloc(nodes_n * nodes_n * sizeof(double));
		memcpy(copy_matrix, matrix, nodes_n * nodes_n * sizeof(double));
		double temp_connected_value = get_eigenvalue(copy_matrix, nodes_n);
		links[i].impact = origin - temp_connected_value;
		free(copy_matrix);

		matrix[links[i].s * nodes_n + links[i].d] = backup;
		matrix[links[i].d * nodes_n + links[i].s] = backup;
		matrix[links[i].s * nodes_n + links[i].s] -= backup;
		matrix[links[i].d * nodes_n + links[i].d] -= backup;
	}

	for (int i = 0; i < links_n; i++) {
		for (int j = i + 1; j < links_n; j++) {
			if (links[i].impact > links[j].impact) {
				int s = links[i].s, d = links[i].d;
				double impact = links[i].impact, c = links[i].c;

				links[i].s = links[j].s;
				links[i].d = links[j].d;
				links[i].c = links[j].c;
				links[i].impact = links[j].impact;

				links[j].s = s;
				links[j].d = d;
				links[j].c = c;
				links[j].impact = impact;
			}
		}
	}

	/*
	for (int i = 0; i < links_n; i++) {
		printf("Link %d : (%d, %d) --> %lf\n", i, links[i].s, links[i].d, links[i].impact);
	}
	*/

	double threshold = atof(argv[1]);
	int remove_link_n = 0;
	for (int i = 0; i < links_n; i++) {
		double backup = matrix[links[i].s * nodes_n + links[i].d];

		matrix[links[i].s * nodes_n + links[i].d] = 0;
		matrix[links[i].d * nodes_n + links[i].s] = 0;
		matrix[links[i].s * nodes_n + links[i].s] += backup;
		matrix[links[i].d * nodes_n + links[i].d] += backup;
		
		double * copy_matrix = (double *) malloc(nodes_n * nodes_n * sizeof(double));
		memcpy(copy_matrix, matrix, nodes_n * nodes_n * sizeof(double));
		double temp_connected_value = get_eigenvalue(copy_matrix, nodes_n);
		free(copy_matrix);

		if (temp_connected_value / origin < threshold) {
			matrix[links[i].s * nodes_n + links[i].d] = backup;
			matrix[links[i].d * nodes_n + links[i].s] = backup;
			matrix[links[i].s * nodes_n + links[i].s] -= backup;
			matrix[links[i].d * nodes_n + links[i].d] -= backup;
		} else {
			//printf("Threshold : %lf\n", temp_connected_value / origin);
			//printf("Remove Links %d : (%d, %d)\n", remove_link_n++, links[i].s, links[i].d);
		}
	}

	//print_matrix(matrix, nodes_n);
	FILE *out = fopen(argv[3], "w");
	fprintf(out, "%d %d\n", nodes_n, links_n - remove_link_n);
	for (int i = 0; i < links_n; i++) {
		if (matrix[links[i].s * nodes_n + links[i].d] != 0) {
			fprintf(out, "%d %d %.2lf\n", links[i].s, links[i].d, links[i].c);
		}
	}
	fclose(out);

	free(matrix);
	return 0;
}

