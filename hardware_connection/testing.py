from deepdiff import DeepDiff

t1 = [566,555,544,533]
t2 = [566,555,544,533]
t3 = [566,555,544,533,522,5111]

print(list(set(t1) ^ set(t2)))