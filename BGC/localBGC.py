import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
import subprocess
from itertools import combinations


cipher = ["SC2000-5","fides-6","fides-5","G0","G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12","G13","G14","G15","elephant","ASCON","fides"]
cipherSbox = [
[20,26,7,31,19,12,10,15,22,30,13,14, 4,24, 9,18, 27,11, 1,21, 6,16, 2,28,23, 5, 8, 3, 0,17,29,25],
[1, 0, 25, 26, 17, 29, 21, 27, 20, 5, 4, 23, 14, 18, 2, 28,15, 8, 6, 3, 13, 7, 24, 16, 30, 9, 31, 10, 22, 12, 11, 19],
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 11, 12, 9, 3, 14, 10, 5],#G0
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 11, 14, 3, 5, 9, 10, 12],#G1
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 11, 14, 3, 10, 12, 5, 9],#G2
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 12, 5, 3, 10, 14, 11, 9],#G3
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 12, 9, 11, 10, 14, 5, 3],#G4
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 12, 11, 9, 10, 14, 3, 5],#G5
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 12, 11, 9, 10, 14, 5, 3],#G6
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 12, 14, 11, 10, 9, 3, 5],#G7
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 9, 5, 10, 11, 3, 12],#G8
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 11, 3, 5, 9, 10, 12],#G9
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 11, 5, 10, 9, 3, 12],#G10
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 11, 10, 5, 9, 12, 3],#G11
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 11, 10, 9, 3, 12, 5],#G12
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 12, 9, 5, 11, 10, 3],#G13
[ 0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 12, 11, 3, 9, 5, 10],#G14
[0, 1, 2, 13, 4, 7, 15, 6, 8, 14, 12, 11, 9, 3, 10, 5],#G15
    [14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6],  # elephant
    [4, 11, 31, 20, 26, 21, 9, 2, 27, 5, 8, 18, 29, 3, 6, 28, 30, 19, 7, 14, 0, 13, 17, 24, 16, 12, 1, 25, 22, 10, 15, 23],  # ASCON
    [54, 0, 48, 13, 15, 18, 35, 53, 63, 25, 45, 52, 3, 20, 33, 41, 8, 10, 57, 37, 59, 36, 34, 2, 26, 50, 58, 24, 60, 19, 
     14, 42, 46, 61, 5, 49, 31, 11, 28, 4, 12, 30, 55, 22, 9, 6, 32, 23, 27, 39, 21, 17, 16, 29, 62, 1, 40, 47, 51, 56, 7, 43, 38, 44],#fides-6

]
bgc=[25,17,8]
BN = [4, 5,6]
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
        fout.write(constr[i])


def Logic_SubConstraint(fout, bitnum, Size, GateNum, Qsum, Tsum, depth,p):
    countQ = Qsum
    countT = Tsum
    for k in range(GateNum):
        # Encoding Q
        for q in range(2):
            if depth == 0 or q == 0 or p==0:
                fout.write("ASSERT( ")
                for i in range(bitnum):
                    fout.write("( Q_" + str(countQ) + " = X_" + str(i) + ")")
                    if (depth == 0 and i == bitnum - 1):
                        fout.write(" );\n")
                    else:
                        fout.write(" OR ")

                for i in range(Tsum):
                    fout.write("( Q_" + str(countQ) + " = T_" + str(i) + ")")
                    if (i == Tsum - 1):
                        fout.write(" );\n")
                    else:
                        fout.write(" OR ")
                countQ = countQ + 1
            else:
                fout.write("ASSERT( ")

                for i in range(Tsum):
                    fout.write("( Q_" + str(countQ) + " = T_" + str(i) + ")")
                    if (i == Tsum - 1):
                        fout.write(" );\n")
                    else:
                        fout.write(" OR ")
                countQ = countQ + 1
        xx0 = "0bin"
        xx1 = "0bin"
        for j in range(Size):
            xx0 = xx0 + "0"
            xx1 = xx1 + "1"
        # encoding T
        #fout.write(
        #    "ASSERT( BVGT(T_" + str(countT)+","+xx0+"));\n")
        #for t in range(0,countT):
        #    fout.write(
        #    "ASSERT( NOT(T_" + str(countT)+" = T_"+str(t)+"));\n")
        fout.write(
            "ASSERT( T_" + str(countT) + " = BVXOR((IF B_" + str(countT) + "[2:2] =0bin1 THEN Q_" + str(
                countQ - 2) + " & Q_" + str(
                countQ - 1) +
            " ELSE " + xx0 + " ENDIF), BVXOR((IF B_" + str(countT) + "[0:0]=0bin1 THEN ~Q_" + str(
                countQ - 2) + " ELSE " + xx0 + " ENDIF), (IF B_" + str(
                countT) + "[1:1]=0bin1 THEN BVXOR( Q_" + str(countQ - 2) + ",  Q_" + str(
                countQ - 1) + ") ELSE " + xx0 + " ENDIF ) ) ) ); \n")
        countT += 1


