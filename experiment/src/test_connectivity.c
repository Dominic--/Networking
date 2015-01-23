#include "tools.h"


//
//
// ./off with_weight threshold input_topology output_topology remove_topology
//
//
int main(int argc, char **argv) {
	// init matrix
	int nodes_n = 0, links_n = 0;
	double * matrix = NULL;
	link_t * links = NULL;
    bool with_weight = true;
	init_matrix_with_file(argv[1], &matrix, &links, &nodes_n, &links_n, with_weight);
    
    if (check_connectivity(matrix, nodes_n)) {
        printf("connected\n");
    } else {
        printf("disconnected\n");
    }

	free(matrix);
	return 0;
}

