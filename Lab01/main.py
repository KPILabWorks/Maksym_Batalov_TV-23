import itertools

def merge_nested_lists(list1, list2):
    return list(set(itertools.chain.from_iterable(list1 + list2)))

# Input example
nested_list1 = [[1, 2], [3, 4]]
nested_list2 = [[3, 5], [6, 2]]

result = merge_nested_lists(nested_list1, nested_list2)
print(result)
