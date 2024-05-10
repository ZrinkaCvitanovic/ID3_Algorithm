import sys


examples = list()
x = list()
y = None

def read_csv(file):
    global x
    with open(file, "r") as data:
            for line in data:
                line = line.strip().split(",")
                if len(x) == 0:
                    x = line[0:-1:] 
                    y = line[-1]
                else:
                    examples.append(line)


class Leaf:
    def __init__(self, value):
        decision = value
        
class Node:
    def __init__(self, x, subtrees):
        
        
class ID3_Algorithm:
    def __init__(self):
        nodes = list()
    
    
    def IG(self, X):
        # save all values of IG
        # return maximum
    
    def argmax(set, target, value):
        maximum = None
        for unit in set:
            if target == value:
                if maximum is None or value > maximum:
                    maximum = target
        return maximum
                
    
    def search(self, D, Dp, X, y):
        if len(D) == 0 or len(X) == 0:
            v = argmax(Dp, y, v) #figure out which argument this is
            return Leaf(v)
        
        x = IG(X)
        
        for v in V(x): #calculate all possible values of this x and return it in this function
            Dp = D
            D = D #remove current feature
            X = X #remove current x
            x = search(D, D, X, y)
            subtrees.append(x)
        return Node(x, subtrees)
        
            
    def fit(self, training_set):
        read_csv(training_set)
        for example in examples:
            search(x, x, example, y)
                
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