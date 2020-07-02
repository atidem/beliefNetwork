# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:48:04 2020

@author: atidem
"""

"""
c = class
pm = property_magnitude
h = housing
p = purpose
ps = personal_status
j = job
e = employment
ot = own_telephone
ch = credit_history
formula = p(c).p(pm|c).p(h|pm,c).p(p|h,c).p(ps|h,c).p(j|pm,c).p(e|j,c).p(ot|j,c).p(ch|ot,c)
"""

from copy import deepcopy 

#Read csv and return dicts in array
def readCsv(name):
    file = open(name,"r")
    data = []
    keyRow = 0
    keys = []
    temp = {} 
    for a in file:
        for b,i in zip(a.split(','),range(len(a.split(',')))):
            if(keyRow==0):
                keys.append(b.strip())
            else:
                temp[keys[i]]= b.strip()
        if len(temp.keys())!=0:
            data.append(deepcopy(temp))        
        keyRow+=1
    return data,keys

#Find unique value
def uniqueValues(colName,data):
    unique = []
    for i in range(len(data)):
        if data[i][colName] not in unique:
            unique.append(data[i][colName])
    return unique

#Find all columns unique values
def mapColumns(cols,data):
    dic = {}
    for a in cols:
        tmp = uniqueValues(a,data)
        dic[a]= deepcopy(tmp)
    return dic

#Using for class seperate
def clsX(clss,data):
    table = []
    count = []
    for a in clss:
        table.append(a)
        count.append(0)
        
    for a in data:
        ind = table.index(str(a["class"]))
        count[ind] += 1
    
    totalCount = sum(count)
    for i in range(len(count)):
        count[i] = count[i] / totalCount
    
    return table,count
    
#Using for p(X|C) x=column
def cptX(X,clss,mp,data):
    table = []
    count = []
    totCount = {}
    for a in clss:
        for b in mp[X]:
            totCount[a] = 0 
            table.append([a,b])
            count.append(0) 
    for a in data:
        ind = table.index([str(a["class"]),str(a[X])])
        totCount[a["class"]] += 1
        count[ind] += 1
        
    for i in range(len(count)):
        count[i] = count[i] / totCount[table[i][0]]
    return table,count

#using for p(X|Y,C) x,y columns
def cptXY(X,Y,clss,mp,data):
    table = []
    count = []
    totCount = {}
    for a in clss:
        for b in mp[Y]:
            totCount[a,b] = 0
            for c in mp[X]:
                table.append([a,b,c])
                count.append(0) 
    for a in data:
        ind = table.index([str(a["class"]),str(a[Y]),str(a[X])])
        totCount[a["class"],a[Y]] += 1
        count[ind] += 1
        
    for i in range(len(count)):
        count[i] = count[i] / totCount[table[i][0],table[i][1]]    
    return table,count

#Predict
def predict(data): 
    predict = []
    for a in range(len(data)):
        bad = (pclsV[pcls.index("bad")]*
        ppmV[ppm.index(["bad",data[a]["property_magnitude"]])]*
        phpmV[phpm.index(["bad",data[a]["property_magnitude"],data[a]["housing"]])]*
        pphV[pph.index(["bad",data[a]["housing"],data[a]["purpose"]])]*
        ppshV[ppsh.index(["bad",data[a]["housing"],data[a]["personal_status"]])]*
        pjpmV[pjpm.index(["bad",data[a]["property_magnitude"],data[a]["job"]])]*
        pejV[pej.index(["bad",data[a]["job"],data[a]["employment"]])]*
        potjV[potj.index(["bad",data[a]["job"],data[a]["own_telephone"]])]*
        pchotV[pchot.index(["bad",data[a]["own_telephone"],data[a]["credit_history"]])])
        
        good = (pclsV[pcls.index("good")]*
        ppmV[ppm.index(["good",data[a]["property_magnitude"]])]*
        phpmV[phpm.index(["good",data[a]["property_magnitude"],data[a]["housing"]])]*
        pphV[pph.index(["good",data[a]["housing"],data[a]["purpose"]])]*
        ppshV[ppsh.index(["good",data[a]["housing"],data[a]["personal_status"]])]*
        pjpmV[pjpm.index(["good",data[a]["property_magnitude"],data[a]["job"]])]*
        pejV[pej.index(["good",data[a]["job"],data[a]["employment"]])]*
        potjV[potj.index(["good",data[a]["job"],data[a]["own_telephone"]])]*
        pchotV[pchot.index(["good",data[a]["own_telephone"],data[a]["credit_history"]])])
        
        if(good>bad):
            predict.append("good")
        else:
            predict.append("bad")
        
    return predict

#Accuracy calc
def accuracy(pred,data):
    sumTrue = 0
    for i in range(len(data)):
        if(data[i]["class"]==pred[i]):
            sumTrue += 1
    return sumTrue/len(data)

#Tp count, tn count , tp rate, tn rate 
def rates(pos,pred,data):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    for i in range(len(pred)):
        if pred[i]==pos and data[i]["class"]==pos:
            tp += 1
        if pred[i]==pos and data[i]["class"]!=pos:
            fp += 1
        if pred[i]!=pos and data[i]["class"]!=pos:
            tn += 1
        if pred[i]!=pos and data[i]["class"]==pos:
            fn += 1
    dct = {"tp count":tp,"tn count":tn,"tp rate":tp/(tp+fn),"tn rate":tn/(tn+fp),"accuracy":accuracy(pred,data)}
    return dct
    
def yazdirCpt(header,lst,lstV,):
    file = open("Result.txt","a+")
    file.write("              -"+str(header)+"-\n\n")
    for i in range(len(lst)):
        file.write('%-65s |%-8s \n' % (str(lst[i]), str(lstV[i])))
        file.write("-------------------------------------------------------------------------------------------\n")
    file.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    file.close()

def yazdirMeasure(meas):
    file = open("Result.txt","a+")
    file.write("\n              -TEST MEASUE-\n")
    file.write(str(meas))
    file.close()
    
#Prepare data
trainData,columns=readCsv("Proje1-Train.txt")
testData,_=readCsv("Proje1-Test.txt")
maps = mapColumns(columns,trainData)

#Cpt Tables
pcls,pclsV = clsX(maps["class"],trainData)
ppm,ppmV = cptX("property_magnitude",maps["class"],maps,trainData)
phpm,phpmV = cptXY("housing","property_magnitude",maps["class"],maps,trainData)
pph,pphV = cptXY("purpose","housing",maps["class"],maps,trainData)
ppsh,ppshV = cptXY("personal_status","housing",maps["class"],maps,trainData)
pjpm,pjpmV = cptXY("job","property_magnitude",maps["class"],maps,trainData)
pej,pejV = cptXY("employment","job",maps["class"],maps,trainData)
potj,potjV = cptXY("own_telephone","job",maps["class"],maps,trainData)
pchot,pchotV = cptXY("credit_history","own_telephone",maps["class"],maps,trainData)

#Pred and accuracy
pred = predict(trainData)
print(" Train Accuracy: "+str(accuracy(pred,trainData)))
trainMeasures = rates("bad",pred,trainData)
pred = predict(testData)
print(" Test Accuracy: "+str(accuracy(pred,testData)))
testMeasures = rates("bad",pred,testData)

##Append metodu kullanıldığı icin yorum satırına alındı aktif edilebilir.
#yazdirCpt("class",pcls,pclsV,)
#yazdirCpt("property_magnitude",ppm,ppmV,)
#yazdirCpt("housing",phpm,phpmV,)
#yazdirCpt("purpose",pph,pphV,)
#yazdirCpt("personal_status",ppsh,ppshV,)
#yazdirCpt("job",pjpm,pjpmV)
#yazdirCpt("employment",pej,pejV,)
#yazdirCpt("own_telephone",potj,potjV)
#yazdirCpt("credit_history",pchot,pchotV)
#yazdirMeasure(testMeasures)

