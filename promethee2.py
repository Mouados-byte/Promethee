import numpy as np

class Promethee2:
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

    def calculate_ranking(self):
        for i in range(len(self.flows[0])):
          self.ranking[i] += self.flows[0][i] - self.flows[1][i]
        return self.get_ranking()
      
    
    def process_promethee(self):
        self.calculate_preference()
        self.calculate_flows()
        return self.calculate_ranking()
        
    def get_ranking(self, with_values = False):
      ranking = dict(zip(self.labels, self.ranking))
      sorted_ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
      return sorted_ranking if with_values else list(sorted_ranking.keys())