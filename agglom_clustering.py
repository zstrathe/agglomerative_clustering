### Agglomerative clustering 
### Using total-linkage and manhattan or euclidean distance

import numpy as np
from math import sqrt

def print_clusters(clusters_dict):
  for i, (key, values) in enumerate(clusters_dict.items()):
    print(f'Cluster {key}:', end=' ')
    for i in range(len(values)): 
      if i == len(values)-1:
        print(values[i])
      else:
        print(values[i], end=', ')
  print('')

def agglom_clustering(starting_points, dist='euclidean'):
  print(f'Agglomerative clustering with {dist} distance calculation')
  # Initially set each starting point as its own cluster
  clusters = {}
  for idx,key in enumerate(starting_points):
    clusters[idx+1] = key
  
  iter_count = 1   ## start a counter to keep track of clustering step for output
  print('Starting clusters:')
  print_clusters(clusters)

  while len(clusters) > 1: 
    distances = [] 
    # Get the total-linkage distance between all clusters
    for i, (ik, cluster_points_i) in enumerate(clusters.items()): # start with the first cluster
      for j, (jk, cluster_points_j) in enumerate(clusters.items()): # next select the other cluster to calculate distances with
        if ik == jk: # skip if selected the same cluster twice
          continue
        else:
          if {ik, jk} not in distances or {jk, ik} not in distances: # check if this cluster pair has not already been calculated
            ''' 
            For each point in the first cluster, compare with each point in the second cluster 
            and calculate the manhattan distance between them by using coordinates from the 'orig_points' dict.
            To get the total-linkage value, keep track of distances between all point-pairs in 'temp_distances' list, then select the highest value
            '''
            temp_distances = []
            for points_i in cluster_points_i: 
              for points_j in cluster_points_j:
                #print(points_i, points_j, ':', end=' ')
                if dist == 'euclidean':
                  dist_calc = sqrt(abs(orig_points[points_i][0] - orig_points[points_j][0])**2 + abs(orig_points[points_i][1] - orig_points[points_j][1])**2)   
                elif dist == 'manhattan':
                  dist_calc = abs(orig_points[points_i][0] - orig_points[points_j][0]) + abs(orig_points[points_i][1] - orig_points[points_j][1])
                else:
                  print('Provide \'euclidean\' or \'manhattan\' only for dist parameter')
                  return None
                #print(dist_calc)                                                                                                  
                temp_distances.append(dist_calc)  
            #print(f'{ik} & {jk}: {temp_distances}')
            #print(temp_distances[np.argmax(temp_distances)])

            # Append the cluster pair as ((Cluster1, Cluster2), the highest value distance between points) to the main distances list
            distances.append(((ik, jk), temp_distances[np.argmax(temp_distances)])) 

    # Find the cluster-pair with the lowest distance 
    # by iterating through the distances list
    min_dist = distances[0] # initially set the first cluster-pair as the minimum distance
    for i in distances:
      if i[1] < min_dist[1]:
        min_dist = i # update minimum distance cluster-pair
  
    print(f'Step {iter_count}: merge clusters {min_dist[0][0]} and {min_dist[0][1]}, with a distance of {float(min_dist[1])}')

    #print(clusters[min_dist[0][0]])
    #print(clusters[min_dist[0][1]])
    clusters[min_dist[0][0]] = clusters[min_dist[0][0]] + clusters[min_dist[0][1]] # merge the clusters
    del clusters[min_dist[0][1]] # delete the cluster that was merged into the other
    print(f'New clusters:')
    print_clusters(clusters)
    iter_count += 1


orig_points = {'1':(1, 2), '2':(2.5, 4.5), '3':(2,2), '4':(4,1.5), '5':(4,2.5)} 
agglom_clustering(orig_points, dist='euclidean')