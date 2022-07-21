from math import sqrt

start_time = 7.00

class Pkg:
	def __init__(self, p_id: int, x_coor: float, y_coor: float, priority: int, rta) -> None:
		self.p_id = p_id
		self.p_x = x_coor
		self.p_y = y_coor
		self.p_dist = sqrt(x_coor**2 + y_coor**2)
		self.p_priority = priority
		self.p_rta = rta
		self.p_time_window = self.__set_time_window()
	
	def __set_time_window(self) -> tuple:
		time_w = []

		if self.p_priority == 2:
			time_w.append(self.p_rta - 0.25)
			time_w.append(self.p_rta + 0.25)
		elif self.p_priority == 1:
			time_w.append(self.p_rta - 1.0)
			time_w.append(self.p_rta + 1.0)
		else:
			time_w.append(start_time)
			time_w.append(start_time + 12)
		
		return tuple(time_w)
	
	def get_loc(self) -> tuple:
		return (self.p_x, self.p_y)
	
	def miss_check(self, eta):
		return self.p_time_window[1] > eta
	
	def within_time_window(self, eta):
		return self.p_time_window[0] <= eta <= self.p_time_window[1]

class Graph:
	def __init__(self, num_nodes: int, directed=True):
		self.m_num_nodes = num_nodes
		self.m_directed = directed
		self.m_adj_mat = [[0 for col in range(self.m_num_nodes)] for row in range(self.m_num_nodes)]

	def add_edge(self, src: int, dest: int, weight: float) -> None:
		self.m_adj_mat[src][dest] = weight
		if not self.m_directed:
			self.m_adj_mat[dest][src] = weight
	
	def print_graph(self) -> None:
		for row in self.m_adj_mat:
			print(row)
		print()

def distance(src: tuple, dest: tuple) -> float:
	return sqrt((src[0] - dest[0])**2 + (src[1] - dest[1])**2)