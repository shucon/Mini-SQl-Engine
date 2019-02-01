#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlparse
import csv
import os
import sys
import re
import copy
function = []
whereCondition = 0
conditionArray = []
ORFlag = 0


# In[2]:


def comparisionFunc(compare11,compare12,compare21,compare22):

    condition1 = False
    if conditionArray[0][2] == '>=':
        if compare11 >= compare12:
            condition1 = True
    if conditionArray[0][2] == '<=':
        if compare11 <= compare12:
            condition1 = True
    if conditionArray[0][2] == '=':
        if compare11 == compare12:
            condition1 = True
    if conditionArray[0][2] == '>':
        if compare11 > compare12:
            condition1 = True
    if conditionArray[0][2] == '<':
        if compare11 < compare12:
            condition1 = True
    
    if len(conditionArray) == 2:
        condition2 = False
        if conditionArray[1][2] == '>=':
            if compare21 >= compare22:
                condition2 = True
        if conditionArray[1][2] == '<=':
            if compare21 <= compare22:
                condition2 = True
        if conditionArray[1][2] == '=':
            if compare21 == compare22:
                condition2 = True
        if conditionArray[1][2] == '>':
            if compare21 > compare22:
                condition2 = True
        if conditionArray[1][2] == '<':
            if compare21 < compare22:
                condition2 = True
        if ORFlag:
            if (condition1 or condition2):
                return True
            else:
                return False
        else:
            if (condition1 and condition2):
                return True
            else:
                return False
    else:
        return condition1


# In[3]:


def replaceStar (tables):
    
    columns = {}
    for i in tables:
        columns[i] = database[i]
    return columns

def whereSplit(query):
    operators = ['>=','<=','=','>','<']
    query =  query[whereCondition].upper().strip(';')
    query = query.strip('WHERE')
    query = query.strip()
    query = query.split('AND')
    if len(query) == 1:
        query = ''.join(query)
        query = query.split('OR')
    for i in range(len(query)):
        for j in operators:
#             print j
            query[i] = query[i].split(j)
            if len(query[i]) > 1:
                query[i].append(j)
                for k in range(len(query[i])):
                    query[i][k] = query[i][k].strip()
                break
            else :
                query[i] = ''.join(query[i])
    return query


# In[4]:


def checkAmbiguity (tables,columns):
    
#     Initialize dictionary
    temp = {}
    for table in tables:
        temp[table] = []
    
    if '.' in columns[0]:
        for i in columns:
            i = i.split('.')
            if i[0] not in tables:
                raise ValueError ("Unknown Table")
            temp[i[0]].append(i[1])
    else:
        for column in columns:
            flag = 0
            for table in tables:
                if column in database[table]:
                    if flag:
                        raise ValueError ("Ambiguity Found")
                    else :
                        flag = 1
                        temp[table].append(column)
    return temp


# In[5]:


def whereAmbiguity (tables):
    
#     Initialize dictionary
    temp = copy.deepcopy(conditionArray)
    
    for i in range(len(conditionArray)):
        if '.' in conditionArray[i][0]:
#             print conditionArray[i]
            for j in range(len(conditionArray[i])):
                if '.' in conditionArray[i][j]:
                    temp1 = conditionArray[i][j].split('.')
#                     if temp1[0] not in tables:
#                         raise ValueError ("Unknown Table")
                    temp[i][j] = temp1[0].lower()
                    conditionArray[i][j] = temp1[1]
        else:
#             print conditionArray[i]
            flag1 = 0
            flag2 = 0
            for table in tables:
                if conditionArray[i][0] in database[table]:
                    if flag1:
                        raise ValueError ("Ambiguity Found")
                    else :
                        flag1 = 1
                        temp[i][0] = table
                            
                if conditionArray[i][1] in database[table]:
#                         print conditionArray[j][1]
                    if flag2:
                        raise ValueError ("Ambiguity Found")
                    else :
                        flag2 = 1
                        temp[i][1] = table
    return temp


# In[6]:


def joinTables (table1,table2):
    
    joinedTable = []
    for i in table1:
        for j in table2:
            joinedTable.append(i+j)
    return joinedTable


