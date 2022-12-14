# -*- coding: utf-8 -*-
"""Teamcluster_ruleminer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RB77XgrAlSpfHMn6k-47SANgN686q96K
"""

#connecting to the drive..
#from google.colab import drive
#drive.mount('/content/drive')

#required packages...
import pandas as pd
import numpy as np
import random 
import itertools
import copy
import sys

#loading data
ratings_df = pd.read_csv(sys.argv[0])

"""**Preprocessing of data**"""

#converting data into numpy array...
ratings_arr = ratings_df.to_numpy()

for i in ratings_arr:
  print(i)
  break

type(ratings_df['movieId'][0])

#considering the movies that were rated above 2....
movies_db={}

for i in ratings_arr:
  if(i[2]>=2):
    if i[0] in movies_db:
      movies_db[i[0]].append(i[1])
    else:
      l = [i[1]]
      movies_db[i[0]] = l

#considering only the users who rated more than 10 movies.....
refined_movies_db={}

for key,value in movies_db.items():
  if(len(value)>=10):
    refined_movies_db[key]=value

del movies_db

#splitting of data into 80% train set 20% test set as given in the question....
train_set = {}
test_set = {}

for key,value in refined_movies_db.items():
  k = int(len(value)*0.2)
  list1 = random.sample(value,k);
  list1.sort()
  test_set[key] = list1
  list1 = list(set(value) - set(list1))
  list1.sort()
  train_set[key] = list1

#converting to sets from list for easy computations
set_train_set = {}
for key,values in train_set.items():
  set_train_set [key] = set(values)

data = []
data.append(train_set)
data.append(test_set)
data.append(set_train_set)
f = open('test_data.npy','wb')
np.save(f,data)
f.close()

#a function of calcualting all the one sized frequent itemsets
def find_frequent_1_itemsets(train_set,min_sup,total_count):
  movies = {}
  #calculating C1 by scanning all the database...
  for key,value in train_set.items():
    for val in value:
      if val in movies:
        movies[val]+=1
      else:
        movies[val]=1
  movies_list = []
  for key,value in movies.items():
    if (value/total_count) >=min_sup :
      list1 = [key,value]
      movies_list.append(list1)
  movies_list.sort()
  return movies_list

#a function that is defined to check the generated itemset have all its subsets are frequent 
def has_frequent_subset(cik,lk,k):
  subsets = [tuple(i) for i in itertools.combinations(cik, k-1)]
  subset = set(subsets)
  return subset.intersection(lk) ==subset

#a function that generates the Ck from Lk-1 which also inherently calls the pruning component
def apriori_gen(lk,k):
  temp_lk = []
  ck = []
  for i in lk:
    temp_lk.append(i[:-1])
  set_temp_lk = []
  for i in temp_lk:
    set_temp_lk.append(tuple(i))
  set_temp_lk = set(set_temp_lk)
  n = len(lk)
  for i in range(n):
    for j in range(i+1,n):
      if lk[i][:-2]==lk[j][:-2]:
        c=[]
        c = list(temp_lk[i])
        c.append(temp_lk[j][-1])
        if has_frequent_subset(c,set_temp_lk,k):
          c.sort() 
          ck.append(c)
  return ck

#taking min_sup as 0.1 and min_conf as 0.1
min_sup = 0.1
total_count = 0.0
min_conf = 0.1
for key,value in train_set.items():
  total_count+=1

#driver code for calculating one item sets
L1 = find_frequent_1_itemsets(train_set,min_sup,total_count)

#apiori method
k=2
lk=L1
L=[]
L.append(lk)
while len(lk)>0:
  ck = apriori_gen(lk,k)
  ck.sort()                                        #generation of the Ck 
  counts = [0 for i in range(len(ck))]
  for ind in range(len(ck)):                                    #scanning the database for calculating the counts of the c that were generated
    set_ck = set(ck[ind])
    for value in set_train_set.values():
      if set_ck.intersection(value)==set_ck:
        counts[ind]+=1
  lk=[]
  print("before:",k,":",len(ck))
  for i in range(len(ck)):                                      #generating Lk by removing the itemsets int ck that are not frequent 
    if counts[i]/total_count >= min_sup:
      ck[i].append(counts[i])
      lk.append(ck[i])
  print("after:",k,":",len(lk)) 
  k=k+1
  L.append(lk)                                                 #appending each Lk to the L.

#storing in the file for the further use....
f = open('out1.npy','wb')
np.save(f,L)
f.close()

"""##Generating association rules"""

#loading the data of the L 
f = open('out1.npy','rb')
L = np.load(f,allow_pickle=True)

#generation of subsets of size n-1
def get_single_drop_subsets(item_set):

    single_drop_subsets = list()
    X = []

    for item in item_set:
        temp = item_set.copy()
        X.append(item)
        temp.remove(item)
        single_drop_subsets.append(temp)
        
    return single_drop_subsets, X

#a function for getting the support....
def get_support(y,level,L):

  for item_set in L[level]:
    if(item_set[:-1] == y):
      return item_set[-1]

#a function for generating all the association rules....
def generate_associations(L):

  support = []
  confidence = []

  rules_sup = []
  rules_conf = []
  for level in range(1,len(L)-1):
    p=0
    for item in L[level]:
      p+=1
      Y,X = get_single_drop_subsets(item[:-1])
      xy_sup = item[-1]

      for i in range(len(Y)):
        x_sup = get_support(X[i],0,L)

        support.append(xy_sup/total_count)
        l =[]
        l.append(X[i])
        l.append(Y[i])
        rules_sup.append(l)

        conf = (xy_sup)/x_sup

        if(conf >= min_conf):
          confidence.append(conf)
          l =[]
          l.append(X[i])
          l.append(Y[i])
          rules_conf.append(l)
  return support,confidence,rules_sup,rules_conf

support,confidence,rules_sup,rules_conf = generate_associations(L)

#storing the generated association rules for the recommendations.....
d = []
d.append(support)
d.append(confidence)
d.append(rules_sup)
d.append(rules_conf)
f.close()
f = open('rules.npy','wb')
np.save(f,d)
f.close()

