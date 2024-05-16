import sys
import math
import copy

examples = list()
x = list()
values = dict() #values for each xi and y
values_r = list()
y = None
subtrees = set()
nodes = list()

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
    def __init__(self, value):
        self.decision = value
        
class Node:
    def __init__(self, x, subtrees):
        self.x = x
        self.subtrees = subtrees
        
        
class ID3_Algorithm:
    def __init__(self):
        nodes = list()
    
    
   #def IG(self, X):
        # save all values of IG
        # return maximum
    
    def argmax(self, given_set):
        maximum = None
        for unit in given_set:
            if target == value:
                if maximum is None or value > maximum:
                    maximum = target
        return maximum

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
        

    def find_greatest_ig(self, D, values_r, start_entropy):
        minimum = None
        max_arg = None
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
               # D_reduced = {a for a in D if a[i] == value}
                values_y = dict()
                share = 0.0
                for el in D_reduced: 
                    current_y = el[-1]
                    if current_y not in values_y:
                        values_y[current_y] = 0
                    values_y[current_y] += 1
                    share += 1
                    
                entropy = self.find_entropy(values_y.values())
                share = share / len(D)
                current_sum += share * entropy 
            if minimum is None or current_sum < minimum:
                minimum = current_sum
                max_arg = attr
        return max_arg, minimum
    
    def most_common_y(self, D):
        values_y = dict()
        for d in D:
            current_y = d[-1]
            if current_y not in values_y:
                values_y[current_y] = 0
            values_y[current_y] += 1
        
        v = 0
        for value, count in values_y.items():
            if count > v:
                v = count
                most_frequent = value
        return values_y, most_frequent
    
    def search(self, D, Dp, features, y, values_r):
        global nodes, subtrees
        if len(D) == 0:
            _, v = self.most_common_y(Dp)
            return Leaf(v)
        #Dp = {x for x in D if x[-1] == v}
        values_y, v = self.most_common_y(D)
        
        if features is None or len(features) == 0: #or ovaj drugi uvjet
            return Leaf(v)

        start_entropy = self.find_entropy(values_y.values())
        next_node, result_entropy = self.find_greatest_ig(D, values_r, start_entropy)
        nodes.append(next_node) #the value with greatest information gain
        if result_entropy == 0.0:
            res = Leaf(D[0][-1])
            print(res.decision)
            return Leaf(D[0][-1])
        #razdvajanje po varijabli next_node
        for val in values[next_node]:
            global x
            position = x.index(next_node)
            D_child = list()
            for a in D:
                if a[position] == val:
                    D_child.append(a)
            index = features.index(next_node)
            del features[index]
            del values_r[next_node]
            t = self.search(D_child, D, features, y, values_r)
            #subtrees[].append(t)
            #subtrees.append(subtrees, (v, t))
        return Node(z, subtrees)
        
            
    def fit(self, training_set):
        read_csv(training_set)
        define_values()
        features = copy.deepcopy(x)
        values_r = copy.deepcopy(values) 
        self.search(examples, examples, features, y, values_r)
                
    def predict(self, testing_set):
        read_csv(testing_set)
        result = None 
            
if __name__ == "__main__":
        ID3 = ID3_Algorithm()
        #training_dataset = sys.argv[1]
        #testing_dataset = sys.argv[2]
        training_dataset = "data.csv"
        #testing_dataset = "test.csv"
        ID3.fit(training_dataset)
        #ID3.predict(testing_dataset)