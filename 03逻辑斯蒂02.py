#!/usr/bin/python3
# -*- coding:utf-8 -*-

#读取数据，存入矩阵

import codecs

from datetime import datetime
import numpy as np
import os  
import csv  
import sys
import re
import pandas as pd
__author__ = 'WSQ'  


#生成要训练的标签
def creatLabel(labely,L):
    #for 循环遍历，!=n,设置为0
    
    n=labely.shape
    #print(n[0])
    labelY = np.ones((n[0],1))
    i=0
    for m in labely:
        #print(m,type(m),'----------------------')
        #print(np.float64(L))
        if m != np.float64(L):
            labelY[i]=0  #再改
        elif m==np.float64(L):
            labelY[i]=1
        i=i+1
    #print(labelY)
    return labelY




#逻辑斯提函数
def sigmoid(inX):
    return 1.0/(1+np.exp(-inX))


#梯度上升函数
def gradAscent(dataMatIn,classLabels):
    mn=dataMatIn.shape
    m=mn[0]
    n=mn[1]
    #print(mn,m,n)
    alpha = 0.01
    weights = np.ones((n,1))
    flag=10
    time=1
    while flag >= 0.0001:
        #print('Run Times:',time,' Start time:',datetime.now())
        h=sigmoid(np.dot(dataMatIn,weights))
        error = (classLabels-h)
        #加入正则化项
        transit = np.dot(dataMatIn.transpose(),error) + 0.1*weights
        detW = np.dot(alpha,transit)

        weights = weights + detW
        flag = np.dot(detW.T,detW)
        time = time+1
        #flag=sum(flag1[1,:])
    print('迭代次数:',time,'学习率=',alpha)
    return weights

#多分类测试函数
def  multiTest(dataMatIn,weights,Label):
    n=Label.shape
    
    testLabel = np.ones((n[0],1))
    h=sigmoid(np.dot(dataMatIn,weights))#查看此处矩阵的意义

    #计算每一个样本属于某类的概率，并选取最大的作为预测结果
    #判断h中每一个数据的大小,得到预测结果labelY
    i=0
    for line  in h:
        #print(line.argmax())
        testLabel[i]=line.argmax()
        i=i+1

    #print('预测标签',labelY.T)
    #给出正确率
    r=0
    for (i1,i2) in zip(Label,testLabel):
        if i1==i2:
            r=r+1
    print('r:',r,'n:',n[0])
    print('准确率：',r/n[0])
    return r/n[0]


    
#加载训练数据及标签
martixFile= open('G:/厦门大学/统计机器学习/03作业/softmax多分类-数据集/trainData.csv','rb')
labelFile= open('G:/厦门大学/统计机器学习/03作业/softmax多分类-数据集/label.csv','rb')

A=np.loadtxt(martixFile,delimiter=',',skiprows=0)
sLabel=np.loadtxt(labelFile,delimiter=',',skiprows=0)

#生成权值矩阵W

for i in range(0,10,1):
    forLabel = creatLabel(sLabel,i)
    w=gradAscent(A,forLabel)
    #print(w)
    if i==0:
        W=w
        continue 
    #W=np.row_stack((W, w)) 
    W=np.hstack((W,w))
    #print(W.shape)

print(W.shape)

labelFile.close()
martixFile.close()


#准确率测试
testMartixFile= open('G:/厦门大学/统计机器学习/03作业/testData.csv','rb')
testLabelFile= open('G:/厦门大学/统计机器学习/03作业/label.csv','rb')
testA=np.loadtxt(testMartixFile,delimiter=',',skiprows=0)
testLabel=np.loadtxt(testLabelFile,delimiter=',',skiprows=0)

#testLabel = creatLabel(testsLabel,0)

multiTest(testA,W,testLabel)


