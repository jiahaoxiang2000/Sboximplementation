import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
import subprocess

A = [[0 for i in range(256)] for i in range(8)]
result=0
def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num //= 2
    return res

def State_Variate(fout, bitnum, Size, GateNum, QNum, bNum,aNum):
    #State Variate
    #x
    for i in range(bitnum):
        fout.write('X_' + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    #y
    for i in range(bitnum):
        fout.write("Y_" + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    #t
    for t in range(GateNum):
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
    for i in range(aNum):
        fout.write("A_" + str(i))
        if (i == aNum - 1):
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
    #C
    for i in range(GateNum):
        fout.write("C_" + str(i))
        if (i == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(8) + " );\n")
        else:
            fout.write(" , ")
    #Logic cost
    fout.write("Cost : ARRAY BITVECTOR(8) OF BITVECTOR(8);\n")
    #GEC
    fout.write("GEC : BITVECTOR( 8 );\n")
    fout.write("ASSERT( Cost[0bin00000000] = 0bin00000000 );\n")  #
    fout.write("ASSERT( Cost[0bin00000001] = 0bin00000000 );\n")  #
    fout.write("ASSERT( Cost[0bin00000010] = 0bin00000000 );\n")  #
    fout.write("ASSERT( Cost[0bin00000011] = 0bin00000010 );\n")  # NOT
    fout.write("ASSERT( Cost[0bin00000100] = 0bin00001001 );\n")  # XOR
    fout.write("ASSERT( Cost[0bin00000101] = 0bin00001001 );\n")  # XNOR
    fout.write("ASSERT( Cost[0bin00000111] = 0bin00000010 );\n")  # NOT
    fout.write("ASSERT( Cost[0bin00001000] = 0bin00000100 );\n")  # AND
    fout.write("ASSERT( Cost[0bin00001001] = 0bin00000011 );\n")  # NAND
    fout.write("ASSERT( Cost[0bin00001100] = 0bin00000100 );\n")  # OR
    fout.write("ASSERT( Cost[0bin00001101] = 0bin00000011 );\n")  # NOR
    fout.write("ASSERT( Cost[0bin01000000] = 0bin00000100 );\n")  # AND3
    fout.write("ASSERT( Cost[0bin01000001] = 0bin00000100 );\n")  # NAND3
    fout.write("ASSERT( Cost[0bin01100000] = 0bin00000100 );\n")  # OR3
    fout.write("ASSERT( Cost[0bin01100001] = 0bin00000100 );\n")  # NOR3
    fout.write("ASSERT( Cost[0bin00010000] = 0bin00001110 );\n")  # XOR3
    fout.write("ASSERT( Cost[0bin00010001] = 0bin00001110 );\n")  # XNOR3
    fout.write("ASSERT( Cost[0bin10000000] = 0bin00001000 );\n")  # MAOI1
    fout.write("ASSERT( Cost[0bin10000001] = 0bin00000110 );\n")  # MOAI1

def Decompose(flag,Sbox):
    for i in range(Size):
        tem = ""
        if flag == 0:
            tem = i
        else:
            tem = Sbox[i]
        for j in range(bitnum - 1, -1, -1):
            A[j][i] = tem % 2
            tem //= 2


def Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,Sbox):
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
    for i in range(bitnum):
        fout.write("ASSERT( Y_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[i][j]))
        fout.write(" );\n")
        # Q_a
    a_Start = 0
    a_counter = bitnum
    for k in range(GateNum):
        for q in range(4):
            for i in range(a_Start, a_Start + a_counter - 1):
                for j in range(i + 1, a_Start + a_counter):
                    fout.write("ASSERT( A_" + str(i) + " & A_" + str(j) + " = 0bin")
                    for j0 in range(Size):
                        fout.write("0")
                    fout.write(" );\n")
            a_Start += a_counter
        a_counter += 1

    # Y_a
    for k in range(bitnum):
        for i in range(a_Start, a_Start + a_counter - 1):
            for j in range( i + 1, a_Start + a_counter):
                fout.write( "ASSERT( A_" + str(i) + " & A_" + str(j)+ " = 0bin")
                for j0 in range(Size):
                    fout.write("0")
                fout.write(" );\n")
        a_Start += a_counter

    for i in range(aNum):
        fout.write("ASSERT( A_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write("1")
        fout.write(" OR A_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write("0")
        fout.write(" );\n")

    for i in range(bNum):
        fout.write("ASSERT( B_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write("1")
        fout.write(" OR B_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write("0")
        fout.write(" );\n")
    xx0 = "0bin"
    xx1 = "0bin"
    for j in range(Size):
        xx0 = xx0 + "0"
        xx1 = xx1 + "1"
    for i in range(0, bNum, 8):
        fout.write("ASSERT( B_" + str(i + 6) + " = " + xx1 + " => (B_" + str(
            i + 4) + " = " + xx0 + " AND B_" + str(i + 7) + " = " + xx1 + " ) );\n")

        fout.write("ASSERT( B_" + str(i + 1) + " = " + xx1 + " => (B_" + str(
            i + 3) + " = " + xx0 + " AND B_" + str(i + 4)
                   + " = " + xx0 + " AND B_" + str(i + 5) + " = " + xx0 + " AND B_" + str(
            i + 6) + " = " + xx0 + " ) );\n")
        fout.write("ASSERT( B_" + str(i + 2) + " = " + xx1 + " => (B_" + str(
            i + 1) + " = " + xx1 + " ) );\n")

        fout.write("ASSERT( B_" + str(i + 3) + " = " + xx1 + " => (B_" + str(
            i + 1) + " = " + xx0 + " AND B_" + str(i + 2)
                   + " = " + xx0 + " AND B_" + str(i + 4) + " = " + xx0 + " AND B_" + str(
            i + 5) + " = " + xx0 + " AND B_"
                   + str(i + 6) + " = " + xx0 + " ) );\n")

        fout.write("ASSERT( B_" + str(i) + " = " + xx1 + " => (B_" + str(
            i + 1) + " = " + xx0 + " AND B_" + str(i + 2)
                   + " = " + xx0 + " AND B_" + str(i + 3) + " = " + xx0 + " AND B_" + str(
            i + 4) + " = " + xx0 + " AND B_"
                   + str(i + 5) + " = " + xx0 + " AND B_" + str(i + 6) + " = " + xx0 + ") );\n")


def Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,MinGEC):
    countA = 0
    countB = 0
    countQ = 0
    countT = 0
    countX = 0
    countY = 0
    for k in range(GateNum):
        # Q
        for q in range(4):
            fout.write("ASSERT(  Q_" + str(countQ) + " = ")
            for i in range(bitnum):
                x = "A_" + str(countA) + " & X_" + str(i)
                if (k == 0 and i == bitnum - 1):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + x + ", ")
                countA += 1
            for i in range(countT):
                x = "A_" + str(countA) + " & T_" + str(i)
                if (i == countT - 1):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + x + ", ")
                countA += 1
            for i in range(bitnum + countT):
                if (i == bitnum + countT - 1):
                    fout.write(" );\n")
                else:
                    fout.write(" )")
            countQ += 1

        xx0 = "0bin"
        xx1 = "0bin"
        for j in range(Size):
            xx0 = xx0 + "0"
            xx1 = xx1 + "1"
        fout.write("ASSERT( T_" + str(countT) + " = BVXOR( B_" + str(countB) + " & Q_" + str(countQ - 4) +
                   " & Q_" + str(countQ - 3) + " & Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1)
                   + " , BVXOR( B_" + str(countB) + " & Q_" + str(countQ - 4) + " & Q_" + str(
            countQ - 3) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB) + " & Q_" + str(countQ - 4) + " & Q_" + str(
            countQ - 3) + " & Q_" + str(countQ - 1)
                   + " , BVXOR( B_" + str(countB) + " & Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1)
                   + " , BVXOR( B_" + str(countB) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB) + " & Q_" + str(countQ - 1)
                   + " , BVXOR( B_" + str(countB + 1) + " & Q_" + str(countQ - 4) + " & Q_" + str(
            countQ - 3) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB + 2) + " & Q_" + str(countQ - 4) + " & Q_" + str(countQ - 3)
                   + " , BVXOR( B_" + str(countB + 2) + " & Q_" + str(countQ - 4) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB + 2) + " & Q_" + str(countQ - 3) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB + 2) + " & Q_" + str(countQ - 4)
                   + " , BVXOR( B_" + str(countB + 2) + " & Q_" + str(countQ - 3)
                   + " , BVXOR( B_" + str(countB + 2) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB + 3) + " & Q_" + str(countQ - 4)
                   + " , BVXOR( B_" + str(countB + 3) + " & Q_" + str(countQ - 3)
                   + " , BVXOR( B_" + str(countB + 3) + " & Q_" + str(countQ - 2)
                   + " , BVXOR( B_" + str(countB + 4) + " & Q_" + str(countQ - 4) + " & Q_" + str(countQ - 3)
                   + " , BVXOR( B_" + str(countB + 5) + " & Q_" + str(countQ - 4)
                   + " , BVXOR( B_" + str(countB + 5) + " & Q_" + str(countQ - 3)
                   + " , BVXOR( B_" + str(countB + 6) + " & Q_" + str(countQ - 4)
                   + " , B_" + str(countB + 7)
                   + ") ) ) ) ) ) ) ) ) ) ) ) ) ) ) ) ) ) ) ) ) ;\n")
        countB += 8
        countT += 1
    # Y
    for y in range(bitnum):
        fout.write("ASSERT( Y_" + str(y) + " = ")
        for i in range(bitnum):
            x = " A_" + str(countA) + " & X_" + str(i)
            fout.write("BVXOR( " + x + ",")
            countA += 1
        for i in range(GateNum):
            x = " A_" + str(countA) + " & T_" + str(i)
            if (i == GateNum - 1):
                fout.write(x)
            else:
                fout.write("BVXOR( " + x + ",")
            countA += 1
        for i in range(bitnum + countT):
            if (i == bitnum + countT - 1):
                fout.write(" );\n")
            else:
                fout.write(" )")
    for i in range(GateNum):
        fout.write("ASSERT( C_" + str(i) + " = Cost[B_" + str(8 * i) + "[0:0]@B_" + str(8 * i + 1) + "[0:0]@B_" + str(
            8 * i + 2) + "[0:0]@B_" +
                   str(8 * i + 3) + "[0:0]@B_" + str(8 * i + 4) + "[0:0]@B_" + str(8 * i + 5) + "[0:0]@B_" + str(
            8 * i + 6) + "[0:0]@B_" + str(8 * i + 7) + "[0:0]] );\n")
    for i in range(GateNum):
        if (i == 0):
            fout.write("ASSERT( GEC = BVPLUS( 8 , ")
        fout.write("C_" + str(i))
        if (i == GateNum - 1):
            fout.write(" ) );\n")
        else:
            fout.write(" , ")
    fout.write("ASSERT( BVLT(GEC , 0bin" + tobits(MinGEC, 8) + ") );\n")