# In[7]:


def checkFunction (function,column):
    if function == "MAX":
        printMax(column)
    elif function == "MIN":
        printMin(column)
    elif function == "AVERAGE":
        printAverage(column)
    elif function == "SUM":
        printSum(column)
    elif function:
        raise ValueError("Unknown function")
    return


# In[8]:


def printFunction (columns,tables,combinedTable,function):
    
    column = []
    for row in combinedTable:
        i = 0
        for table in tables:
            for j in database[table]:
                if j in columns[table]:
                    temp = j
                    column.append(row[i])
                    i += 1
                else:
                    i += 1
    print (function+'('+temp+')')
    checkFunction(function, column)


# In[9]:


def printMax(column):
    
    print max(column)
    return

def printMin(column):
    
    print min(column)
    return

def printAverage(column):
    
    sum_p = 0
    for i in column:
        sum_p += int(i)
    print sum_p/len(column)
    return

def printSum(column):
    
    sum_p = 0
    for i in column:
        sum_p += int(i)
    print sum_p
    return


# In[10]:


def printDistinct (columns,tables,combinedTable):
    
    tableFinal = []
# Print Header
    for table in tables:
        for j in database[table]:
            if j in columns[table]:
                print('DISTINCT ('+j+')'),
    print
                
    for row in combinedTable:
        i = 0
        tempRow = []
        for table in tables:
            for j in database[table]:
                if j in columns[table]:
                    temp = j
                    tempRow.append(row[i])
                    i += 1
                else:
                    i += 1
        if not tableFinal:
            tableFinal.append(tempRow)
#         print tableFinal
        for i in tableFinal:
            flag = 0
            for j in range(len(i)):
                if i[j] != tempRow[j]:
                    flag = 1
        if flag == 1:
            tableFinal.append(tempRow)
    
#     print tableFinal
    for i in tableFinal:
        for j in i:
            print (j),
        print


# In[11]:


def getTables(query):
#     gives the tables that are required
    for i in range(len(query)):
        if (query[i].upper() == "FROM"):
            tableIndex = i+1
    table = re.split(r'[\ \t,]+',query[tableIndex])
    global whereCondition
    if query[tableIndex+1] != ";":
        whereCondition = tableIndex + 1
        if query[tableIndex+1].upper().find('OR') != -1:
            global ORFlag
            ORFlag = 1
#             print 'OR'
    return table

def getColumns(query):
#     gives the rows that are to be printed
    column = []
    global function 
    for i in range(len(query)):
        if (query[i].upper() == "FROM"):
            rowIndex = i-1
    for i in range(len(query[rowIndex])):
        if (query[rowIndex][i] == "("):
            column = re.split(r'[\ \t,]+',query[rowIndex][query[rowIndex].find("(")+1:query[rowIndex].find(")")])
            break;
        function.append(query[rowIndex][i])
    
    if not column:
        column = re.split(r'[\ \t,]+',query[rowIndex])
        function = []
    
#     Converting function list to Array
    string = ''.join(function)
    function = string.upper()
    return column


# In[12]:


def select(query):
    columns = getColumns(query)
# Get data from all the required tables
    tables = getTables(query)
