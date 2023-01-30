import itertools
import pandas as pd

'''
trans =  [[1, 2, 5],
[2, 4],
[2, 3],
[1, 2, 4],
[1, 3],
[2, 3],
[1, 3],
[1, 2, 3, 5],
[1, 2, 3]]

trans = [[1,2],
         [2,4],
         [2,3],
         [1,2,4],
         [1,3],
         [2,3],
         [1,3],
         [1,2,3,5],
         [1,2,3]]
'''
sup = 0.40
minConf = 0.60


def isPresent(sub, trans):
    return all(elem in trans for elem in sub)


def Pruning(Cand, supCand):
    return [Cand[i] for i in range(len(supCand)) if supCand[i] >= sup]


def GenerateFreqItemset(LkPrev, Lk, supC, trans, NumTrans):
    while (len(Lk[-1]) != 0):
        Ck = [list(set(LkPrev[i]+LkPrev[j])) for i in range(len(LkPrev))
              for j in range(i+1, len(LkPrev)) if LkPrev[i][:-1] == LkPrev[j][:-1]]
        supCk = [
            round(sum([1 for t in trans if isPresent(i, t)])/NumTrans, 2) for i in Ck]
        supkDict = {str(Ck[i]): supCk[i] for i in range(len(Ck))}
        supC.append(supkDict)
        L = Pruning(Ck, supCk)
        Lk.append(L)
        LkPrev = Lk[-1]
    return Lk


def sub_lists(l):
    comb = []
    for i in range(1, len(l)+1):
        comb += [list(j) for j in itertools.combinations(l, i)]
    return list(filter(None, comb))


def list_diff(li1, li2):
    return list(set(li1).symmetric_difference(set(li2)))

# Association Rule Mining
def Association_Rules(Freq, minConf, supCnt):
    rules = []
    # Freq: all k-freq itemsets [k>1]
    Freq = [j for sub in Freq for j in sub]
    for i in range(len(Freq)):
        sub = sub_lists(Freq[i])
        subsets = [item for item in sub if item != Freq[i]]
        for j in range(len(subsets)):
            if (len(subsets[j]) != 1):
                if ((supCnt[str(Freq[i])] / supCnt[str(subsets[j])]) >= minConf):
                    rules.append([subsets[j], list_diff(Freq[i], subsets[j])])
            # if subset is single int and not a list of int.
            else:
                if ((supCnt[str(Freq[i])] / supCnt[str(subsets[j][0])]) >= minConf):
                    rules.append([subsets[j], list_diff(Freq[i], subsets[j])])
    return rules


def encoding(uniqueItems):
    uniqueItems.sort()
    encode = {}
    for i in range(len(uniqueItems)):
        encode[uniqueItems[i]] = i
    return encode


def decoding(encoding_dict, itemset):
    decoding_dict = {}
    for key, value in encoding_dict.items():
        decoding_dict[value] = key
    print(decoding_dict)
    decoded_freq_item_set = []
    for freq in itemset:
        L = []
        for items in freq:
            lst = []
            for ele in items:
                lst.append(decoding_dict[ele])
            L.append(lst)
        decoded_freq_item_set.append(L)

    return decoded_freq_item_set


def main():
    df = pd.read_csv("ds1.csv", header=None)
    df = df.dropna()
    # transaction = list(df.groupby(['Transaction'])['Item'].apply(list))
    transaction = df.values.tolist()
    print('Transactions:')
    for t in transaction:
        print(t)
    uniqueItems = list(set(item for i in transaction for item in i))
    encode = encoding(uniqueItems)
    trans = [[encode[j] for j in i] for i in transaction]
    print('\nEncoding :', encode)
    # dfEnc = df.copy()
    # encode = {"Bread":1, "Cola":2, "Diapers":3, "Eggs":4, "Jam":5, "Milk":6}
    # dfEnc = dfEnc.replace(encode).dropna()
    # transac = dfEnc.values.tolist()
    # trans = [[int(x) for x in item] for item in transac]
    print("\nTransactions Encoded:")
    for t in trans:
        print(t)
    NumTrans = len(trans)

    # trans - a 2d list of transactions
    C1 = list(set(x for l in trans for x in l))
    supC1 = [round(sum([t.count(i) for t in trans])/NumTrans, 2) for i in C1]
    sup1Dict = {str(C1[i]): supC1[i] for i in range(len(C1))}
    L1 = Pruning(C1, supC1)

    C2 = [list(comb) for comb in itertools.combinations(L1, 2)]
    supC2 = [round(sum([1 for t in trans if isPresent(i, t)])/NumTrans, 2)
             for i in C2]
    sup2Dict = {str(C2[i]): supC2[i] for i in range(len(C2))}
    L2 = Pruning(C2, supC2)

    Lk = [[L1], L2]
    supC = [sup1Dict, sup2Dict]
    Lk = GenerateFreqItemset(L2, Lk, supC, trans, NumTrans)
    supCnt = {k: v for d in supC for k, v in d.items()}
    FreqItemset = list(filter(None, Lk))

    # reomving the 1-freq as they dont have any subset
    Freq = list(filter(None, Lk[1:]))
    Rules = Association_Rules(Freq, minConf, supCnt)

    print("\nFrequent Itemsets using Apriori (ordinality wise): ")
    for i in range(len(FreqItemset)):
        print(f'L{i+1}: {FreqItemset[i]}')

    print('\nDecoded Frequent Itemsets using Apriori Algorithm:')
    decoded_FreqItemSet = decoding(encode, FreqItemset)
    for i in range(len(decoded_FreqItemSet)):
        print(f'L{i+1}: {decoded_FreqItemSet[i]}')
    
    # write freq itemset to a file
    f = open("FrequentItemset.txt", "w")
    for item in decoded_FreqItemSet:
        f.write("%s\n" % item)
    f.close()


    
    print('\nAssociation Rules ordinality wise')
    for i in Rules:
        print(i[0], "->", i[1])

    print('\nAssociation Rules Decoded')
    decoded_rules = decoding(encode, Rules)
    for a, b in decoded_rules:
        print(a, '->', b)

    # write association rules to file
    f = open("AssociationRules.txt", "w")
    for rule in decoded_rules:
        f.write("%s\n" % rule)
    f.close()


main()
