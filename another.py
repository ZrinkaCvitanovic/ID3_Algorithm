import sys
import math
import copy

examples = list()
x = list() #xi attributes
values = dict() #values for each xi and y
y = None
nodes = list()
subtrees = dict()

def read_csv(file):
    global x
    global y
    with open(file, "r") as data:
            for line in data:
                line = line.strip().split(",")
                if len(x) == 0:
                    x = line[0:-1:] 
                    y = line[-1]
                else:
                    examples.append(line)
def define_values():
    for e in examples:
        for i in range (len(x) + 1):
            current_value = e[i]
            if i == len(x):
                current_attr = y
            else:
                current_attr = x[i]
            if current_attr not in values.keys():
                values[current_attr] = set()
            values[current_attr].add(current_value)
class Leaf:
    def __init__(self, decision):
        self.decision = decision
        
    def print(self):
        print(self.decision)
        
class Node:
    def __init__(self, x, subtrees):
        self.x = x
        self.subtrees = subtrees  
    
    def print(self):
        print(self.x)       
        for el in subtrees:
            if el.x is not None:
                print(el.x, end= " ")
        
class ID3_Algorithm:
    def __init__(self):
        nodes = list()


    def find_entropy(self, values):
        entropy_value = 0.0
        total_instances = 0.0
        for v in values:
            total_instances += v
        
        total_instances = float(total_instances)
        for v in values:
            probability = v / total_instances
            entropy_value -= probability * math.log2(probability)
        return entropy_value
        

    def find_greatest_ig(self, D, values_r):
        minimum = None
        max_arg = None
        global nodes
        for attr in values_r.keys():
            try:
                i = x.index(attr)
            except:
                break
            current_sum = 0.0
            for value in values_r[attr]: 
                D_reduced = list()
                for a in D:
                    if a[i] == value:
                        D_reduced.append(a)
                values_y = dict()
                share = 0.0
                last_value = None
                for el in D_reduced: 
                    current_y = el[-1]
                    if current_y not in values_y:
                        values_y[current_y] = 0
                    values_y[current_y] += 1
                    last_value = current_y
                    share += 1
                    
                entropy = self.find_entropy(values_y.values())
                if entropy == 0:
                    continue
                else:
                    share = share / len(D)
                    current_sum += share * entropy 
            if minimum is None or current_sum < minimum:
                minimum = current_sum
                max_arg = attr
        return max_arg
    
    def most_common_y(self, D):
        values_y = dict()
        for d in D:
            current_y = d[-1]
            if current_y not in values_y:
                values_y[current_y] = 0
            values_y[current_y] += 1
        
        maximum = 0
        most_frequent = None
        for value, count in values_y.items():
            if count > maximum:
                maximum = count
                most_frequent = value
        return values_y, most_frequent
    
    def search(self, D, Dp, features, values_r, parent_node=None):
        global subtrees
        if len(D) == 0:
            _, v = self.most_common_y(Dp)
            return subtrees
        values_y, v = self.most_common_y(D)
        if features is None or len(features) == 0: #fali još jedan uvjet
            return subtrees
        current_entropy = self.find_entropy(values_y.values())
        if current_entropy == 0:
            if parent_node is not None:
                subtrees[parent_node].append(v)
            return subtrees
        next_node = self.find_greatest_ig(D, values_r)
        copy_features = copy.deepcopy(features)
        index = copy_features.index(next_node)
        del copy_features[index]
        values_r_copy = copy.deepcopy(values_r)
        del values_r_copy[next_node]
        index = x.index(next_node)
        for value in values[next_node]:
            keyname = next_node + "_" + value
            if parent_node is None:
                if keyname not in subtrees.keys():
                    subtrees[keyname] = list()
            else:
                if parent_node not in subtrees.keys():
                    subtrees[parent_node] = list()
                subtrees[parent_node].append(keyname)
            D_child = list()
            for el in D:
                if el[index] == value:
                    D_child.append(el)
            if parent_node is None:
                t = self.search(D_child, D, copy_features, values_r_copy, keyname)
            else:
                t = self.search(D_child, D, copy_features, values_r_copy, parent_node)
        return subtrees
        
            
    def fit(self, training_set):
        read_csv(training_set)
        define_values()
        features = copy.deepcopy(x)
        values_r = copy.deepcopy(values) 
        subtrees = self.search(examples, examples, features, values_r, None)
        return subtrees
                
    def predict(self, testing_set):
        read_csv(testing_set)
        result = None 
            
if __name__ == "__main__":
        ID3 = ID3_Algorithm()
        #training_dataset = sys.argv[1]
        #testing_dataset = sys.argv[2]
        training_dataset = "abcdef.csv"
        #testing_dataset = "test.csv"
        print("[BRANCHES]:")
        subtrees = ID3.fit(training_dataset)
        for tree in subtrees.keys():
            attr, val = tree.split("_")
            node = subtrees[tree]
            counter = 1
            term = True
            for i in range(len(node)):
                if term == True:
                    counter = 1
                    print(f"{counter}: {attr}={val}", end= " ")
                n = node[i].split("_")
                if len(n) == 1:
                    print(f"{n[0]}")
                    term = True
                else:
                    counter += 1
                    print(f"{counter}:{n[0]}={n[1]}", end= " ")
                    term = False
                    
                
        print("[PREDICTIONS]:", end=" ")
        #ID3.predict(testing_dataset)