import random



class User:
	def __init__(self,num_items):
		self.num_items = num_items
		self.items = self.generate_list()
		self.x_coord = None
		self.y_coord = None

	def generate_list(self):
		my_list = []
		for num in range(self.num_items):
			rand = random.randrange(10000)
			my_list.append(rand)
		return my_list


def generate_users(num_users,num_items):
	user_list = []
	for i in range(num_users):
		user_list.append(User(num_items))
	return user_list

user_list = generate_users(50,1000)

def generate_grid(size):
	grid = []
	for i in range(size):
		row = []
		for j in range(size):
			row.append([])
		grid.append(row)
	return grid



def comparison(user1,user2):
	count = 0
	similar = 0
	for x in user1.items:
		if x in user2.items:
			similar += 1
		count += 1
	percent = similar /count
	return percent


def seed_grid(user_list,max_num_iterations,size_of_grid):
	grid = generate_grid(size_of_grid)
	first_user = user_list.pop()
	# places the first user at the centre
	first_user.x_coord = int(size_of_grid/2)
	first_user.y_coord = int(size_of_grid/2)
	grid[first_user.y_coord][first_user.x_coord].append(first_user)
	user_counter = 1

	direction_array = [[0,1],[-1,0],[0,-1],[1,0]]
	direction_index = random.randrange(0,4)


	# places other users
	# loops through users list, who have starting coordinates in the middle of the map
	for user in user_list:
		x_coord = first_user.x_coord
		y_coord = first_user.y_coord
		# ensure iterations is limited to number of users currently on the map
		iterations = min(user_counter,max_num_iterations)
		for it in range(iterations):
			found = False
			search_radius = 0
			### Finds the nearest user for comparison
			count = 0
			while found == False:
				# biased - needs fixing!!!!!!
				search_index = random.randrange(0,4)
				for x in range(4):
					search_y = int(max(min(y_coord+(direction_array[search_index][0])*search_radius,size_of_grid-1),0))
					search_x = int(max(min(x_coord+(direction_array[search_index][1])*search_radius,size_of_grid-1),0))

					on_the_spot = grid[search_y][search_x]
					if len(on_the_spot) > 0:
						found = True
						comparator = on_the_spot[random.randrange(0,len(on_the_spot))]
						break
						if search_index == 3:
							search_index = 0
						else:
							search_index += 1 
				search_radius += 1
				count += 1
				if count == 10:
					break
			similarity = comparison(user,comparator)
			if similarity >= 0.12:
				distance = 0
			elif similarity <= 0.07:
				distance = int(size_of_grid/2)
			else:
				distance = (similarity - 0.07)/(0.12-0.07) * int(size_of_grid/2)

			print(distance)
			# print(similarity)
			# distance = ((1-similarity)*int(size_of_grid/2))
			# can be improved to nudges direction based on previous similarity value
			x_coord += distance*direction_array[direction_index][1]
			y_coord += distance*direction_array[direction_index][0]
			## change direction
			if direction_index == 3:
				direction_index = 0
			else:
				direction_index += 1 
			#temp fix
			x_coord = max(0,x_coord)
			x_coord = min(size_of_grid-1,x_coord)
			y_coord = max(0,y_coord)
			y_coord = min(size_of_grid-1,y_coord)
		user.x_coord = x_coord
		user.y_coord = y_coord
		grid[int(x_coord)][int(y_coord)].append(user)
		user_counter += 1
	# prints out the grid
	display_grid = generate_grid(size_of_grid)	
	for row in range(len(grid)):
		for col in range(len(grid)):
			display_grid[row][col] = len(grid[row][col])
	for row in display_grid:
		print(row)
	return grid

	# for x,row in enumerate(grid):
	# 	comparison_total_total = 0
	# 	random_comparison = 0
	# 	count_total = 0
	# 	for y,col in enumerate(row):
	# 		print(x,y)
	# 		count = 0
	# 		comparison_total = 0
	# 		for user in col:
	# 			print (sorted(user.items), comparison(user,col[0]))
	# 			count += 1
	# 			count_total += 1
	# 			comparison_total += comparison(user,col[0])
	# 			comparison_total_total += comparison(user,col[0])
	# 			print (grid[random.randrange(0,size_of_grid-1)][0][0])
	# 			if len(grid[random.randrange(0,size_of_grid-1)][0]) > 0:
	# 				random_comparison += comparison(user,grid[random.randrange(0,size_of_grid-1)][0][0])

	# 		try:
	# 			print("Average: {0}".format(comparison_total/count))
	# 		except:
	# 			pass
	# print("My average{0}".format(comparison_total_total/count_total))
	# print("Random average")

# def algo_analysis(grid):
# 	total_similar = 0
# 	count = 0
# 	for x, row in enumerate(grid):
# 		for y, col in enumerate(row):
# 			if len(col) > 1:
# 				user1 = col.pop()
# 				for user in col:
# 					total_similar += comparison(user1,user)
# 					count += 1
# 	return total_similar / count 


# grid = seed_grid(user_list,50,10)
# print(algo_analysis(grid))


# seed_grid(user_list,20,25)

def test(number_of_runs):
	correlation_total = 0
	a = User(1000)
	for x in range(number_of_runs):
		b = User(1000)
		correlation_total += comparison(a,b)
	return correlation_total / number_of_runs

print(test(1000))