def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")

if __name__ == '__main__':
    Cipherstr = "PROST"
    Sbox = [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3]  # PROST
    BGC = 8  # number of gates
    bitnum = 4
    GEC=37
    for GateNum in range(BGC,1,-1):
        Size = pow(2, bitnum)
        QNum = 4 * GateNum
        aNum = 4 * (2 * bitnum + GateNum - 1) * GateNum // 2 + bitnum * bitnum + GateNum * bitnum
        bNum = 8*GateNum
        MinGEC=GEC
        if not os.path.exists("./oldgec"):
            os.system("mkdir ./oldgec")
        if not os.path.exists("./oldgec/" + Cipherstr):
            os.system("mkdir ./oldgec/" + Cipherstr)
        filestr = "./oldgec/"+Cipherstr+"/"+Cipherstr+"oldge"
        fout=open(filestr + ".cvc", 'w')
        State_Variate(fout, bitnum, Size, GateNum, QNum, bNum,aNum)
        Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, Sbox)
        Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,MinGEC)
        Objective(fout)
        fout.close()
        # start---------------
        tttstr=[]
        x = 1
        while (x):
            order = "stp -p " + str(filestr) + ".cvc  --cryptominisat --threads 1"  # > "+file+".txt "
            # print(order)
            start_time = time.time()
            # print(i,start_time)
            # s=(os.popen(order))
            # os.system(order)
            s = (os.popen(order).read())
            resultstr = s
            print(s)
            fstr = "./oldgec/" + Cipherstr + "/" + str(GateNum) + Cipherstr + str(MinGEC)
            foutc = open(fstr + ".txt", 'a+')
            foutc.write(s)
            foutc.close()
            Astr = []
            AAstr = []
            Ystr = ""
            for line in resultstr.splitlines():
                s = line.split()
                if "Valid." in s[0]:
                    x = 0
                    break
                if "Y_" in s[1]:
                    Ystr = int(s[3], 16)
                    break
            ttstr = []
            getMinGEC = ""
            for line in resultstr.splitlines():
                s = line.split()
                print(s)
                isture = 0
                if len(s) > 2 and "T_" in s[1] and int(s[3], 16) != Ystr:
                    Astr.append("".join(s))
                    ttstr.append(int(s[3], 16))
                if len(s) > 2 and "T_" in s[1]:
                    AAstr.append("".join(s))
                if len(s) > 2 and "GEC" in s[1]:
                    getMinGEC = int(s[3], 16)
                if "Valid." in s[0]:
                    x = 0
                    break
            if len(Astr) > 0:
                ttstr.sort()
                if ttstr not in tttstr:
                    filestr1 = "./oldgec/" + Cipherstr + "/" + str(GateNum) + str(MinGEC)
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
                        b1str = b1str + "OR"
                # print(b1str)
                for line in f:
                    if "ASSERT( BVLT(GEC , 0bin" + tobits(MinGEC, 8) + ") );\n" in line:
                        lines.append("ASSERT( BVLT(GEC , 0bin" + tobits(getMinGEC, 8) + ") );\n")
                        MinGEC = getMinGEC
                    else:
                        lines.append(line)
                lines.insert(4 + 2 * bitnum + GateNum, b1str)
                s = ''.join(lines)
                f.close()
                f = open(filestr + ".cvc", 'w')
                f.write(s)
                f.close()

