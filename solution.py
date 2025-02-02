import math
import copy
import sys

examples = list()
examples_test = list()
predictions = list()
x = list()
values = dict() 
y = None
values_of_y = list()

def read_csv(file, purpose="train"):
    global x, y
    global examples, examples_test
    with open(file, "r") as data:
            for line in data:
                line = line.strip().split(",")
                if len(x) == 0:
                    x = line[0:-1:] 
                    y = line[-1]
                else:
                    if purpose == "train":
                        examples.append(line)
                    else:
                        examples_test.append(line)
                    
                    
def define_values():
    for e in examples:
        for i in range (len(x) + 1):
            current_value = e[i]
            if i == len(x):
                current_attr = y
                try:
                    index = values_of_y.index(e[i])
                except:
                    values_of_y.append(e[i])
            else:
                current_attr = x[i]
            if current_attr not in values.keys():
                values[current_attr] = set()
            values[current_attr].add(current_value)
            
            
def print_subtree(data, prefix="", counter=1):
  for i in range(1, len(data), 2):
    subtree = data[i]
    if isinstance(subtree, list):
        if (prefix.endswith("=")):
            print_subtree(subtree, f"{prefix}{data[i-1]} ", counter+1)
        else:
            print_subtree(subtree, f"{prefix}{counter}:{data[i-1]}=", counter)
    else:
      print(f"{prefix}{data[i-1]} {subtree}")            

        
class ID3_Algorithm:
    def __init__(self, limit=None):
        self.limit = limit


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
        y_keys = list(values_y.keys())
        y_keys.sort()
        sorted_dict = {i: values_y[i] for i in y_keys}
        for value, count in sorted_dict.items():
            if count > maximum:
                maximum = count
                most_frequent = value
        return values_y, most_frequent
    
    def search(self, D, Dp, features, values_r, level):
        subtrees = list()
        if len(D) == 0:
            _, v = self.most_common_y(Dp)
            return v
        values_y, v = self.most_common_y(D)
        if features is None or len(features) == 0:
            return v
        current_entropy = self.find_entropy(values_y.values())
        if current_entropy == 0:
            return v
        if self.limit is not None and self.limit == level:
            return v
        next_node = self.find_greatest_ig(D, values_r)
        copy_features = copy.deepcopy(features)
        index = copy_features.index(next_node)
        del copy_features[index]
        values_r_copy = copy.deepcopy(values_r)
        del values_r_copy[next_node]
        index = x.index(next_node)
        for value in values[next_node]:
            D_child = list()
            for el in D:
                if el[index] == value:
                    D_child.append(el)
            t = self.search(D_child, D, copy_features, values_r_copy, level+1)
            subtrees.append(value)
            subtrees.append(t)
        return [next_node, subtrees]
        
            
    def fit(self, training_set):
        read_csv(training_set)
        define_values()
        features = copy.deepcopy(x)
        values_r = copy.deepcopy(values) 
        subtrees = self.search(examples, examples, features, values_r, 0)
        return subtrees
    
    def find_prediction(self, node, example, level):
        current_label = node[0]
        try:
            current_index = x.index(current_label)
        except:
            print(f"{node}", end=" ")
            predictions.append(node)
            return
        if self.limit is not None and level == self.limit:
            _, node = self.most_common_y(examples)
            print(f"{node}", end=" ")
            predictions.append(node)
            return
        current_subtree = node[1]
        if isinstance(current_subtree, list):
            for i in range (0, len(current_subtree), 2):
                if example[current_index] not in values[current_label]:
                    _, node = self.most_common_y(examples)
                    print(f"{node}", end=" ")
                    predictions.append(node)
                    return
                if current_subtree[i] == example[current_index]:
                    self.find_prediction(current_subtree[i+1], example, level+1)
        else:
            print(f"{current_subtree}")
        return
                
    def predict(self, testing_set, node):
        matrix = dict()
        global values_of_y
        values_of_y.sort()
        for value in values_of_y:
            i = values_of_y.index(value)
            matrix[i] = dict()
            for v in values_of_y:
                j = values_of_y.index(v)
                matrix[i][j] = 0
        read_csv(testing_set, "test")
        global examples_test
        accurate = 0.0
        total = float(len(examples_test))-1
        for example in examples_test[1::]:
            self.find_prediction(node, example, 0)
        for index in range (len(predictions)):
            if predictions[index] == examples_test[index+1][-1]:
                accurate += 1
            i = values_of_y.index(predictions[index])
            j = values_of_y.index(examples_test[index+1][-1])
            matrix[i][j] += 1            
        return accurate/total, matrix
        
                   
if __name__ == "__main__":
        training_dataset = sys.argv[1]
        testing_dataset = sys.argv[2]
        try:
            limit = int(sys.argv[3])
        except:
            limit = None           
        ID3 = ID3_Algorithm(limit)
        print("[BRANCHES]:")
        node = ID3.fit(training_dataset)
        print_subtree(node)
        print("[PREDICTIONS]:", end=" ")
        accuracy, matrix = ID3.predict(testing_dataset, node)
        print(f"\n[ACCURACY]:", end=" ")
        print(f"{accuracy:.{5}f}")
        print("[CONFUSION_MATRIX]:")
        for i in matrix.keys():
            for j in matrix.keys():
                print(matrix[j][i], end=" ")
            print()