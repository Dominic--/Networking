#include <cstdio>
#include <cstdlib>

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

int multiply_matrix(double* const a, double* const b, double* const out, int p, int q, int r) {
	// set zero of result matrix
	for (int i = 0; i < p * r; i++) {
		out[i] = 0.; 
	}

	double s10, s11, s00, s01;
	if (!(p & 1)) {
		if (!(r & 1)) { 
			for (int m = 0, double *pc = out; m < r; m += 2, pc += 2) { 
				for(int i = 0, double *pb = b + m; i < p; i += 2) {
                    double *pa = a + i * q; 
                    s00 = s01 = s10 = s11 = 0.; 
                    for (int j = 0; j < q; j++, pa++) { 
                        s00 += pa[0] * pb[j * r]; 
                        s01 += pa[0] * pb[j * r + 1]; 
                        s10 += pa[q] * pb[j * r]; 
                        s11 += pa[q] * pb[j * r + 1];
                    }
                    pc[i * r] += s00;
                    pc[i * r + 1] += s01;
                    pc[(i + 1) * r] += s10;
                    pc[(i + 1) * r + 1] += s11;
                }
            }
        } else {
            for (int m = 0, double *pc = out; m < r - 1; m += 2, pc += 2) {
                for (int i = 0, double *pb = b + m; i < p; i += 2) {
                    double *pa = a + i * q;
                    s00 = s01 = s10 = s11 = 0.;
                    for (int j = 0; j < q; j++, pa++){
                        s00 += pa[0] * pb[j * r];
                        s01 += pa[0] * pb[j * r + 1];
                        s10 += pa[q] * pb[j * r];
                        s11 += pa[q] * pb[j * r + 1];
                    }
                    pc[i * r] += s00;
                    pc[i * r + 1] += s01;
                    pc[(i + 1) * r] += s10;
                    pc[(i + 1) * r + 1] += s11;
                }
            }
            for (int i = 0; i < p; i++) {
                for (int j = 0; j < q; j++) {
                    out[i * r + r - 1] += a[i * q + j] * b[j * r + r - 1];
                }
            }
        }
    } else {
        if (!(r & 1)) {
            for (int m = 0, double *pc = out; m < r; m += 2, pc += 2) {
                for(int i = 0, double *pb = b + m; i < p - 1; i += 2) {
                    double *pa = a + i * q;
                    s00 = s01 = s10 = s11 = 0.;
                    for (int j = 0; j < q; j++, pa++) {
                        s00 += pa[0] * pb[j * r];
                        s01 += pa[0] * pb[j * r + 1];
                        s10 += pa[q] * pb[j * r];
                        s11 += pa[q] * pb[j * r + 1];
                    }
                    pc[i * r] += s00;
                    pc[i * r + 1] += s01;
                    pc[(i + 1) * r] += s10;
                    pc[(i + 1) * r + 1] += s11;
                }
            }
            for (int i = 0; i < r; i++) {
                for(int j = 0; j < q; j++) {
                    out[(p - 1) * r + i] += a[(p - 1) * q + j] * b[j * r + i];
                }
            }
        } else {
            for (int m = 0, double *pc = out; m < r - 1; m += 2, pc += 2) {
                for(int i = 0, double *pb = b + m; i < p - 1; i += 2){
                    double *pa = a + i * q;
                    s00 = s01 = s10 = s11 = 0.;
                    for (int j = 0; j < q; j++, pa++) {
                        s00 += pa[0] * pb[j * r];
                        s01 += pa[0] * pb[j * r + 1];
                        s10 += pa[q] * pb[j * r];
                        s11 += pa[q] * pb[j * r + 1];
                    }
                    pc[i * r] += s00;
                    pc[i * r + 1] += s01;
                    pc[(i + 1) * r] += s10;
                    pc[(i + 1) * r + 1] += s11;
                }
            }
            for (int i = 0; i < r; i++) {
                for(int j = 0; j < q; j++) {
                    out[(p - 1) * r + i] += a[(p - 1) * q + j] * b[j * r + i];
                }
            }
            for (int i = 0; i < p - 1; i++) {
                for (int j = 0; j < q; j++) {
                    out[i * r + r - 1] += a[i * q + j] * b[j * r + r - 1];
                }
            }
        }
    }
  return 0;
}


void print_matrix(double* const matrix, int height, int width) {
	for (int i = 0; i < height; i++) { 
		for (int j = 0; j < width; j++) { 
			printf("%6.2lf", matrix[i * width + j]);
		} 
		printf("\n ");
	}
}
