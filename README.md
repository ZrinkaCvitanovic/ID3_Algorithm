# ID3 Algoritm
This program is a simple implementation of an ID3 algoritm

## Tehcnical details
All important data for the algorithm is stored in a class so that global variables are avoided and encapsulation is ensured. There is an optional "limit" argument which determined whether the srearch goes on until it reaches the end of the tree or it should be interrupted afeter a certain number of levels. The deafult value of that argument is None.  
The data is in a .csv format. The last column is the target value (the class label).  
This program can be used on many well-known datasets such as _EnjoySport_ (https://ai.vub.ac.be/sites/default/files/concept%20learning%20and%20decision%20trees%20with%20extra%20notes_1.pdf).

## Algorithm flow
The algorithm starts with reading the data and storing them in a dictionary. 
The *fit()* function is here to determine all possible values for each feature in a vector and store all relevant data for calculating entropy and information gain later. 
The *search()* function tries to find the node that gives the greatest information gain and splits the current tree based on the value of that node. The greatest information gain is found by calculating entropy of each node and selecting the one with the mininum entropy. The function goes on recursively until all features have been used for splitting a tree or all data has defined class labels or a limit is reached (if any).  
After that it is time to predict information on other labelled data to test how well our tree predicts values. All the relevant data is printed. 
