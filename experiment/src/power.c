#include "tools.h"

double get_power(double *matrix, int nodes_n) {
	double power_sum = 0;
	double card[4][2] = {{155.52, 60}, {1244.16, 100}, {2488.32, 140}, {9953.28, 174}};
	for (int i = 0; i < nodes_n; i++) {
		for (int j = 0; j < nodes_n; j++) {
			if (i == j) {
				continue;
			}

			double c = matrix[i * nodes_n + j];
			while (c > 0.0001) {
				if (c > card[3][0]) {
					c -= card[3][0];
					power_sum += card[3][1];
				} else if (c > card[2][0]) {
					c -= card[2][0];
					power_sum += card[2][1];
				} else if (c > card[1][0]) {
					c -= card[1][0];
					power_sum += card[1][1];
				} else if (c > card[0][0]) {
					c -= card[0][0];
					power_sum += card[0][1];
				} else {
					power_sum += card[0][1];
					break;
				}
			}
		}
	}

	return power_sum;
}

