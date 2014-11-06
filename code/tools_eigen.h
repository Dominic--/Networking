#include <cstdio>

void printMatrix(double*, int, int);

int readMatrixFromFile(FILE*, double*, int);
int simpleMatrixMultiply(double*,double*,double*,int,int,int);

int qrAlmostUpperTriangle(double*, int);
int searchEigenValues(double*, double*, int);
double traceMatrix(double*, int);
double someInvariant_ii(double *, int );
