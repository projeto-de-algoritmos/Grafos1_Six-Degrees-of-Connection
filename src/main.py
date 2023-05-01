import numpy as np
import pandas as pd 
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')  # switch to TkAgg backend
import matplotlib.pyplot as plt
import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename)) 
        
nodes = pd.read_csv('./dataset/nodes.csv')
edges = pd.read_csv('./dataset/edges.csv')
hero_network = pd.read_csv('./dataset/hero-network.csv')
print(nodes.head())
print(edges.head())
print(hero_network.head())

Thor = hero_network[hero_network['hero1']=='THOR/DR. DONALD BLAK'].sample(25)
Cap = Subset = hero_network[hero_network['hero1']=='CAPTAIN AMERICA'].sample(25)
IronMan = hero_network[hero_network['hero1'].str.contains('IRON MAN/TONY STARK')].sample(25)

Subset = pd.concat([Thor,Cap,IronMan],axis = 0)


G=nx.from_pandas_edgelist(Subset, 'hero1', 'hero2')
plt.figure(figsize = (20,20))
nx.draw(G, with_labels=True, node_size=8, node_color='red', edge_color='blue')
plt.show(block=True)