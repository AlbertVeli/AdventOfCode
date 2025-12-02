#include <stdio.h>
#include <stdlib.h>

typedef struct {
	/* dir: +1 for 'R', -1 for 'L' */
	int dir;
	int dist;
} Move;

int read_moves(const char *filename, Move **out_moves, int *out_count)
{
	char buf[128];
	int lines = 0;
	int idx = 0;
	int empty;

	FILE *fp = fopen(filename, "r");
	if (!fp) {
		perror("fopen");
		return -1;
	}

	/* Count non-empty lines */
	while (fgets(buf, sizeof(buf), fp)) {
		empty = 1;
		for (char *p = buf; *p; ++p) {
			if (*p > ' ') {
				empty = 0;
				break;
			}
		}
		if (!empty)
			lines++;
	}

	if (lines == 0) {
		fclose(fp);
		*out_moves = NULL;
		*out_count = 0;
		return 0;
	}

	Move *moves = malloc((size_t)lines * sizeof(Move));
	if (!moves) {
		fclose(fp);
		perror("malloc");
		return -1;
	}

	rewind(fp);
	idx = 0;

	/* Read moves */
	while (fgets(buf, sizeof(buf), fp) && idx < lines) {
		char c;
		int dist;

		/* Skip empty lines */
		int empty = 1;
		for (char *p = buf; *p; ++p) {
			if (*p > ' ') {
				empty = 0;
				break;
			}
		}
		if (empty)
			continue;

		if (sscanf(buf, " %c%d", &c, &dist) == 2) {
			int dir         = (c == 'R') ? 1 : -1;
			moves[idx].dir  = dir;
			moves[idx].dist = dist;
			idx++;
		}
	}

	fclose(fp);
	*out_moves = moves;
	*out_count = idx;

	return 0;
}

/* Part 1: Count how many times we land on position 0 */
int part1(const Move *moves, int count)
{
	int pos = 50;
	int zero_count = 0;
	int i;

	for (i = 0; i < count; i++) {
		pos = (pos + moves[i].dir * moves[i].dist) % 100;
		if (pos < 0)
			pos += 100;

		if (pos == 0)
			zero_count++;
	}

	return zero_count;
}

/* Part 2: Count how many times we pass over position 0 */
int part2(const Move *moves, int count)
{
	int pos = 50;
	int zero_count = 0;
	int dir, dist, first;

	for (int i = 0; i < count; ++i) {
		dir  = moves[i].dir;
		dist = moves[i].dist;

		/* Determine distance to first zero crossing */
		if (pos == 0) {
			first = 100;
		} else {
			first = (dir == 1) ? (100 - pos) : pos;
		}

		/* Count zero crossings */
		if (dist >= first) {
			int hits = 1 + (dist - first) / 100;
			zero_count += hits;
		}

		/* Update position */
		pos = (pos + dir * dist) % 100;
		if (pos < 0)
			pos += 100;
	}

	return zero_count;
}

int main(void)
{
	const char *filename = "input.txt";
	Move *moves          = NULL;
	int count;

	if (read_moves(filename, &moves, &count) != 0) {
		fprintf(stderr, "Failed to read input\n");
		return 1;
	}

	printf("Part 1: %d\n", part1(moves, count));
	printf("Part 2: %d\n", part2(moves, count));

	free(moves);

	return 0;
}
