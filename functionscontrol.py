# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 17:13:13 2018

@author: DMC
"""

import csv
import os
import matplotlib.pyplot as plt 

def Inifile(Tf):
    if os.path.isfile('ctrl.csv'):
        os.remove('ctrl.csv') 
        
    with open('ctrl.csv', 'w', newline='') as csvfile:
        fieldnames = ['DIO0','DIO1','DIO2','DIO3','DIO4','DIO5','DIO6','DIO7','DIO8','DIO9','DIO10','DIO11','DIO12','DIO13','DIO14','DIO15','DIO16','DIO17','DIO18','DIO19','DIO20','DIO21','DIO22','Tiempo reloj']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
        #writer.writeheader()
        for i in range(0,Tf+10,10):
            writer.writerow({'DIO0': 0,'DIO1':  0,'DIO2': 0,'DIO3':0,'DIO4':0,'DIO5':0,'DIO6':0,'DIO7':0,'DIO8':0,'DIO9':0,'DIO10':0,'DIO11':0,'DIO12':0,'DIO13':0,'DIO14':0,'DIO15':0,'DIO16':0,'DIO17':0,'DIO18':0,'DIO19':0,'DIO20':0,'DIO21':0,'DIO22':0,'Tiempo reloj': i})
    
        csvfile.close()
        

def Pulsefile(OUT,chan):   
   # open file
   with open('ctrl.csv', 'r') as f:
        reader = csv.reader(f)              
        # read file row by row
        data = list(reader)
        for i in OUT:
           dio = int(i)
           Tpul = chan[i]
           print('Los pulsos en el canal',i,'son:',Tpul)
     
           
           for i in range(len(Tpul)):
               T = int(Tpul[i][0]/10)
               t = int(Tpul[i][1]/10)
               for n in range(T,t):
                   data[n][dio] = 1
                    
   f.close()
   if os.path.isfile('output.csv'):
       os.remove('output.csv')         
   with open('output.csv', 'w',newline='') as g:
       writer = csv.writer(g)
       writer.writerows(data)
       g.close()

    
def graffile(salida,Tf):     
    tiempos = []
    DIO0 = []
    DIO1 = []
    DIO2 = []
    # open file
    with open('output.csv', 'r') as f:
            rrr = csv.reader(f)              
            for row in rrr:
                tiempos.append(int(row[23]))
                DIO0.append(int(row[0]))
                DIO1.append(int(row[1]))
                DIO2.append(int(row[2]))
    
                # Print data 
            #print(tiempos)
            #print(DIO0)
            #print(DIO1)
            #print(DIO2)
            
            ax1 = plt.subplot(311)
            plt.plot(tiempos, DIO0)
            plt.xlabel('time (micros)')
            plt.ylabel('DIO0')
            plt.setp(ax1.get_xticklabels(), fontsize=6)
            
            # share x only
            ax2 = plt.subplot(312, sharex=ax1)
            plt.plot(tiempos, DIO1)
            plt.ylabel('DIO1')
            # make these tick labels invisible
            #plt.setp(ax2.get_xticklabels(), visible=False)
            
            # share x and y
            ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
            plt.plot(tiempos, DIO2)
            plt.ylabel('DIO2')
            plt.show()
            
            #plt.plot(tiempos, DIO0)
            #plt.xlim(0, Tf)
            #plt.ylim(0,1.5)
            #plt.show()
            f.close()
            
def binfile():
    with open('output.csv', 'r') as f:
        reader = csv.reader(f)              
        # read file row by row
        data = list(reader)
        f.close()
        
        newdata =[]
        for i in range(len(data)):
            FIO = 0
            EIO = 0
            CIO = 0 
            MIO = 0
            
            for j in range(0,8):
                FIO+= int(data[i][j])* 2**(j)
                for k in range(8,16):    
                    EIO+= int(data[i][k])*2**(j)
           
            CIO = int(data[i][16]) + int(data[i][17]) * 2 + int(data[i][18])*4 + int(data[i][19])*8
            
            MIO = int(data[i][20]) + int(data[i][21]) * 2 + int(data[i][22])*4 
            
            #newdata.append([bin(FIO),bin(EIO),bin(CIO),bin(MIO)])    
            newdata.append([(FIO),(EIO),(CIO),(MIO)])    
        if os.path.isfile('binoutput.csv'):
            os.remove('binoutput.csv')         
        with open('binoutput.csv', 'w',newline='') as g:
            writer = csv.writer(g)
            writer.writerows(newdata)
            g.close()

            
            
            
            
            
            
            
            




















































