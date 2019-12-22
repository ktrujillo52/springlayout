#!/usr/bin/python
#Global trade analysis WITS Data 
import pandas as pd
import os
import networkx as nx
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable


#Change directory
os.chdir("../data/wits_summary_10")
#Get directory
path = os.getcwd()
#Get contents of directory
contents = []
tot = os.listdir(path)
for item in tot:
	contents.append(item)
#Read CSV
#Create array and dictionary
countries = []
data = []
count = 0
#Create a directed graph called G
G = nx.DiGraph()
for item in contents:
	with open(item, "r+") as f:
		#text = pd.read_csv(csv)
		text = csv.reader(f)
		#Read all countries into array
		for row in text:
			print row
			if (row[0] not in countries):
				countries.append(row[0])
		f.close()

for item in contents:
	with open(item, "r+") as f:
		text = csv.reader(f)
		#Collect all data
		for row in text:
			data.append(row)
		
		count += 1
		f.close()		
#Build dictionary
dic = {}
for i in countries:
	dic[i] = {key : float(0) for key in countries}

for i in data:
	if (str(i[0]) in countries):
				if (i[1] in countries):
					if (str(i[2]) == "All Products"):
						try:					
							dic[i[0]][i[1]] += float(i[5])	
						except:
							print "Error"
						#print dic[i[0]][i[1]]
#Test
"""Check to see if all files opened"""
print "Length contents:"+str(len(contents))
print "Opened: "+str(count)

#Clean list
clean = []
for i in countries:
	if (str(i) != 'nan'): 
		clean.append(i)


"""Count countries in list"""
#print "Length of countries list: "+str(len(clean))
#for i in countries:
#	for j in countries:
#		print str(i)+"+"+str(j)+":"+str(dic[i][j])

#Build the network by adding each row of data as edge between two nodes
track1 = []
track2 = []
for i in countries:
	for j in countries:
		#if (k == i and l == j or k == j and l == i):
		#	next
		#else:
		if (float(dic[i][j]) != float(0)):
			#track1.append(i)
			#track2.append(j)
			try:
				for k, l in zip(track1, track2):
					if (str(k) == str(i) and str(l) == str(j) or str(k) == str(j) and str(l) == str(i)):
						G.add_edge(i, j, weight=int(dic[i][j]))
						print str(i)+"-"+str(j)+":"+str(dic[i][j])
					else:
						#G.add_edge(i, j, weight=int(dic[i][j]))
						#print str(i)+"-"+str(j)+":"+str(dic[i][j])	
						#print "Skipped:"+str(k)+"-"+str(l)+":"+str(dic[k][l])
						next
				track1.append(i)
				track2.append(j)
			except:
				print "Could not create edge"
			#track1.append(i)
			#track2.append(j)


print "Track1:"+str(track1)
print "Track2:"+str(track2)



#Calculate eigenvector centrality
ec = nx.eigenvector_centrality_numpy(G, weight='weight')
nx.set_node_attributes(G,'cent', ec)
node_color = [float(G.node[v]['cent']) for v in G]

#Calculate each country's total exports
totexp = {}
for exp in G.nodes():
	tx = sum([float(g) for exp, f, g in G.out_edges_iter(exp, 'weight')])
	totexp[exp] = tx
	avgexp = np.mean(tx)
	nx.set_node_attributes(G, 'totexp', totexp)
#Use results later for node's size in the graph
node_size = [float(G.node[v]['totexp']) / avgexp for v in G]

#Test
G.nodes()
G
for (u,v,d) in G.edges(data='weight'):
	print '(%s, %s, %s)'%(u,v,d)
for u in G.nodes(data=False):
	print '[%s]'%(u)



# Visualization
# Calculate position of each node in G using networkx spring layout
pos = nx.spring_layout(G,k=None,iterations=50) 

# Draw nodes
nodes = nx.draw_networkx_nodes(G,pos, node_size=node_size, \
                               node_color=node_color, alpha=0.5) 
# Draw edges
edges = nx.draw_networkx_edges(G, pos, edge_color='lightgray', \
                               arrows=False, width=0.05,)

# Add labels
nx.draw(G,pos,with_labels=True, font_size=10)
#nx.draw_networkx_labels(G,pos,font_size=5)
nodes.set_edgecolor('gray')

# Add labels and title
plt.text(0,-0.1, \
         'Node color is eigenvector centrality; \
         Node size is value of global exports', \
         fontsize=7)
plt.title('Global Trade Network ', fontsize=12)

# Bar with color scale for eigenvalues
cbar = plt.colorbar(mappable=nodes, cax=None, ax=None, fraction=0.015, pad=0.04)
cbar.set_clim(0, 1)

# Plot options
plt.margins(0,0)
plt.axis('off')# Save as high quality png
plt.savefig('springlayout' + '.png', dpi=1000)

