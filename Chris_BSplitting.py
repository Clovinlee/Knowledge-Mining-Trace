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
    default_data = pd.read_excel("gnp_numerical.xlsx")
    # default_data = pd.read_excel("contact-lenses.xlsx")

    baseData = default_data
    df = baseData

    keyColumn = df.columns[-1]
    keys = (df[keyColumn]).unique()

    colNumber = df.columns[0]

    indicator = []

    print("INITIATING NOW")
    print("\n\n\n\n\n\n")
    print("Key : ")
    print(keys)
    print("==========\n")

    df = df.sort_values(by=[colNumber])
    
    # Contains changed VALUE OF YA - TIDAK
    indicator = []

    # df["changed"] = df[keyColumn].ne(df[keyColumn].shift().bfill()).astype(int)
    # df = df[df["changed"] == 1]
    df = df.reset_index(drop=True)


    indicator = []

    iter_now = -1
    for idx, row in df.iterrows():
        if(idx > 0):

            # Compare this row and previous row
            a = df.loc[idx-1]
            b = df.loc[idx]

            if(a[keyColumn] != b[keyColumn] and a is not None and b is not None):
                indicator.append([a,b])

    split_average = []
    for x in indicator:
        avg = 0
        for y in x:
            avg += y[colNumber]
        avg = avg / len(x)
        split_average.append(avg)

    df = baseData

    # split avg
    # [350.0, 565.0, 665.0]

    indicator = []
    for avg in split_average:
        indicator.append([avg])
        indicator[len(indicator)-1].append([])
        for key in keys:
            a = len(df[(df[colNumber] <= avg) & (df[keyColumn] == key)])
            indicator[len(indicator)-1][len(indicator[len(indicator)-1])-1].append(a)
    
        indicator[len(indicator)-1].append([])
        for key in keys:
            a = len(df[(df[colNumber] > avg) & (df[keyColumn] == key)])
            indicator[len(indicator)-1][len(indicator[len(indicator)-1])-1].append(a)
            
        

    # [[350.0, [0, 4], [6, 1]], [565.0, [5, 4], [1, 1]], [665.0, [5, 5], [1, 0]]]
    # Position <= then last >
    # 4,6 are from <= , 6 1 are from >
    

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

    print(keys)

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

def marginError(indicator):
    mtot = 0
    totalData = 0

    for i in range(1,len(indicator)):
        for y in indicator[i]:
            totalData += y


    for i in range(1, len(indicator)):
        tot = getTotal(indicator[i])
        temp_max = []
        for val in range(0, len(indicator[i])):
            temp_max.append(countMarginError(indicator[i][val],tot))
        
        me = max(temp_max)
        meCalculated = 1-me

        mex = (tot/totalData) * meCalculated
        mtot += mex

        # TRACING PURPOSE
        print("=================")
        print("MarginError")
        print("Col : ",indicator[0])
        print("Total :",tot)
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

def gini(indicator):
    totalData = 0
    gtot = 0

    print(indicator)
    
    for i in range(1,len(indicator)):
        for y in indicator[i]:
            totalData += y

    for i in range(1, len(indicator)):
        tot = getTotal(indicator[i])

        debugTot = 0

        gtemp = []

        for val in range(0, len(indicator[i])):
            # from sunny, get the rest data. 3, 2, etc...
            gini_calculated = (math.pow(indicator[i][val]/tot,2))

            gtemp.append(gini_calculated)

        gCalcTemp = 1
        for g in gtemp:
            gCalcTemp -= g

        # TRACING PURPOSE
        print("=================")
        print("Gini")
        print("Col :",indicator[0])
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

def countGini(a, tot):
    pass

def entropy(indicator):
    totalData = 0
    etot = 0

    print(indicator)
    
    for i in range(1,len(indicator)):
        for y in indicator[i]:
            totalData += y

    for i in range(1, len(indicator)):
        tot = getTotal(indicator[i])

        debugTot = 0

        for y in indicator[i]:
            entropy_calculated = countEntropy(y,tot)

            ex = (tot/totalData) * entropy_calculated
            debugTot += entropy_calculated

            etot += ex

        # TRACING PURPOSE
        print("=================")
        print("Entropy")
        print("Col :",indicator[0])
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
    for y in range(0, len(indicator)):
        tot += indicator[y]
    return tot


if __name__ == "__main__" :
    main()