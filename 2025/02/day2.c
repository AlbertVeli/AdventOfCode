#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RANGES 64
#define MAX_LINE   1024

struct range {
	long start;
	long end;
};

static int is_invalid(long n, int part2)
{
	char s[32];
	int L, p, reps, off;

	L = sprintf(s, "%ld", n);

	for (p = 1; p * 2 <= L; p++) {
		if (L % p != 0)
			continue;

		reps = L / p;
		if (reps < 2 || (!part2 && reps != 2))
			continue;

		off = p;
		for (;;) {
			if (off >= L)
				/* all blocks matched */
				return 1;
			if (strncmp(s, s + off, p) != 0)
				/* block doesn't match */
				break;
			off += p;
		}
	}
	return 0;
}

int main(void)
{
	char line[MAX_LINE];
	struct range ranges[MAX_RANGES];
	int num_ranges = 0;
	FILE *fp;
	char *p, *dash;
	int i;
	long a, b, n;
	long part1 = 0, part2 = 0;

	fp = fopen("input.txt", "r");
	if (!fp) {
		perror("fopen");
		return 1;
	}

	if (!fgets(line, sizeof(line), fp)) {
		fprintf(stderr, "Failed to read file\n");
		fclose(fp);
		return 1;
	}
	fclose(fp);

	/* Parse ranges */
	p = strtok(line, ",");
	while (p && num_ranges < MAX_RANGES) {
		dash = strchr(p, '-');
		if (!dash) {
			fprintf(stderr, "Invalid range: %s\n", p);
			return 1;
		}
		*dash = '\0';

		a = atol(p);
		b = atol(dash + 1);

		ranges[num_ranges].start = a;
		ranges[num_ranges].end   = b;
		num_ranges++;

		p = strtok(NULL, ",");
	}

	for (i = 0; i < num_ranges; i++) {
		a = ranges[i].start;
		b = ranges[i].end;

		for (n = a; n <= b; n++) {
			if (is_invalid(n, 0))
				part1 += n;
			if (is_invalid(n, 1))
				part2 += n;
		}
	}

	printf("Part 1: %ld\n", part1);
	printf("Part 2: %ld\n", part2);

	return 0;
}
