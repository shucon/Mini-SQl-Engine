#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlparse
import csv
import os
import sys
import re


# In[2]:


def select(query):
    for i in query:
        if (i.lower() == "from"):
            continue


# In[3]:


# Getting Metadata
database = {}
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


# In[4]:


query = sys.argv[1]
# print(query)
query = "Select * from table1 where a=b"
queries=sqlparse.split(query)


# In[5]:


for query in queries:
    query = sqlparse.format(query,strip_comments=True)
    sql = sqlparse.parse(query)[0]
    token = sql.tokens
    querytype = sqlparse.sql.Statement(token).get_type()
    print (querytype)
    identifierList = []
    queryArray = sqlparse.sql.IdentifierList(token).get_identifiers()
    print queryArray
    #     whereClause = sqlparse.sql.Where(token)
#     print(re.split(r'[\ \t,]+',queryArray))
# #     comparision = sqlparse.sql.Comparision(token)
# #     print comparision
#     if querytype == "SELECT":
#         continue
# #         select(queryArray)
#     else:
#         print("Error: Unknown Function")


# In[6]:


def queryProcessor(query):
	if query[-1]!=';':
		print("Syntax Err: Expected ';' in the end")    
	else:
		query_convert = sqlparse.parse(query)[0].tokens
		commands = []
		lst = sqlparse.sql.IdentifierList(query_convert).get_identifiers()
		for command in lst:
			commands.append(str(command))
		if commands[0].lower() == 'select':
			print(commands)
			select_process(commands)
		else:
			print("This query is not supported by slq-engine.")


# In[ ]:




