# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 22:06:46 2023

@author: varna s
"""
import itertools
def subsetgeneration(L):
    C=[]
    for i in range(0,len(L)):
      for j in range(i+1,len(L)):
        if L[i][0:len(L[i])-1]==L[j][0:len(L[j])-1]:
          string=list(set(list(L[i])+list(L[j])))
          string.sort()
          C.append(list(string))
    return C

def apriori(C_list,r,L):
    C={}
    for i in range(0,len(C_list)):
      C[tuple(C_list[i])]=0
      for combination in itertools.combinations(C_list[i],r):
        if combination not in L:
          del C[tuple(C_list[i])]
    return C
          
def supcount(C,df):
    for s in C:
      for i in range(0,len(df)):
        if set(s).intersection(set(df[i]))==set(s):
          C[s]+=1    
    return C

def association(Total_candidate,L,C,conf):
    A={}
    for i in L:
         for j in range(1,len(i)):
             for combination in itertools.combinations(i,j):
                 v=set(combination)
                 s=set(i)
                 subset2=s.difference(v)
                 c=tuple(sorted(subset2))
                 if len(c)==1:
                    c=c[0]
                 A[tuple(v),c]=C[i]/Total_candidate[c]   
                 if A[tuple(v),c]<conf:
                      del A[tuple(v),c]
    for i in A:
      print(i[0],"=>",i[1],":",A[i])
      
    return A
                     
                      
import pandas as pd
from itertools import chain
from itertools import combinations

df=pd.read_csv(r'C:\Users\varna s\Downloads\Transaction.csv',header=None)
df=df.fillna(0)
df=df.values.tolist()

# df2 = pd.read_csv(r'C:\Users\varna s\Downloads\Transaction1.csv')
# df2 = df2.drop(df2[df2.Item == "NONE"].index)
# df2['Datetime'] = pd.to_datetime(df2["Date"]+' '+df2["Time"])
# main_df = df2[['Datetime','Item']].groupby(['Datetime'])['Item'].apply(list)
# transactions = list(main_df)
# df=transactions

for i in range(0,len(df)):
  if 0 in df[i]:
    df[i].remove(0)
    
I=list(set(chain(*df)))
support=0.3
#generating 1 candidate list
C1={}
for x in I:
  sum=0
  for i in range(0,len(df)):
    if x in df[i]:
      sum=sum+1
  C1[x]=sum
L1=[ x for x in C1 if C1[x]/len(df)>=support]
L1.sort()
print("1 frequent itemset\n", L1)

#generating 2 candidate list
C2_list=list(combinations(L1,2))
C2={}
for x in C2_list:
  C2[x]=0
  
for s in C2_list:
  for i in range(0,len(df)):
    if set(s).intersection(set(df[i]))==set(s):
      C2[s]+=1      
L2=[x for x in C2 if C2[x]/len(df)>=support]
print("2 frequent itemset \n",L2)

#generating 3 candidate list
C3_list=[]
C3_list=subsetgeneration(L2)
C3=apriori(C3_list,2,L2)
C3=supcount(C3,df)  
L3=[x for x in C3 if C3[x]/len(df)>=support]
print("3 frequent itemset \n",L3)

#generating 4 candidate list
C4_list=[]
C4_list=subsetgeneration(L3)
C4=apriori(C4_list,3,L3)
C4=supcount(C4,df)
L4=[x for x in C4 if C4[x]/len(df)>=support]
print("4 frequent itemset",L4)

Frequent_Itemset=L1+L2+L3+L4
s=open("Frequent Itemset.txt","w")
for rule in Frequent_Itemset:
    s.write("%s \n" % str(rule))
        
s.close()        
conf=0.7  
#association rules
Total_candidate=C1|C2|C3|C4 
A2=association(Total_candidate, L2, C2,conf)
A3=association(Total_candidate, L3, C3,conf)
A4=association(Total_candidate, L4, C4,conf)
A=A2|A3|A4
f=open("Association Rules.txt","w")
for rule in A:
    f.write("%s => %s : %f\n" %(str(rule[0]) ,str(rule[1]),A[rule]))
        
f.close()        
        
        
        