def Logic_Constraint(fout, bitnum, Size, GateNum, depth,SS,yN,p):
    countB = 0
    countQ = 0
    countT = 0
    lenght = bitnum
    for d in range(depth):
        # print(d,countT)
        Logic_SubConstraint(fout, bitnum, Size, SS[d], countQ, countT, d, p)
        countQ = countQ + 2 * SS[d]
        countT = countT + SS[d]
        lenght = lenght + SS[d]
        # print(lenght)
        # Y
    #    // encoding Y
    for y in range(yN):
        fout.write("ASSERT( ")
        for i in range(GateNum):
            fout.write("( Y_" + str(y) + " =  T_" + str(i))
            if (i == GateNum - 1):
                fout.write("));\n")
            else:
                fout.write(" ) OR ")


def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")


def thread_func(t,filestr, strs):
    global result
    order = "stp -p " + str(filestr) + ".cvc --cryptominisat --threads 1"# > " + file + ".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    s=(os.popen(order).read())
    #os.system(order)
    end_time = time.time()
    # for t in threads:
    #    if
    # print(file,(end_time-start_time)*1000,'ms')

    if "Invalid." in s:
        result =strs
        print(s,filestr, strs,(end_time-start_time)*1000,'ms')
        fouts=open(filestr+"Y.txt",'a+')
        fouts.write(str(s))
        fouts.write(str((end_time - start_time)*1000))
        fouts.close()
    elif "Valid." in s:        
        result =strs
        print(s,filestr, strs,(end_time-start_time)*1000,'ms')
        fouts=open(filestr+"N.txt",'a+')
        fouts.write(str(s))
        fouts.write(str((end_time - start_time)*1000))
        fouts.close()
def combination_impl(l, n, stack,length,SS):
    if n == 0:
        if len(stack)==length:
            ss=[]
            for i in range(len(stack)):
                ss.append(stack[i])
            #print(ss)
            SS.append(ss)
        return
    for i in range(0, len(l)):
        if l[i] <= n:
            stack.append(l[i])
            combination_impl(l, n - l[i], stack,length,SS)
            stack.pop()
        else:
            break

