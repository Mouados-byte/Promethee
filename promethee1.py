from matplotlib import pyplot as plt
import numpy as np
import networkx as nx

class Promethee1:
    def __init__(self, criteria, alternatives, weights = None, direction = None, labels = None, flows = None, preference = None):
        self.criteria = criteria
        self.alternatives = alternatives
        self.labels = [i for i in range(len(criteria))] if labels is None else labels
        self.weights = [1 for i in range(len(criteria))] if weights is None else weights
        self.direction = ["max" for i in range(len(criteria))] if direction is None else direction
        self.compared_alterantives = [[0 for i in range(len(alternatives))] for j in range(len(alternatives))]
        self.preference = [[0 for i in range(len(alternatives))] for j in range(len(alternatives))] if preference is None else preference
        self.flows = [[0 for i in range(len(alternatives))] for j in range(2)] if flows is None else flows
        self.ranking = [0 for i in range(len(alternatives))]
        self.graph = {}

    def set_weights(self, weights):
        self.weights = weights

    def set_flows(self, flows):
        self.flows = flows
        
    def calculate_preference(self):
        max_value = [max(np.transpose(self.alternatives)[i]) for i in range(len(self.criteria))]
        min_value = [min(np.transpose(self.alternatives)[i]) for i in range(len(self.criteria))]
        for i in range(len(self.alternatives)):
          for j in range(len(self.criteria)):
            self.compared_alterantives[i][j] = max_value[j] - self.alternatives[i][j] if self.direction[j] == "min" else self.alternatives[i][j] - min_value[j]
            self.compared_alterantives[i][j] /= max_value[j] - min_value[j]

        for i in range(len(self.compared_alterantives)):
            for j in range(len(self.compared_alterantives)):
                if i == j:
                  continue
                for k in range(len(self.criteria)):
                    if self.compared_alterantives[i][k] > self.compared_alterantives[j][k]:
                        self.preference[i][j] += (self.compared_alterantives[i][k] - self.compared_alterantives[j][k]) * self.weights[k]
        return self.preference
        
    def calculate_flows(self):
      sum_weights = sum(self.weights)
      for i in range(len(self.preference)):
          for j in range(len(self.preference)):
              if i == j:
                  continue
              self.flows[0][i] += self.preference[i][j] / sum_weights
              self.flows[1][i] += self.preference[j][i] / sum_weights
      return self.flows
    
    def determine_preference(self, a, b):
      if a[0] == b[0] and a[1] == b[1]:
        return [0, "I"]
      
      if (a[0] > b[0] and a[1] > b[1]) or (a[0] < b[0] and a[1] < b[1]):
        return [0, "R"]

      if (a[0] > b[0] and a[1] < b[1]) or (a[0] > b[0] and a[1] == b[1]) or (a[0] == b[0] and a[1] < b[1]):
        return [0, "P"]
      else:
        return [1, "P"]

    def draw_graph(self):
        graph = {}
        for i in self.labels:
            graph[i] = []
        flows = dict(zip(self.labels, np.transpose(self.flows)))
        print(flows)
        
        for i in self.labels:
          for j in self.labels:
            if i == j or (j in graph and i in graph[j]) or (i in graph and j in graph[i]):
                continue
            result = self.determine_preference(flows[i], flows[j])
            source = i if result[0] == 0 else j
            target = j if result[0] == 0 else i
            
            # Add the edge to the graph
            temp = source
            source = target
            target = temp
            match result[1]: 
              case "R":
                continue
              case "P":
                if source in graph:
                  graph[source].append(target)
                else:
                  graph[source] = [target]
              case "I":
                if source in graph:
                  graph[source].append(target)
                else:
                  graph[source] = [target]
                if target in graph:
                  graph[target].append(source)
                else:
                  graph[target] = [source]
        self.graph = graph
        self.draw()
        return self.graph
    
    def process_promethee(self):
        self.calculate_preference()
        self.calculate_flows()
        return self.draw_graph()
        
    def draw(self):
      graph = nx.DiGraph(self.graph)
      nx.draw_networkx(graph, with_labels=True)
      plt.show()
      return self.ranking