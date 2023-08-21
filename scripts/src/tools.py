def cmp_lines(path_1, path_2):
	l1 = l2 = True
	with open(path_1, 'r') as f1, open(path_2, 'r') as f2:
		while l1 and l2:
			l1 = f1.readline()
			l2 = f2.readline()
			if l1 != l2:
				return False
	return True