if __name__ == '__main__':
    n0=1 #part of S-box outputs
    yystr=[] #the part of S-box output with solution if Y_2,Y_3 has solution, yystr=[2,3]

    TTstr=[] #the solution of part S-box output, its value is [T_0,T_1...]

    constr=[]#Exclude existing solutions realized by S-box NOT(T_0=0xf22f)
    Cipherstr = "PROST"#ciphername
    Sbox = [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3]  # #S-box
    BGC = 8  # number of gates n0 or n1
    bitnum = 4  #number of S-box inputs
    d = 2  # depth
    p=0#parallel sign
    for GateNum in range(BGC,1,-1):
        result =0
        items=[] #part of S-box output without solution
        Size = pow(2, bitnum)#2^n length
        QNum = 2 * GateNum #total number of 2-input gates' inputs
        bNum = GateNum  #number of variate B
        yy=[]
        l=[]
        for j in range(1, GateNum + 1):
            l.append(j)
        for y in range(bitnum):
            if y not in yystr:
                items.append(y)
        for c in combinations(items, n0): #Obtain any n0 outputs of S-box
            yy.append(c)

        stardepth = GateNum
        enddepth = GateNum-1
        if p:#parallel implementation
            stardepth=d
            enddepth=1
        for depth in range(stardepth, enddepth,-1):
            SStr = []
            combination_impl(l, GateNum, [], depth, SStr)
            SStr0=[]
            for dd in range(len(SStr)):
                SS = SStr[len(SStr) - dd - 1]
                ff=1
                gs=n0
                g0=0
                for sd in range(len(SS)):
                    if SS[len(SS)-sd-1]>gs+g0:
                        ff=0
                        break
                    g0=g0+gs-SS[len(SS)-sd-1]
                    gs=2*SS[len(SS)-sd-1]
                if(ff):
                    SStr0.append(SS)
            x=1
            val=1
            issolver=0
            for d in range(len(SStr0)):
                result=0
                SS=SStr0[d]
                for y0 in range(len(yy)):  #Encoding and solve any n outputs of S-box using thread
                    strz=""
                    for yy0 in range(len(yy[y0])):
                        strz=strz+str(yy[y0][yy0])
                    print(d,Cipherstr,SS)
                    if not os.path.exists("./localbgc"):
                        os.system("mkdir ./localbgc")
                    if not os.path.exists("./localbgc/"+Cipherstr):
                        os.system("mkdir ./localbgc/"+Cipherstr)
                    if not os.path.exists("./localbgc/"+Cipherstr+"/11"):
                        os.system("mkdir ./localbgc/"+Cipherstr+"/11")
                    filestr = "./localbgc/"+Cipherstr+"/11/"+Cipherstr+"LocalBGC"+str(GateNum)+strz #encoding modle to file
                    fout=open(filestr + ".cvc", 'w')
                    State_Variate(fout, bitnum, Size, GateNum, QNum, bNum,n0,TTstr)  #define Variate X, Y, B, T, Q
                    Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, Sbox,n0,yy[y0],constr) #Constraints of X, Y, B, T, Q
                    Logic_Constraint(fout, bitnum, Size, GateNum, depth,SS,n0,p) #Encoding of gates' inputs and outputs, S-box outputs
                    Objective(fout)
                    fout.close()
                    tttstr=[]
                    x=1
                    xx=0
                    while (x):
                        order = "stp -p " + str(filestr) + ".cvc  --cryptominisat --threads 1"  # > "+file+".txt "
                        #print(order)
                        start_time = time.time()
                        # print(i,start_time)
                        # s=(os.popen(order))
                        # os.system(order)
                        s = (os.popen(order).read())
                        resultstr = s
                        print(s,filestr)
                        if "Invalid." in s:
                            issolver=1
                            Astr = []
                            AAstr = []
                            Ystr = ""
                            for line in resultstr.splitlines():
                                s0 = line.split()
                                if "Y_" in s0[1]:
                                    Ystr = int(s0[3], 16)
                                    break
                            ttstr = []
                            for line in resultstr.splitlines():
                                s0 = line.split()
                                isture = 0
                                print(s0)
                                if len(s0) > 2 and "T_" in s0[1] and int(s0[3], 16) != Ystr:
                                    Astr.append("".join(s0))
                                    ttstr.append(int(s0[3], 16))
                                if len(s0) > 2 and "T_" in s0[1]:
                                    AAstr.append("".join(s0))
                            fstr = "./localbgc/"+Cipherstr+"/11/" + Cipherstr+str(GateNum)+strz +str(depth)
                            foutc = open(fstr + ".txt", 'a+')
                            foutc.write(s)
                            foutc.close()
                            if len(Astr) > 0:
                                ttstr.sort()
                                if ttstr not in tttstr:
                                    filestr1 = "./localbgc/"+Cipherstr+"/11/" + str(GateNum)+strz  +str(depth)
                                    fout1 = open(filestr1 + ".txt", 'a+')
                                    fout1.write("\n".join(AAstr) + "\n\n")
                                    fout1.close()
                                    tttstr.append(ttstr)
                                f = open(filestr + ".cvc", 'r')
                                lines = []
                                b1str = "ASSERT("
                                for i0 in range(len(Astr)):
                                    b1str = b1str + " (NOT" + ((Astr[i0].replace("ASSERT", "")).replace(";", "")) + ") "
                                    if i0 == len(Astr) - 1:
                                        b1str = b1str + ");\n"
                                    else:
                                        b1str = b1str + "AND"
                                # print(b1str)
                                for line in f:
                                    lines.append(line)
                                lines.insert(4 + 2 * bitnum + GateNum, b1str)
                                s = ''.join(lines)
                                f.close()
                                f = open(filestr + ".cvc", 'w')
                                f.write(s)
                                f.close()
                        else:
                            filestr = "./localbgc/"+Cipherstr+"/11/"+Cipherstr+"LocalBGC"+str(GateNum)+strz #encoding modle to file
                            os.system("rm -f "+ filestr+".cvc")
                            x=0
                            xx=1
                if issolver:
                    break
