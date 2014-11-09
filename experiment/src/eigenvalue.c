#include <math.h>
#include "tools.h"

double get_second(double *a, int n) {
	double first = 1000000, second = 1000000;
	for (int i = 0; i < n; i++) {
		if (a[i] <= second) {
			if (a[i] <= first) {
				second = first;
				first = a[i];
			} else {
				second = a[i];
			}
		}
	}
	return second;
}

int multiply_matrix(double * const a, double * const b, double * const out, int p, int q, int r) {
	// set zero of result matrix
	for (int i = 0; i < p * r; i++) {
		out[i] = 0.; 
	}

	double *pa, *pb, *pc;
	double s10, s11, s00, s01;
	int i, j , m;
	if (!(p & 1)) {
		if (!(r & 1)) { 
			for (m = 0, pc = out; m < r; m += 2, pc += 2) { 
				for(i = 0, pb = b + m; i < p; i += 2) {
                    pa = a + i * q; 
                    s00 = s01 = s10 = s11 = 0.; 
                    for (j = 0; j < q; j++, pa++) { 
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
            for (m = 0, pc = out; m < r - 1; m += 2, pc += 2) {
                for (i = 0, pb = b + m; i < p; i += 2) {
                    pa = a + i * q;
                    s00 = s01 = s10 = s11 = 0.;
                    for (j = 0; j < q; j++, pa++){
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
            for (i = 0; i < p; i++) {
                for (j = 0; j < q; j++) {
                    out[i * r + r - 1] += a[i * q + j] * b[j * r + r - 1];
                }
            }
        }
    } else {
        if (!(r & 1)) {
            for (m = 0, pc = out; m < r; m += 2, pc += 2) {
                for(i = 0, pb = b + m; i < p - 1; i += 2) {
                    pa = a + i * q;
                    s00 = s01 = s10 = s11 = 0.;
                    for (j = 0; j < q; j++, pa++) {
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
            for (i = 0; i < r; i++) {
                for(j = 0; j < q; j++) {
                    out[(p - 1) * r + i] += a[(p - 1) * q + j] * b[j * r + i];
                }
            }
        } else {
            for (m = 0, pc = out; m < r - 1; m += 2, pc += 2) {
                for(i = 0, pb = b + m; i < p - 1; i += 2){
                    pa = a + i * q;
                    s00 = s01 = s10 = s11 = 0.;
                    for (j = 0; j < q; j++, pa++) {
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
            for (i = 0; i < r; i++) {
                for(j = 0; j < q; j++) {
                    out[(p - 1) * r + i] += a[(p - 1) * q + j] * b[j * r + i];
                }
            }
            for (i = 0; i < p - 1; i++) {
                for (j = 0; j < q; j++) {
                    out[i * r + r - 1] += a[i * q + j] * b[j * r + r - 1];
                }
            }
        }
    }
	return 0;
}
double normalize_vector(double *x, int n) {
	double ans = 0.;
	for (int i = 0; i < n; i++) {
		ans += x[i] * x[i];
	}
	return sqrt(ans);
}


double trace_matrix(double *a, int n) {
	double ans = 0.;
	for (int i = 0; i < n; i++) {
		ans += a[i * n + i];
	}
	return ans;
}

double some_invariant_i(double *a, int n, int k) {
	double ans = 0.;
	for (int i = 0; i < n; i++) {
		ans += a[i * n + k] * a[i * n + k];
	}
	return ans;
}

double some_invariant_ii(double *a, int n) {
	double ans = 0.;
	for (int i = 0; i < n * n; i++) {
		ans += a[i] * a[i];
	}
	return ans;
}

int shift_matrix(double *a, int n, double k) {
	for (int i = 0; i < n * n; i += (n + 1)) {
		a[i] -= k;
	}
	return 0;
}

double inf_matrix_norm(double *a, int n) {
	double temp = 0., ans = 0.;
	for (int i = 0; i < n; i++) {
		temp = 0.;
		for (int j = 0; j < n; j++) {
			temp += fabs(a[j * n + i]);
		}
		if (temp > ans) {
			ans = temp;
		}
	}
	return ans;
}

int qr_upper_triangle(double *a, int n) {
	double s_k, temp;
	double eps = 1e-6;
	int dim_x;
	double *rotMatrix = (double *) malloc(n * n * sizeof(double));
	double *tempMatrix = (double *) malloc(n * n * sizeof(double));
	double *tempVector = (double *) malloc(n * n * sizeof(double));
	double *tempMatrix_i = (double *) malloc(n * n * sizeof(double));
	double *tempMatrix_ii = (double *) malloc(n * n * sizeof(double));

	for (int i = 0; i < (n - 2); ++i) {
		dim_x = n-i-1;
		s_k = 0.;
		for (int j = i + 2; j < n; ++j) {
			s_k += a[j * n + i] * a[j * n + i];
		}
		if (s_k < eps) {
			continue;
		}
		temp = sqrt(s_k + a[(i + 1) * n + i] * a[(i + 1) * n + i]);
		tempVector[0] = a[(i + 1) * n + i] - temp;
		for (int j = i + 2, k = 1; j < n; ++j, ++k) {
			tempVector[k] = a[j * n + i];
		}
		temp = sqrt(tempVector[0] * tempVector[0] + s_k);
		s_k = 1 / temp;
		for (int j = 0; j < dim_x; j++) {
			tempVector[j] *= s_k;
		}
		for (int j = 0; j < dim_x * dim_x; ++j) {
			rotMatrix[j] = 0.;
		}
		for (int j = 0; j < dim_x * dim_x; j += dim_x + 1) {
			rotMatrix[j] = 1.;
		}
		for (int j = 0; j < dim_x; ++j) {
			for (int k = j; k < dim_x; ++k) {
				rotMatrix[j * dim_x + k] -= 2 * tempVector[j] * tempVector[k];
			}
		}
		for (int j = 1; j < dim_x; ++j) {
			for (int k = 0; k < j; ++k) {
				rotMatrix[j * dim_x + k] = rotMatrix[k * dim_x + j];
			}
		}
   
		for (int j1 = i+1, j2 = 0; j1 < n; ++j1, ++j2) {
			for (int k1 = i, k2 = 0; k1 < n; ++k1, ++k2) {
				tempMatrix_i[j2 * (dim_x + 1) + k2] = a[j1 * n + k1];
			}
		}
		multiply_matrix(rotMatrix, tempMatrix_i, tempMatrix_ii, dim_x, dim_x, dim_x + 1);

		for (int j1 = i + 1, j2 = 0; j1 < n; ++j2, ++j1) {
			for (int k1 = i, k2 = 0; k1 < n; ++k1, ++k2) {
				a[j1 * n + k1] = tempMatrix_ii[j2 * (dim_x + 1) + k2];
			}
		}

		for (int j1 = 0; j1 < n; ++j1) {
			for (int k1 = i + 1, k2 = 0; k1 < n; ++k1, ++k2){
				tempMatrix_i[j1 * dim_x + k2] = a[j1 * n + k1];
			}
		}

		multiply_matrix(tempMatrix_i, rotMatrix, tempMatrix_ii, n, dim_x, dim_x);
		for (int j1 = 0; j1 < n; ++j1) {
			for (int k1 = i + 1, k2 = 0; k1 < n; ++k1, ++k2) {
				a[j1 * n + k1] = tempMatrix_ii[j1 * dim_x + k2];
			}
		}
	}

	free(tempMatrix);
	free(tempMatrix_i);
	free(tempMatrix_ii);
	free(tempVector);
	free(rotMatrix);
	return 0;
}


double get_eigenvalue(double *a, int n){
	qr_upper_triangle(a, n);

	double *out = (double *) malloc(n * sizeof(double));
	double *sins = (double *) malloc((n - 1) * sizeof(double));
	double *coss = (double *) malloc((n - 1) * sizeof(double));
	double shift;
	double norm = 0.;
	double eps = 1e-10;
	double temp1, temp2;
	double x,y;
  
	for (int i = n; i > 1; i--) {
		norm = inf_matrix_norm(a, n);
		while (fabs(a[(i - 1) * n + (i - 1) - 1]) > eps * norm) {
			shift = a[(i - 1) * n + (i - 1)] + 0.5 * a[(i - 1) * n + (i -1 ) - 1];
			shift_matrix(a, n, shift);
			for (int j = 0; j < i - 1; ++j) {
				x = a[j * n + j];
				y = a[(j + 1) * n + j];
				temp1 = sqrt(x * x + y * y);
				temp2 = 1. / temp1;
				sins[j] = -temp2 * y;
				coss[j] = temp2 * x;
				a[j * n + j] = temp1;
				for (int k = j + 1; k < i; ++k) {
					a[k * n + j] = 0.;
				}
				for (int k = j + 1; k < i; ++k) {
					temp1 = a[j * n + k] * coss[j] - a[(j + 1) * n + k] * sins[j];
					temp2 = a[j * n + k] * sins[j] + a[(j + 1) * n + k] * coss[j];
					a[j * n + k] = temp1;
					a[(j + 1) * n + k] = temp2;
				}
			}
			for (int j = 0; j < (i - 1); ++j) {
				for (int k = 0; k < (j + 2); ++k) {
					temp1 = a[k * n + j] * coss[j] - a[k * n + j + 1] * sins[j];
					temp2 = a[k * n + j] * sins[j] + a[k * n + j + 1] * coss[j];
					a[k * n + j] = temp1;
					a[k * n + j + 1] = temp2;
				}
			}
			shift_matrix(a, n, -shift);
			norm = inf_matrix_norm(a, n);
		}
		out[i - 1] = a[(i - 1) * n + (i - 1)];
	}
	out[0] = a[0];
	out[1] = a[n + 1];
	free(sins);
	free(coss);

	return get_second(out, n);
}
