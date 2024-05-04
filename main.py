from promethee2 import Promethee2
from promethee1 import Promethee1

# Phones based on price, storage, camera and looks
alternatives = [[250, 16, 12, 5], [200, 16, 8, 3], [300, 32, 16, 4], [275, 32, 8, 2]]
# Criteria to compare the alternatives
criteria = ['price', 'storage', 'camera', 'looks']
# labels of the alternatives
labels = ['phone1', 'phone2', 'phone3', 'phone4']
# Minimize or maximize the criteria
direction = ['min', 'max', 'max', 'max']
# Weights for each criteria
weights = [0.35, 0.25, 0.25, 0.15]


promethee1 = Promethee1(criteria, alternatives, weights, direction, labels)
ranking1 = promethee1.process_promethee()
print(ranking1)
promethee2 = Promethee2(criteria, alternatives, weights, direction, labels)
ranking2 = promethee2.process_promethee()
print(ranking2)