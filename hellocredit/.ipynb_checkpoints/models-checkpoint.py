def optimized_buckets(min_val, max_val, lower_is_better=False, num_buckets=9):
    """
    Generates optimized buckets based on min, max values, desired number of buckets, and whether lower values are better.

    Args:
        min_val (float): The minimum value.
        max_val (float): The maximum value.
        num_buckets (int, optional): Number of buckets. Defaults to 9.
        lower_is_better (bool, optional): True if lower values are better, else False. Defaults to False.

    Returns:
        list: List of tuples (start, end) representing each bucket's range.
    """
    min_val, max_val = (max_val, min_val) if lower_is_better else (min_val, max_val)
    interval = (max_val - min_val) / (num_buckets - 1)
    buckets = [(round(min_val + i * interval, 2), round(min_val + (i + 1) * interval, 2)) for i in range(num_buckets - 1)]
    buckets.append((round(max_val - interval, 2), max_val))
    return list(reversed(buckets)) if lower_is_better else buckets

# Redefine the values and number of buckets for clarity
min_val = 1
median_val = 3
max_val = 5
num_buckets = 3

# Generate the optimized buckets
buckets_list = get_buckets(min_val, median_val, max_val, num_buckets)
print(buckets_list)