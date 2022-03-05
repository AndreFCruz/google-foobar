def root_of_node(h, k):
	# Start at root
	root_of_current = -1
	current_node = 2 ** h - 1
	current_h = h

	while current_node != k:
		current_h -= 1
		# Take left path or right path?
		left_child = current_node - (2 ** current_h)
		right_child = current_node - 1

		root_of_current = current_node
		if k <= left_child:
			current_node = left_child
		else:
			current_node = right_child

	return root_of_current


def solution(h, q):
	return [root_of_node(h, k) for k in q]


if __name__ == '__main__':
	
	print(solution(5, [19, 14, 28]))
	# Output: 21,15,29

	print(solution(3, [7, 3, 5, 1]))
	# Output: -1,7,6,3
