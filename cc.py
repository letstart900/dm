import pandas as pd

from itertools import combinations

df = pd.read_csv('DS1.csv',header=None)
df = df.fillna(0)
transactions = df.values.tolist()

for i in range(0,len(transactions)):
  while 0 in transactions[i]:
    transactions[i].remove(0)
transactions

N1 = len(transactions)
s = 0.3

def candidate_1_itemset():
  candidates.append({})
  for l in transactions:
    for x in l:
      if x in candidates[0]:
        candidates[0][x] += 1
      else:
        candidates[0][x] = 1
  print(candidates[0])

def candidate_2_itemset():
  c2=list(combinations(frequentItemSets[0],2))
  candidates.append({})
  for x in c2:
    candidates[1][x]=0
  for subset in candidates[1]:
    for i in range(0,len(transactions)):
      if set(subset).issubset(set(transactions[i])):
        candidates[1][subset]+=1
  print(candidates[1])

def frequentItemSetGeneration(C):
  L = [x for x in C if (C[x]/N1)>=s]
  L.sort()
  return L

def candidateSetGeneration(L):
  C = {}
  for i in range(0,len(L)):
    for j in range(i+1,len(L)):
      if L[i][0:len(L[i])-1] == L[j][0:len(L[j])-1]:
        string = set(list(L[i]) + list(L[j]))
        sets = combinations(string,len(L[i]))
        flag = 0
        for each in sets:
          lis = list(each)
          lis.sort()
          if tuple(lis) not in L:
            flag=1
            break
        if flag == 0:
          string = list(string)
          string.sort()
          C[tuple(string)]=0
  for subset in C:
    for i in range(0,len(transactions)):
      if set(subset).issubset(set(transactions[i])):
        C[subset]+=1
  return C

candidates = []
frequentItemSets = []
print('Candidate 1-itemset:')
candidate_1_itemset()
print('Frequent 1-itemset:')
frequentItemSets.append(frequentItemSetGeneration(candidates[0]))
print(frequentItemSets[0])
print('Candidate 2-itemset:')
candidate_2_itemset()
print('Frequent 2-itemset:')
frequentItemSets.append(frequentItemSetGeneration(candidates[1]))
print(frequentItemSets[1])
flag = True
i = 0
while flag:
  i = i+1
  print('Candidate ',i+2,'-itemset:')
  candidates.append(candidateSetGeneration(frequentItemSets[i]))
  print(candidates[i+1])
  print('Frequent ',i+2,'-itemset:')
  freq = frequentItemSetGeneration(candidates[i+1])
  if freq == []:
    flag = False
  frequentItemSets.append(freq)
  print(frequentItemSets[i+1])

f=open("Frequent Item Sets.txt","w")
for i in range(0,len(frequentItemSets)):
    f.write("%s => %s\n" %('L'+str(i+1) ,str(frequentItemSets[i])))   
f.close()   
print(frequentItemSets)

def association(Total_candidate,L,C,conf):
    A={}
    for i in L:
         for j in range(1,len(i)):
             for combination in combinations(i,j):
                 s=set(combination)
                 l=set(i)
                 subset2=l.difference(s)
                 l_s=tuple(sorted(subset2))
                 if len(l_s)==1:
                    l_s=l_s[0]
                 A[tuple(s),l_s]=C[i]/Total_candidate[l_s]  
                 if A[tuple(s),l_s]<conf:
                      del A[tuple(s),l_s]
    for i in A:
      print(i[0],"=>",i[1],":",A[i])
    return A

conf=0.7  
C = {}
for i in range(0,len(candidates)):
  C.update(candidates[i])
A={}
for i in range(1,len(candidates)):
  A.update(association(C,frequentItemSets[i],candidates[i],conf))
f=open("Association Rules.txt","w")
for rule in A:
    f.write("%s => %s : %f\n" %(str(rule[0]) ,str(rule[1]),A[rule]))
f.close()
