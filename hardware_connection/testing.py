repo = ["1", "2", "3", "4"]
i = 0


def some_f():
	"""

	:return:
	"""
	yield repo[i]


print(next(some_f()))
repo.pop(0)

print(next(some_f()))
repo.pop(0)
print(repo)
print(next(some_f()))
