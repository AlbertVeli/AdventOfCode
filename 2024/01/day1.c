#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINES 1000

/* compare function for qsort */
int compare_ints(const void *a, const void *b)
{
	return (*(int *)a - *(int *)b);
}

int count_occurrences(int *array, size_t size, int target)
{
	int count;
	size_t i;

	for (i = 0, count = 0; i < size; i++) {
		/* almost unreadable, but it works */
		count += array[i] == target;
	}

	return count;
}

int main(int argc, char *argv[])
{
	FILE *fp;
	/* Input is 1000 lines */
	int left[MAX_LINES], right[MAX_LINES];
	int sorted_left[MAX_LINES], sorted_right[MAX_LINES];
	int n, i, result;

	if (argc < 2) {
		fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
		return 1;
	}

	fp = fopen(argv[1], "r");
	if (!fp) {
		perror("Error opening file");
		return 1;
	}

	n = 0;
	/* This could lead to a stack overflow if the file has more than 1000 lines */
	while (fscanf(fp, "%d %d", &left[n], &right[n]) == 2) {
		n++;
	}
	fclose(fp);

	/* Part 1, distance between lists */
	memcpy(sorted_left, left, n * sizeof(int));
	memcpy(sorted_right, right, n * sizeof(int));

	qsort(sorted_left, n, sizeof(int), compare_ints);
	qsort(sorted_right, n, sizeof(int), compare_ints);

	for (i = 0, result = 0; i < n; i++) {
		result += abs(sorted_left[i] - sorted_right[i]);
	}
	printf("Part 1: %d\n", result);

	/* Part 2, similarity score */
	for (i = 0, result = 0; i < n; i++) {
		result += left[i] * count_occurrences(right, n, left[i]);
	}
	printf("Part 2: %d\n", result);

	return 0;
}
