#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlparse
import csv
import os
import sys
import re
function = []


# In[2]:


def replaceStar (tables):
    
    columns = {}
    for i in tables:
        columns[i] = database[i]
    return columns


# In[3]:


def checkAmbiguity (tables,columns):
    
#     Initialize dictionary
    temp = {}
    for table in tables:
        temp[table] = []
    
    if '.' in columns[0]:
        for i in columns:
            i = i.split('.')
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


# In[4]:


def joinTables (table1,table2):
    
    joinedTable = []
    for i in table1:
        for j in table2:
            joinedTable.append(i+j)
    return joinedTable


# In[5]:


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


# In[6]:


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


# In[7]:


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


# In[8]:


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


# In[9]:


def getTables(query):
#     gives the tables that are required
    for i in range(len(query)):
        if (query[i].upper() == "FROM"):
            tableIndex = i+1
    table = re.split(r'[\ \t,]+',query[tableIndex])
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


# In[10]:


def select(query):
    columns = getColumns(query)
# Get data from all the required tables
    tables = getTables(query)
    
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
                data[table].append(row)
#     print data
    if len(tables) > 1:
        combinedTable = joinTables(data[tables[0]],data[tables[1]])
        tables.remove(tables[0])
        tables.remove(tables[0])
        for i in tables:
            combinedTable = joinTables(combinedTable,data[i])
    else:
        combinedTable = data[tables[0]]
    
    tables = getTables(query)
    
    if function :
        printFunction (columns,tables,combinedTable,function)
        return
    
    if (query[1].upper() == 'DISTINCT'):
        printDistinct(columns,tables,combinedTable)
        return
    
#         Prints Header
    for i in tables:
        for columnName in columns[i]:
            print (i+"."+columnName),
    print
    
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
            


# In[11]:


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


# In[12]:


query = sys.argv[1]
# print(query)
query = "Select DISTInct A,C,D from table1,table2 where a=b;"
queries=sqlparse.split(query)


# In[13]:


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
    print command
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




