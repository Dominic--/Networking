#include "tools.h"

//
// ./abilene_demand inputfile outputfile
//
int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "r");
	FILE *out = fopen(argv[2], "w");
	fprintf(out, "%d\n", 132);

	char demand[100];
	for (int i = 0; i < 720; i++) {
		int result = fscanf(in, "%s", demand);
		if (i % 5 == 0 && result && (i / 60 != (i / 5) % 12)) {
			fprintf(out, "%d %d %0.2lf\n", (i / 5) / 12, (i / 5) % 12, atof(demand));
		}
	}
	
	fclose(in);
	fclose(out);

	return 0;
}

