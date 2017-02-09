
import sys, os
import networkx as nx
import community



def create_NX_obj(edges):
	# takes list of edges of format [p1, p2, weight]
	G = nx.Graph()
	for edge in edges:
		G.add_edge(edge[0], edge[1], weight=float(edge[2]))
	print "%d edges added." %(len(edges))
	return G


def main():
	projectPath = sys.argv[1]
	robustPath = projectPath+"/summary/robust_nodes_edgevals.txt"
	f_out = projectPath+"/summary/louvian_clustering/"
	
	if not os.path.exists(f_out): os.makedirs(f_out)
	
	# read into array
	edges = []
	with open(robustPath, 'r') as f:
		for line in f.readlines():
			edges.append(line.rstrip('\n').split('\t'))
	
	G = create_NX_obj(edges)
	partition = community.best_partition(G)
	
	clusters = []
	for com in set(partition.values()):
		list_nodes = [nodes for nodes in partition.keys() if partition.keys() if partition[nodes] == com]
		clusters.append(list_nodes)		
	clusters.sort(key=lambda a: -len(a))

	print "%d clusters found with sizs:" %len(clusters)
	print [len(x) for x in clusters]

	# write out cluster information
	with open(f_out+"node_membership.txt", 'w') as f:
		for i, cluster in enumerate(clusters):
			for node in cluster:
				f.write("%d\t%s\n" %(i, node))
	
	# write annotations
	os.system("python clustering/analyze_gene_clusters_enrichr.py "+f_out+"node_membership.txt")	

main()
