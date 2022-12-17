#!/usr/bin/env python3

# detect pattern of length m, repeated k or more times
# (thanks google)
def find_pattern(arr, m, k):
    L = len(arr)
    cnt = 0
    threshold = m * (k - 1)
    for i in range(L - m):
        if arr[i] == arr[i + m]:
            if cnt == 0:
                start_i = i
            cnt += 1
        else:
            cnt = 0
            start_i = -1
        if cnt == threshold:
            # Repeats at least k times
            print(f'repeating pattern of length {m} starts at index {start_i}')
            return True
    return False 

pattern = [1, 4, 6, 2, 4, 9, 3, 4, 3, 4, 5, 9, 2, 1, 4, 5]
lst = [1, 2, 3, 9, 9, 8, 6, 4, 4] + pattern * 4
print(lst)
for length in range(11, 17):
    # search for pattern repeating at least 4 times
    has_pattern = find_pattern(lst, length, 4)
