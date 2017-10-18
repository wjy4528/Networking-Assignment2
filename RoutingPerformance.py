import sys
import socket
import time
import threading
import os.path 
import math
import collection
import re
from Graph import Graph

#global counters
total_circuit_request = 0
total_packets = 0
total_success_packets = 0
total_blocked_packets = 0
avg_cumulative_prog = 0
total_paths = 0
total_hops = 0

#arr of global counters
arr_avg_hop = []
arr_avg_delay = []

def create_graph(TOPOLOGY_FILE):
	my_graph=Graph()
	with open(TOPOLOGY_FILE,'r') as ff:
		for line in ff:
			node_name=line.split(' ')[0]
			node_name_1=line.split(' ')[1]
			delay_time=line.split(' ')[2]
			max_laod=line.split(' ')[3].split('\n')[0]
			my_graph.add_Node(node_name)
			my_graph.add_Node(node_name_1)
			my_graph.add_adj(node_name,node_name_1,delay_time,max_laod)
			my_graph.add_adj(node_name_1,node_name,delay_time,max_laod)
	return my_graph


def dijsktra(graph,start_node,end_node):
	visited={start_node:0}
	path={}
	nodes=set(graph.graph)
	while nodes:
		min_node=None
		for node in nodes:
			if node.name in visited:
				if min_node is None:
					min_node=node
				elif visited[node.name]<visited[min_node.name]:
					min_node=node
		if min_node is None:
			break
		nodes.remove(min_node)
		current_weight=visited[min_node.name]
		for edge in min_node.adj_node:
			weight=current_weight+int(edge['dtime'])
			if edge['name'] not in visited or weight < visited[edge['name']]:
				visited[edge['name']]=weight
				path[edge['name']]=min_node.name
	search_key=end_node
	path_to_return=search_key

	while search_key!=start_node:
		temp=path[search_key]
		path_to_return=temp+path_to_return
		search_key=temp

	return path_to_return

#main processing function
def workload(input, packet_rate, case):
	#some vars
	m = re.search('(.*\d+) (/w) (/w) (.*\d+)', input )
	elapse = float(m.group(1))
	num_packets = round(float(packet_rate)*float(m.group(4)))
	source = m.group(2)
	destin = m.group(3)
	packet_dur = round(num_packets/float(packet_rate))


	print "debugging here:"
	print "----------------------------"
	print "elapse" + str(elapse)
	print "number of packets" + str(num_packets)
	print "source " + str(source)
	print "destination " + str(destin)

	#check the commands to see which case to approach
	#example command: 

	if (case == 0):
		#case 1
		#use routing protocol once and send packets through the same route

	elif (case == 1):
		#case 2
		#use routing protocol multiple times and 
		#find appropriate path for each packet (time elapse and time is important here)

		#blocked request

		#busy: route once the circuit has been established

		#need to implement something in graph for this case

	else:
		print "invalid input"
		return 

def workload_case1():
	pass

def workload_case2():
	pass


#stats functions here
def init_stats():
	#check if file exist 
	#if so delete and make new
	fname = "./log.txt"
	if (os.path.exists(fname)):
		print "it exists"
	else:
		print "no file exist in directory"
	

def log_statistics():
	#calculates the statistics and appedn to file

	success_percentage_routed_packets = total_success_packets/total_success_packets
	blocked_percent = total_blocked_packets/total_packets
	avg_hops = total_hops/total_paths

	f = open("stats.txt", 'a+')

	f.write("total number of virtual circuit requests:" + str(total_circuit_request))
	f.write("total number of packets:" + str(total_packets))
	f.write("number of successfully routed packets:" + str(total_success_packets))
	f.write("percentage of successfully routed packets:" + str(success_percentage_routed_packets)) 
	f.write("number of blocked packets:" + str(total_blocked_packets))
	f.write("percentage of blocked packets:" + str())
	f.write("average number of hops per circuit:" + str())
	f.write("average cumulative propagation delay per circuit:" + str())

	f.close()


def print_stats ():
	#for debugging purposes
	f = open("stats.txt", 'r')

	for line in iter(f):
		print line 
	f.close()

def cal_avg_delay():
	#array of delay over, each element calculated individually based off the other delay
	#add up all the delays in the array over total circuits
	
	#completed


def cal_avg_hops(hops_input):
	#total hops per circuit
	#over total circuits
	global arr_avg_hop

	if (len(arr_avg_hop) == 0):
		arr_avg_hop.append(hops_input)
	else:
		arr_total = 0
		for i in arr_avg_hop:
			arr_total += i

		arr_total += hops_input
		arr_avg_hop.append(arr_total / (len(arr_avg_hop)+1))

	#completed


def main():
	NETWORK_SCHEME=sys.argv[1]
	ROUTING_SCHEME=sys.argv[2]
	TOPOLOGY_FILE=sys.argv[3]
	WORKLOAD_FILE=sys.argv[4]
	PACKET_RATE=sys.argv[5]

	my_graph=create_graph(TOPOLOGY_FILE)

	path=dijsktra(my_graph,'A','O')
	#print(visited)
	print(path)

	#workload main 
	workload(path, PACKET_RATE)


	'''
	for each in my_graph.graph:

		print(each.name)
		print("adj_node")
		for one in each.adj_node:
			print(one['name'])
		print("------------")
	'''




if __name__=='__main__':
	main()