#     print tables
#     Convert columns to dictionary
    if columns[0] == "*":
        columns = replaceStar(tables)
    else:
        columns = checkAmbiguity(tables,columns)
    
    for table in tables:
        data[table] = []
        with open('files/'+table+'.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                row = [j.replace("'",'') for j in row]
                row = [int(j) for j in row]
                data[table].append(row)
                

    if len(tables) > 1:
        combinedTable = joinTables(data[tables[0]],data[tables[1]])
        tables.remove(tables[0])
        tables.remove(tables[0])
        for i in tables:
            combinedTable = joinTables(combinedTable,data[i])
    else:
        combinedTable = data[tables[0]]
    tables = getTables(query)

    #     Check where condition
    if whereCondition:
        global conditionArray
        conditionArray = whereSplit(query)
        tableArray = whereAmbiguity(tables)
#         print conditionArray
#         print tableArray
#         print tables
        tempArray = copy.deepcopy(combinedTable)
        tempIndex = 0
        removeColumn1 = []
        removeColumn2 = []
        for i in range(len(combinedTable)):
            count = 0
            compare11=0
            compare12=0
            compare21=0
            compare22=0
            
            for table in tables:
                for j in database[table]:
                    if j in conditionArray[0][0] and table in tableArray[0][0]:
#                         print j
                        compare11 = combinedTable[i][count]
                    if tableArray[0][1] != conditionArray[0][1]:
                        if tableArray[0][2] == '=':
                            removeColumn1.append(conditionArray[0][1])
                            removeColumn1.append(tableArray[0][1])
#                         Condition for checking a number or column
                        if j in conditionArray[0][1] and table in tableArray[0][1]:
                            compare12 = combinedTable[i][count]
                    else:
                        compare12 = tableArray[0][1]
                    if len(conditionArray) == 2:
                        if j in conditionArray[1][0] and table in tableArray[1][0]:
                            compare21 = combinedTable[i][count]
                        if tableArray[1][1] != conditionArray[1][1]:
                            if tableArray[1][2] == '=':
                                removeColumn2.append(conditionArray[1][1])
                                removeColumn2.append(tableArray[1][1])
    #                         Condition for checking a number or column
                            if j in conditionArray[1][1] and table in tableArray[1][1]:
                                compare22 = combinedTable[1][count]
                        else:
                            compare22 = tableArray[1][1]
                    count += 1
#             print compare11,compare12,compare21,compare22
            booleanVar=comparisionFunc(compare11,compare12,compare21,compare22)
#             print booleanVar
            if not booleanVar:
                del tempArray[tempIndex]
            else:
                tempIndex += 1
        combinedTable= tempArray
                    
    if function :
        printFunction (columns,tables,combinedTable,function)
        return
    
    if (query[1].upper() == 'DISTINCT'):
        printDistinct(columns,tables,combinedTable)
        return
    
#     print removeColumn1
    if len(removeColumn1):
        columns[removeColumn1[1]].remove(removeColumn1[0])
#     print columns
        
    if len(removeColumn2):
        columns[removeColumn2[1]].remove(removeColumn2[0])
#     print columns
        
#         Prints Header
    for i in tables:
        for columnName in columns[i]:
            print (i+"."+columnName),
    print
    
#     print columns
#     Print Rows
    for row in combinedTable:
        i = 0
        for table in tables:
            for j in database[table]:
                if j in columns[table]:
                    print(row[i]),
                    i += 1
                else:
                    i += 1
        print
            


# In[13]:


# Getting Metadata
database = {}
data = {}
f = open('files/metadata.txt','r')
for line in f:
#     print(line.strip())
    if line.strip() == "<begin_table>":
        begin = 1
        continue
    if line.strip() == "<end_table>":
        begin = 0
        continue
    if begin == 1:
        table_name = line.strip()
        database[table_name] = []
        begin = 2
        continue
    if begin == 2:
        database[table_name].append(line.strip())
        continue
# print(database)


# In[14]:


query = sys.argv[1]
# print(query)
query = "Select table1.B,table2.B from table1,table2 where table1.B=table2.B;"
queries=sqlparse.split(query)


# In[15]:


for query in queries:
    query = sqlparse.format(query,strip_comments=True)
    sql = sqlparse.parse(query)[0]
    token = sql.tokens
    querytype = sqlparse.sql.Statement(token).get_type()
    identifierList = []
    queryArray = sqlparse.sql.IdentifierList(token).get_identifiers()
# command is an array that divides sql query into multiple parts
    command = []
    for i in queryArray:
        command.append(str(i))
# Error Handling of ; ending
    commandLength = len(command)
    lastcommandLength = len(command[commandLength-1])
#     print command
    if command[commandLength-1][lastcommandLength-1] != ";":
        raise ValueError("Error: The command does not end with ;")
        continue
#         Run specific query command
    if querytype == "SELECT":
        select(command)
#         continue
    else:
        raise ValueError("Error: Unknown Function")


# In[ ]:




