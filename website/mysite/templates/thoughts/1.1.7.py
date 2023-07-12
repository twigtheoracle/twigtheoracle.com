def euclid(m: int, n:int) -> int:
	# Keep track of the number of times step E1 has been executed
	e1_counter = 0

	while(True):

		# Step E1
		e1_counter += 1
		r = m % n

		# Step E2
		if r == 0:
			return e1_counter

		# Step E3
		m = n
		n = r

digits = 6
for m in range(1, 21):
	total = 0
	end_point = 10**digits
	for i in range(1, end_point + 1):
		total += euclid(m, i)
	print(f"{m} & {total / end_point} \\\\")