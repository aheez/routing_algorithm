from random import random as rnd
from module import *
import time
from datetime import datetime


MAX_PKGS = 35
AVG_SPEED = 60
MAX_TIME = 1 / 3
MAX_DIST = MAX_TIME * AVG_SPEED

ts = 7.00

def generate_pkgs(num_pkgs: int) -> list:
	pkgs = [Pkg(0, 0, 0, 0, 0)]
	for i in range(num_pkgs):
		x = rnd() * MAX_DIST
		y = rnd() * MAX_DIST
		priority = int(rnd() * 100 % 3)
		rta = rnd() * 12 + ts
		pkgs.append(Pkg(i + 1, x, y, priority, rta))
	return pkgs

def generate_graph(pkg_list: list) -> Graph:
	graph = Graph(len(pkg_list))
	for i in pkg_list:
		for j in pkg_list:
			if i.p_id != j.p_id:
				graph.add_edge(i.p_id, j.p_id, distance(i.get_loc(), j.get_loc()) / AVG_SPEED)
	return graph

def print_pkg_list(pkg_lis: list) -> None:
	print("Pkg list:")
	print("id\t(X,Y)\tPriority\tRTA\tTime window")
	for pkg in pkg_lis:
		if pkg.p_priority == 2:
			pr = "High"
		elif pkg.p_priority == 1:
			pr = "Medium"
		else:
			pr = "Low"
		print(pkg.p_id, pkg.get_loc(), pr, pkg.p_rta, pkg.p_time_window)
	print()

def find_missing_pkg(sched, search_pool, pkg_list):
	for pkg in pkg_list:
		if pkg not in sched and pkg not in search_pool:
			return pkg
	return None

def search_alg(graph: Graph, pkg_list: list) -> list:
	# Based on bratley's algorithm and BFS
	sched = [pkg_list[0]]
	search_pool = [x for x in pkg_list if x not in sched]
	time = p_time =  [ts]
	add_delay = False
	iter = 0
	wasted_time = 0

	# while len(search_pool) > 0:
	#	for pkg in search_pool:
	#		temp_node = search_pool.pop(0)
	#		eta = graph.m_adj_mat[sched[-1].p_id][temp_node.p_id]

	#		if temp_node.within_time_window(time[-1] + eta):
	#			sched.append(temp_node)
	#			time.append(time[-1] + eta)
	#			add_delay = False
	#			break

	#		elif not temp_node.miss_check(time[-1] + eta):
	#			search_pool.append(sched.pop())
	#			break

	#		else:
	#			search_pool.append(temp_node)

	#	if add_delay:
	#		time.append(time[-1] + (10 /60))
	#		wasted_time += 10 / 60

	#	if len(search_pool) + len(sched) != len(pkg_list):
	#		print("Error: len(search_pool) + len(sched) != len(pkg_list)")
	#		mis_pkg = find_missing_pkg(sched, search_pool, pkg_list)
	#		print("Missing Pkg ID:", mis_pkg.p_id)
	#		return [sched, time, wasted_time]
	#	add_delay = True
	#	iter += 1

	while len(search_pool) > 0:
		for pkg in search_pool:
			eta = graph.m_adj_mat[sched[-1].p_id][pkg.p_id] + time[-1]

			if pkg.within_time_window(eta):
				pkg.p_eta = eta
				sched.append(pkg)
				search_pool.remove(pkg)
				time.append(eta)
				p_time.append(eta)
				add_delay = False
				break
			elif not pkg.miss_check(eta):
				search_pool.append(sched.pop())
				time.pop()
				p_time.pop()
				time.append(sched[-1].p_eta)
				add_delay = False
				break

		if add_delay:
			time.append(time[-1] + (10 /60))
			wasted_time += 10 / 60

		if len(search_pool) + len(sched) != len(pkg_list):
			print("Error: len(search_pool) + len(sched) != len(pkg_list)")
			mis_pkg = find_missing_pkg(sched, search_pool, pkg_list)
			print("Missing Pkg ID:", mis_pkg.p_id)
			return [sched, time, wasted_time]

		if iter >= len(pkg_list) ** 2:
			print("No schedule was found")
			return

		add_delay = True
		iter += 1

	return [sched, time, wasted_time]

def generate_graph_distance(pkg_list: list) -> Graph:
	graph = Graph(len(pkg_list))
	for i in pkg_list:
		for j in pkg_list:
			if i.p_id != j.p_id:
				graph.add_edge(i.p_id, j.p_id, distance(i.get_loc(), j.get_loc()))
	return graph


def get_min_val(list: list) -> list:
	min_val = min(list)
	min_idx = list.index(min_val)
	return [min_val, min_idx]

def hamads_alg(g: Graph, pkg_list: list) -> list:
	# based on distance
	route = [pkg_list[0]]

	for i in range(1, len(pkg_list)):
		[idc, next_stop] = get_min_val(g.m_adj_mat[route[-1].p_id])
		route.append(pkg_list[next_stop])
	return route

def main():
	pkgs_num = []
	avg_time = []
	for i in range(1, 21):
		pkgs_num.append(5 * i)
		pkgs_num[-1]
		dt = 0

		for j in range(3):
			pkg_list = generate_pkgs(pkgs_num[-1])
			graph = generate_graph(pkg_list)
			t0 = time.perf_counter_ns()

			# [schedule, time_list, waste_time] = search_alg(graph, pkg_list)
			search_alg(graph, pkg_list)

			dt += (time.perf_counter_ns() - t0) / 10e3

		avg_time.append(dt / 3.0)

	print('-' * 59)
	print('|{:^10}| {:^20}|'.format('# Pkgs', 'AvgTime(ms)'))
	for i in range(len(pkgs_num)):
		print('-' * 19)
		print('{:<}| {:<}'.format(pkgs_num[i], avg_time[i]))
	print('-' * 19)

	title = datetime.now().isoformat()

	with open(title + '.csv', 'x', encoding='utf-8') as f:
		f.write('#pkgs, avgSpeed\n')
		for i in range(len(pkgs_num)):
			f.write('{},{}\n'.format(pkgs_num[i], avg_time[i]))


if __name__ == '__main__':
	main()
	exit(0)

