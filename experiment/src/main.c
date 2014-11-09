#include "tools.h"


int main(int argc, char **argv) {
	// init matrix
	int nodes_n = 0, links_n = 0;
	double * matrix = NULL;
	link_t * links = NULL;
	char *filename = "../topology/connected/abilene-connected-topology";
	bool if_weight = false;
	init_matrix_with_file(filename, &matrix, &links, &nodes_n, &links_n, if_weight);

	print_matrix(matrix, nodes_n);

	// 
	double origin = get_eigenvalue(matrix, nodes_n);
	printf("Origin == %lf\n", origin);
	for (int i = 0; i < links_n; i++) {
		double backup = matrix[links[i].s * nodes_n + links[i].d];

		matrix[links[i].s * nodes_n + links[i].d] = 0;
		matrix[links[i].d * nodes_n + links[i].s] = 0;
		matrix[links[i].s * nodes_n + links[i].s] += backup;
		matrix[links[i].d * nodes_n + links[i].d] += backup;



		double new_second = get_eigenvalue(matrix, nodes_n);
		
		printf("New Second == %lf\n", new_second);
		links[i].impact = origin - new_second;

		matrix[links[i].s * nodes_n + links[i].d] = backup;
		matrix[links[i].d * nodes_n + links[i].s] = backup;
		matrix[links[i].s * nodes_n + links[i].s] -= backup;
		matrix[links[i].d * nodes_n + links[i].d] -= backup;
	}

	for (int i = 0; i < links_n; i++) {
		for (int j = 0; j < links_n; j++) {
			if (links[i].impact > links[j].impact) {
				int s = links[i].s, d = links[i].d;
				double impact = links[i].impact;

				links[i].s = links[j].s;
				links[i].d = links[j].d;
				links[i].impact = links[j].impact;

				links[j].s = s;
				links[j].d = d;
				links[j].impact = impact;
			}
		}
	}

	for (int i = 0; i < links_n; i++) {
		printf("Link %d : (%d, %d) --> %lf\n", i, links[i].s, links[i].d, links[i].impact);
	}

	free(matrix);
	return 0;
}

