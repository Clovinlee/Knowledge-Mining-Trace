# get nth row
# print(df.iloc[4])
# df = df.iloc[0:5]

# get col
# df = df.loc[:,["age","spectacle"]]
# df = df.loc[:,[2,3]]

# Delete column
# df = df.drop(columns=["age"])
# df = df.drop(columns=df.columns[3])

# Delete Row
# df = df.drop([0,1,2])

# Re arrange index to start from 0
# df = df.reset_index(drop=True)

# iloc = df.iloc[Row,Col] in integer

# get column name
# df = df.columns[1] 

# get unique val
# key = (df[keyColumn]).unique()

# get all young
# df = df.loc[df["age"] == "young"]
# df = df.loc[(df["age"] == "young") & (df["spectacle"] == "myope")]

# get all non young
# df = df[df["age"] != "young"]
# print(df[(df["age"] != "young") & (df["age"] != "presbyopic")])

# get last column data
# df.iloc[:,-1:]

# get multiple specific row data
# df.iloc[[3,11,19]]

from cmath import log
import math
import numpy as np
import pandas as pd

def main():
    pd.set_option("display.max_columns",None)

    # default_data = pd.read_excel("weather-nominal.xlsx")
    # default_data = pd.read_excel("contact-lenses.xlsx")
    default_data = pd.read_excel("negara.xlsx")

    baseData = default_data
    df = baseData

    keyColumn = df.columns[-1]
    keys = (df[keyColumn]).unique()

    finalIndicator = []

    indicator = []

    print("INITIATING NOW")
    print("\n\n\n\n\n\n")
    print("Key : ")
    print(keys)
    print("==========\n")
    for col in df:
        uniqueCol = (df[col]).unique()
        if col != "no" and col != keyColumn and col.upper() != "TINGKAT GNP":
            indicator.append([col])
            b = len(df[col])
            indicator[len(indicator)-1].append(b)
            for i in range(0, len(uniqueCol)):
                indicator[len(indicator)-1].append([uniqueCol[i]])

                tmp = indicator[len(indicator)-1]
                for key in keys:
                    # Get total NO/YES (key) for each Column
                    a = len(df[(df[col] == uniqueCol[i]) & (df[keyColumn] == key)])                    


                    #['outlook', 14, ['sunny', 3, 2], ['overcast', 0, 4], ['rainy', 2, 3]]
                    tmp[len(tmp)-1].append(a)
                    # [outlook, sunny, no, 3]
                    # indicator[len(indicator)-1].append([uniqueCol[i], key, a])


    temp_entropy = []

    for x in indicator:
        temp_entropy.append(entropy(x))
    
    temp_marginError = []

    for x in indicator:
        temp_marginError.append(marginError(x))

    temp_gini = []

    for x in indicator:
        temp_gini.append(gini(x))



    smallest_Entropy = 1
    idxSmallest_Entropy = -1

    smallest_ME = 1
    idxSmallest_ME = -1

    smallest_gini = 1
    idxSmallest_gini = -1

    for i in range(0, len(temp_entropy)):
        if(temp_entropy[i] < smallest_Entropy):
            smallest_Entropy = temp_entropy[i]
            idxSmallest_Entropy = i

    for i in range(0, len(temp_marginError)):
        if(temp_marginError[i] < smallest_ME):
            smallest_ME = temp_marginError[i]
            idxSmallest_ME = i

    for i in range(0, len(temp_gini)):
        if(temp_gini[i] < smallest_gini):
            smallest_gini = temp_gini[i]
            idxSmallest_gini = i

    print("SMALLEST ENTROPY :")
    print(indicator[idxSmallest_Entropy])
    print(temp_entropy[idxSmallest_Entropy])
    print("\n")

    print("SMALLEST MARGIN ERROR :")
    print(indicator[idxSmallest_ME])
    print(temp_marginError[idxSmallest_ME])
    print("\n")

    print("SMALLEST GINI :")
    print(indicator[idxSmallest_gini])
    print(temp_gini[idxSmallest_gini])
    print("\n")

def gini(indicator):
     # ['outlook', 14, ['sunny', 3, 2], ['overcast', 0, 4], ['rainy', 2, 3]]

    gtot = 0
    totalData = indicator[1]

    for i in range(2, len(indicator)):
        tot = getTotal(indicator[i])

        gtemp = []

        for val in range(1, len(indicator[i])):
            # from sunny, get the rest data. 3, 2, etc...
            gini_calculated = (math.pow(indicator[i][val]/tot,2))

            gtemp.append(gini_calculated)

        gCalcTemp = 1
        for g in gtemp:
            gCalcTemp -= g

        # TRACING PURPOSE
        print("=================")
        print("Gini")
        print("Col : "+indicator[0])
        print(indicator[i])
        print(gtemp)
        print(gCalcTemp)
        print("=================")
        print("\n")
        # ########### #
        gtot += (tot/totalData) * gCalcTemp
    
    print("#")
    print("TOTAL :",abs(gtot))
    print("#\n")

    return abs(gtot)

def marginError(indicator):
    # ['outlook', 14, ['sunny', 3, 2], ['overcast', 0, 4], ['rainy', 2, 3]]

    mtot = 0
    totalData = indicator[1]

    for i in range(2, len(indicator)):
        tot = getTotal(indicator[i])

        temp_max = []

        for val in range(1, len(indicator[i])):
            temp_max.append(countMarginError(indicator[i][val],tot))

        me = max(temp_max)
        meCalculated = 1-me

        mex = (tot/totalData) * meCalculated
        mtot += mex
    
        # TRACING PURPOSE
        print("=================")
        print("MarginError")
        print("Col : "+indicator[0])
        print(indicator[i])
        print(meCalculated)
        print("=================")
        print("\n")
        # ########### #
    
    print("#")
    print("TOTAL :",abs(mtot))
    print("#\n")

    return abs(mtot)

def countMarginError(a, tot):
    if(a == 0):
        return 0

    return a/tot

def entropy(indicator):
    # ['outlook', 14, ['sunny', 3, 2], ['overcast', 0, 4], ['rainy', 2, 3]]

    etot = 0
    totalData = indicator[1]

    for i in range(2, len(indicator)):
        # ['sunny', 3, 2]

        # Get total , 3 + 2 = 5
        tot = getTotal(indicator[i])

        # For debug purpose
        debugTot = 0

        for val in range(1, len(indicator[i])):
            # from sunny, get the rest data. 3, 2, etc...
            entropy_calculated = countEntropy(indicator[i][val], tot)

            debugTot += entropy_calculated

            ex = (tot/totalData) * entropy_calculated
            etot += ex
        
        # TRACING PURPOSE
        print("=================")
        print("Entropy")
        print("Col : "+indicator[0])
        print(indicator[i])
        debugTot = abs(debugTot)
        print(debugTot)
        print("=================")
        print("\n")
        # ########### #

    print("#")
    print("TOTAL :",abs(etot))
    print("#\n")

    return abs(etot)

def countEntropy(a, tot):
    if(a == 0):
        return 0
    return (a/tot * math.log(a/tot,2))

def getTotal(indicator):
    tot = 0
    for y in range(1, len(indicator)):
        tot += indicator[y]
    return tot

if __name__ == "__main__" :
    main()