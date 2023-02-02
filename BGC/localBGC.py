import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
import subprocess
from itertools import combinations

cipher = ["elephant","ASCON"]
cipherSbox = [
    [14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6],  # elephant
    [4, 11, 31, 20, 26, 21, 9, 2, 27, 5, 8, 18, 29, 3, 6, 28, 30, 19, 7, 14, 0, 13, 17, 24, 16, 12, 1, 25, 22, 10, 15, 23],  # ASCON
]
bgc=[17,25]
BN = [4, 5]
A = [[0 for i in range(256)] for j in range(8)]
result=0

def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num //= 2
    return res

def State_Variate(fout, bitnum, Size, GateNum, QNum, bNum,yN,TTstr):
    #State Variate
    #x
    for i in range(bitnum):
        fout.write('X_' + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    #y
    for i in range(yN):
        fout.write("Y_" + str(i))
        if (i == yN - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    #t
    for t in range(GateNum+len(TTstr)):
        fout.write("T_"+ str(t))
        if (t == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    #q
    for i in range(QNum):
        fout.write("Q_"+ str(i))
        if (i == QNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    #B
    for i in range(bNum):
        fout.write("B_" + str(i))
        if (i == bNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")

def Decompose(flag,Sbox):
    #get value of X or Y
    for i in range(Size):
        tem = ""
        if flag == 0:
            tem = i
        else:
            tem = Sbox[i]
        for j in range(bitnum - 1, -1, -1):
            A[j][i] = tem % 2
            tem //= 2


def Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,Sbox,yN,Yelem,constr):
    # Trival Constraints
    # X
    Decompose(0,Sbox)
    for i in range(bitnum):
        fout.write("ASSERT( X_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[i][j]))
        fout.write(" );\n")
    # Y
    Decompose(1,Sbox)
    for i in range(yN):
        fout.write("ASSERT( Y_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[Yelem[i]][j]))
        fout.write(" );\n")
    #B
    for i in range(0, bNum):
        x0 = "0bin0"
        fout.write("ASSERT( B_" + str(i) + "[2:2] & B_" + str(i) + "[0:0] = " + x0 + "  );\n")
        fout.write("ASSERT( B_" + str(i) + "[1:1] & B_" + str(i) + "[0:0] = " + x0 + "  );\n")
    #Q
    for i in range(0, QNum, 2):
        fout.write("ASSERT( BVGE(Q_" + str(i) + ", Q_" + str(i + 1) + "));\n")

    for i in range(len(constr)):
        fout.write(constr[i]);

def Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,yN,TTstr):
    countB = 0
    countQ = 0
    countT = 0
    #the solution of previous gates outputs
    for k in range(len(TTstr)):
        fout.write("ASSERT( T_" + str(countT)+ " = 0bin"+str(tobits(TTstr[k],Size))+");\n")
        countT+=1
    for k in range(len(TTstr),GateNum+len(TTstr)):
        # encoding Q
        for q in range(2):
            fout.write("ASSERT( ")
            for i in range(bitnum):
                fout.write("( Q_" + str(countQ) + " = X_" + str(i) + ")")
                if (k == 0 and i == bitnum - 1):
                    fout.write(" );\n")
                else:
                    fout.write(" OR ")

            for i in range(countT):
                fout.write("( Q_" + str(countQ) + " = T_" + str(i) + ")")
                if (i == countT - 1):
                    fout.write(" );\n")
                else:
                    fout.write(" OR ")
            countQ = countQ + 1
        #encoding T
        xx0 = "0bin"
        xx1 = "0bin"
        for j in range(Size):
            xx0 = xx0 + "0"
            xx1 = xx1 + "1"
        fout.write(
            "ASSERT( T_" + str(countT) + " = BVXOR( ( IF B_" + str(countB) + "[2:2] = 0bin1 THEN Q_" + str(
                countQ - 2) + " & Q_" + str(
                countQ - 1) +
            " ELSE " + xx0 + " ENDIF), BVXOR((IF B_" + str(countB) + "[0:0] = 0bin1 THEN ~Q_" + str(
                countQ - 2) + " ELSE " + xx0 + " ENDIF), (IF B_" + str(
                countB) + "[1:1] = 0bin1 THEN BVXOR( Q_" + str(countQ - 2) + ",  Q_" + str(
                countQ - 1) + ") ELSE " + xx0 + " ENDIF ))) ); \n")
        countB += 1
        countT += 1
    # encoding Y
    for y in range(yN):
        fout.write("ASSERT( ")
        for i in range(GateNum+len(TTstr)):
            fout.write("( Y_" + str(y) + " =  T_" + str(i))
            if (i == GateNum+len(TTstr) - 1):
                fout.write("));\n")
            else:
                fout.write(" ) OR ")


def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")


def thread_func(t,filestr, strs):
    global result
    order = "stp -p ./" + str(filestr) + ".cvc --cryptominisat --threads 1"# > " + file + ".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    # s=(os.popen(order))
    os.system(order)
    end_time = time.time()
    # for t in threads:
    #    if
    # print(file,(end_time-start_time)*1000,'ms')

    if result==0:
        print(strs,(end_time-start_time)*1000,'ms')
        result =1
        fouts=open(filestr+".txt",'a+')
        #fouts.write(str(s.read()))
        fouts.write(str((end_time - start_time)*1000))
        fouts.close()

if __name__ == '__main__':
    yN=2 #n0 or n1 part of S-box outputs
    yystr=[] #the part of S-box output with solution if Y_2,Y_3 has solution, yystr=[2,3]

    TTstr=[] #the solution of part S-box output, its value is [T_0,T_1...]

    constr=[]#Exclude existing solutions realized by S-box NOT(T_0=0xf22f)
    
    for i in range(0,1):
        items=[] #part of S-box output without solution
        Cipherstr = cipher[i]#ciphername
        bitnum = BN[i] #number of S-box inputs
        GateNum = 8#number of gates n0 or n1
        Size = pow(2, bitnum)#2^n length
        Sbox = cipherSbox[i]#S-box
        QNum = 2 * GateNum #total number of 2-input gates' inputs  
        aNum = 4 * (2 * bitnum + GateNum - 1) * GateNum / 2 + bitnum * bitnum + GateNum * bitnum #number of variate A
        bNum = GateNum  #number of variate B
        yy=[]
        for y in range(bitnum):
            if y not in yystr:
                items.append(y)
        for c in combinations(items, yN): #Obtain any n0 outputs of S-box
            yy.append(c)
        for y0 in range(len(yy)):  #Encoding and solve any n outputs of S-box using thread
            filestr = Cipherstr+"LocalBGC"+str(y0) #encoding modle to file
            fout=open(filestr + ".cvc", 'w')
            State_Variate(fout, bitnum, Size, GateNum, QNum, bNum,yN,TTstr)  #define Variate X, Y B, T, Q
            Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, Sbox,yN,yy[y0],constr) #Constraints of X, Y B, T, Q
            Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,yN,TTstr)  #Encoding of gates' inputs and outputs, S-box outputs
            Objective(fout)
            fout.close()
            threads = []
            p = threading.Thread(target=thread_func, args=(threads,str(filestr),yy[y0],))

            p.start()
        x = 1 # flag represent finish or continue
        start_time = time.time()
        while (x):
            xx=0
            end_time = time.time()
            #if end_time - start_time > 600: #upper search time
            #    xx=1
            if result == 1:  #1: number of cipher, result represents End of solution
                x = 0
                xx=1
            if xx: #if End of solution,Close all solving commands
                order = "ps -ef|grep " + Cipherstr
                res = os.popen(order).read()
                
                for line in res.splitlines():
                    s = line.split()
                    
                    for y0 in range(len(yy)):
                        filestr = Cipherstr + "LocalBGC" + str(y0)
                        if "./" + filestr + ".cvc" in s:
                            # print(s[1])
                            r = os.popen("kill -9 " + s[1]).read()

    os._exit(0)
