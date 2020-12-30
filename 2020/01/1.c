#include <stdio.h>

#include "input.h"

#define is_same_type(a, b)      __builtin_types_compatible_p(typeof(a), typeof(b))
#define is_array(arr)           (!is_same_type((arr), &(arr)[0]))
#define Static_assert_array(arr) _Static_assert(is_array(arr), "Not a `[]` !")

#define ARRAY_SIZE(arr)(                    \
{                                           \
        Static_assert_array(arr);           \
        sizeof(arr) / sizeof((arr)[0]);     \
}                                           \
)

int main(void)
{
	int len = ARRAY_SIZE(input);
	int *p1, *p2, *pend;

	//printf("%d\n", len);

	pend = &input[len];

	for (p1 = &input[0]; p1 < pend; p1++) {
		for (p2 = p1 + sizeof(int); p2 < pend; p2++) {
			if (*p1 + *p2 == 2020) {
				printf("%d, %d\n", *p1, *p2);
				printf("%d\n", *p1 * *p2);
			}
		}
	}

	return 0;
}
