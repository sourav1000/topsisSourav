# -*- coding: utf-8 -*-
"""101903216_topsis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U8MKYcH3BH0OSKPwiLO10wybEfr6nUef
"""

import sys
import os
import copy
import math
import pandas as pd
import numpy as np
from os import path

def topsis(source,l,im,dest):

  df=pd.read_csv(source)
  df1=df.loc[:,['P1','P2','P3','P4','P5']]

  class myexception(Exception):
    pass
  if not (path.exists(source)):
    raise myexception("No such file exists")

  if not source.endswith('.csv'):
    raise myexception("Enter CSV format file only")

  weight=[]
  wt=l.split(',')
  for i in wt:
    k=0
    for j in i:
      if not j.isnumeric():
        if k>=1 or j!='.':
          raise myexception("Format of Weight is not correct")
        else:
          k=k+1
    weight.append(float(i))
  weight=np.array(weight)

      
  impact=im.split(',')
  for i in impact:
    if i not in {'+','-'}:
      raise myexception("Format of impact is not correct")
      
  r,c=df1.shape
  if not c>=3:
    raise myexception("Input file must contain 3 or more columns")

  if len(weight)!=(c):
    raise myexception("Number of weight and number of columns must be equal")

  if len(impact)!=c:
    raise myexception("Number of impact and Number of columns must be equal")


  for i in df1.columns:
    for j in df1.index:
      val=isinstance(df1[i][j],int)
      val1=isinstance(df1[i][j],float)
      if not val and not val1:
        raise myexception("Values are not numeric")
    
  s=[]
  for j in range(0,c):
    sum=0
    for i in range(0,r):
      sum=sum+df1.iloc[i,j]**2
    s.append(sum**0.5)
  s=np.array(s)
  number=np.array(df1)
  for i in range(0,c):
    number[:,i]=number[:,i]/s[i]

  for i in range(0,c):
    number[:,i]=number[:,i]*weight[i]
  number

  max=[]
  min=[]
  for i in range(0,c):
    max.append(np.max(number[:,i]))
    min.append(np.min(number[:,i]))

  best=[]
  worst=[]
  for i in range(0,r):

    sum1=0
    sum2=0
    for j in range (0,c):
      if(impact[j]=='+'):
        sum1=sum1+((max[j]-number[i][j])**2)
        sum2=sum2+((min[j]-number[i][j])**2)
      else:
          sum2=sum2+((max[j]-number[i][j])**2)
          sum1=sum1+((min[j]-number[i][j])**2)
    best.append(sum1**0.5)
    worst.append(sum2**0.5)

  s1=np.array(best)
  s2=np.array(worst)
  s1

  s3=s1+s2
  s3=np.array(s3)
  perform=s2/s3
  perform
  df['score']=perform
  df
  scoring=perform.tolist()

  df["Rank"] = (df["score"].rank(method="max", ascending=False))
  df = df.astype({"Rank": "int"})
  df.to_csv(dest,index=False)
 

