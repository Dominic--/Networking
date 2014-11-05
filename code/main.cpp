  double *b;
  double temp;
  char *name;
  clock_t t;
  double time=0.;
  FILE *input;
    
  b = new double[n];
  printMatrix(a, n, n);

  qrAlmostUpperTriangle(a, n);
  temp = traceMatrix(a, n);
  printf("Trace after step 1:%.2lf\n", temp);
  searchEigenValues(a, b, n);
  printMatrix(a, n, n);
  temp = traceMatrix(a, n);
  printf("Trace after step 2:%.2lf\n", temp);

  for (int i=0; i<n; i++){
    printf("Value %d: %.4lf\n", i, b[i]);
  }
  delete[] a;
  delete[] b;
  return 0;
}
