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

import numpy as np
import pandas as pd

def main():

    pd.set_option("display.max_columns",None)

    # default_data = pd.read_excel("weather-nominal.xlsx")
    # default_data = pd.read_excel("contact-lenses.xlsx")
    default_data = pd.read_excel("negara.xlsx")
    # default_data = pd.read_excel("student.xlsx")

    baseData = default_data
    df = baseData

    keyColumn = df.columns[-1]
    keys = (df[keyColumn]).unique()
    # keys = ["hard","soft","none"]
    # keys = ["none","soft","hard"]
    # keys = ["soft","hard","none"]

    finalRules = []
    print("INITIATING NOW")
    print("VVVVV")
    print("\n\n\n\n\n\n\n\n\n\n")

    for key in keys:
        baseData = default_data
        df = baseData

        while not checkKeyComplete(df, key, keyColumn):
            rules = []
            while not checkRuleComplete(df, rules, key, keyColumn):
                indicator = []
                for col in df:
                    if col.upper() != "NO" and col != keyColumn and col not in getUsedCol(rules):
                        uniqueCol = (df[col]).unique()
                        txtPrint = "-------------------------------------\n"
                        txtPrint += "| {col:}\n".format(col = col)
                        txtPrint += "-------------------------------------\n"
                        for i in range(0, len(uniqueCol)) : 
                            # penyebut
                            a = len(df[(df[col] == uniqueCol[i]) & (df[keyColumn] == key)])
                            # pembilang
                            b = len(df[df[col] == uniqueCol[i]])

                            txtPrint += "| {colName:} = {uq:} 	          |{a:}/{b:}|\n".format(colName = col, uq = uniqueCol[i], a = a ,b = b)
                            indicator.append([col, uniqueCol[i], a, b])
                        txtPrint += "-------------------------------------"
                        
                        # ###################
                        # FOR TRACING
                        print(txtPrint)
                        # ###################

                # highest
                #  Col    ColVal   a / b
                # ['age', 'young', 2, 8]
                # print(indicator)
                highest = ""
                if(len(indicator) > 0):
                    highest = indicator[0]

                # print(indicator)
                for i in range(1,len(indicator)) :
                    per = indicator[i][2] / indicator[i][3]
                    # if(per == 1):
                        # highest = indicator[i]
                        # if(absoluteCol == ""):
                        #     absoluteCol = indicator[i][0]
                    
                    perHighest = highest[2] / highest[3]
                    if(per > perHighest):
                        highest = indicator[i]
                    elif( per == perHighest):
                        if(indicator[i][2] > highest[2]):
                            highest = indicator[i]
                if(indicator != ""):
                    df = df[df[highest[0]] == highest[1]]
                # print("\n=====")
                # print(highest)
                # print(df)
                # print("=====")
                rules.append(highest)
                # print("New Cycle")
                print("\n")
                print("Key : "+key)
                print("Highest : ")
                print(highest)
                print("########################\n")
            # print("KEY : "+key)
            # print(rules)
            # print("Absolute : "+absoluteCol)

            finalRules.append([key, rules])
            df = trimRule(baseData, df, rules)
            baseData = df
            print("Individual Rule : ")
            print(rules)
            print(df)
            # print("\n\n\n\n\n\n\n\n\n\n")

    # Final Rules
    # ['hard', [['astigmatism', 'yes', 4, 12], ['tear', 'normal', 4, 6], ['spectacle', 'myope', 3, 3]]]
    print('\n')
    for r in finalRules:
        print(r)

def trimRule(baseData, df, rules):
    df1 = baseData
    df2 = df
    return mergeTrim(df1,df2)


def mergeTrim(df1, df2):
    dfFinal = pd.merge(df1, df2, indicator=True, how="outer").query("_merge=='left_only'").drop("_merge",axis=1)
    return dfFinal

def getUsedCol(rules):
    lst = []
    for rule in rules : 
        lst.append(rule[0])
    return lst

def checkRuleComplete(df, rules, key, keyColumn):
    # If complete, then out of loop.!!!
    df1 = df
    df2 = df

    df2 = df2[df2[keyColumn] == key]

    if(len(df) == 0):
        return True 



    if(len(df1) == len(df2)):
        return True

def checkKeyComplete(df, key, keyColumn):
    df = df[df[keyColumn] == key]
    if(len(df) == 0) :
        return True
    else:
        return False

if __name__ == "__main__" :
    main()