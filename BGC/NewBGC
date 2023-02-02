import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
result =0
cipher = ["x","PROST", "PICCOLO", "PICCOLO-1", "SKINNY","LBlock", "RECTANGLE", "RECTANGLE-1", "GIFT",
          "elephant","Keccak","ASCON"]
cipherSbox = [
    [0,5,3,2,6,1,4,7],#xoodyak
    [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3],  # PROST
    [14, 4, 11, 2, 3, 8, 0, 9, 1, 10, 7, 15, 6, 12, 5, 13],  # picoolo
    [6, 8, 3, 4, 1, 14, 12, 10, 5, 7, 9, 2, 13, 15, 0, 11],  # picoolo-1
    [12, 6, 9, 0, 1, 10, 2, 11, 3, 8, 5, 13, 4, 14, 7, 15],  # SKINNY
    [14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5],  # lblock
    [6, 5, 12, 10, 1, 14, 7, 9, 11, 0, 3, 13, 8, 15, 4, 2],  ##rectangle
    [9, 4, 15, 10, 14, 1, 0, 6, 12, 7, 3, 8, 2, 11, 5, 13],  # rectangle-1
    [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14],  # GIFT
    [14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6],  # elephant
    [0, 5, 10, 11, 20, 17, 22, 23, 9, 12, 3, 2, 13, 8, 15, 14, 18, 21, 24, 27, 6, 1, 4, 7, 26, 29, 16, 19, 30, 25, 28, 31],  # keccak
    [4, 11, 31, 20, 26, 21, 9, 2, 27, 5, 8, 18, 29, 3, 6, 28, 30, 19, 7, 14, 0, 13, 17, 24, 16, 12, 1, 25, 22, 10, 15, 23],  # ASCON
]
BGC=[7,8,10,10,11,11,12,12,11,14,13,16]
BN =[3,4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5]
A = [[0 for i in range(256)] for i in range(8)]

resstr = ""


def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num /= 2
    return res


def State_Variate(fout, bitnum, Size, GateNum, QNum, bNum):
    # State Variate
    for i in range(bitnum):
        fout.write('X_' + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    for i in range(bitnum):
        fout.write("Y_" + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    for t in range(GateNum):
        fout.write("T_" + str(t))
        if (t == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    for i in range(QNum):
        fout.write("Q_" + str(i))
        if (i == QNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    for i in range(bNum):
        fout.write("B_" + str(i))
        if (i == bNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")


def Decompose(flag, Sbox):
    for i in range(Size):
        tem = ""
        if flag == 0:
            tem = i
        else:
            tem = Sbox[i]
        for j in range(bitnum - 1, -1, -1):
            A[j][i] = tem % 2
            tem //= 2


def Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, Sbox):
    # Trival Constraints
    # X
    Decompose(0, Sbox)
    for i in range(bitnum):
        fout.write("ASSERT( X_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[i][j]))
        fout.write(" );\n")
    # Y
    Decompose(1, Sbox)
    for i in range(bitnum):
        fout.write("ASSERT( Y_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[i][j]))
        fout.write(" );\n")
    #B
    for i in range(0, bNum):
        x0 = "0bin0"        
        fout.write("ASSERT( B_" + str(i) + "[2:2] & B_" + str(i) + "[0:0] = " + x0 + "  );\n")
        fout.write("ASSERT( B_" + str(i) + "[1:1] & B_" + str(i) + "[0:0] = " + x0 + "  );\n")

def Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum):
    countB = 0
    countQ = 0
    countT = 0
    for k in range(GateNum):
        # Encoding Q
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

        xx0 = "0bin"
        xx1 = "0bin"
        for j in range(Size):
            xx0 = xx0 + "0"
            xx1 = xx1 + "1"
        #encoding T        
        fout.write(
            "ASSERT( T_" + str(countT) + " = BVXOR((IF B_" + str(countB) + "[2:2] =0bin1 THEN Q_" + str(countQ - 2) + " & Q_" + str(
                countQ - 1) +
            " ELSE "+xx0+" ENDIF), BVXOR((IF B_" + str(countB) + "[0:0]=0bin1 THEN ~Q_" + str(countQ - 2) + " ELSE "+xx0+" ENDIF), (IF B_" + str(
                countB) + "[1:1]=0bin1 THEN BVXOR( Q_" + str(countQ - 2) + ",  Q_" + str(countQ - 1) + ") ELSE "+xx0+" ENDIF ) ) ) ); \n")
        countB += 1
        countT += 1
    #    // encoding Y
    for y in range(bitnum):
        fout.write("ASSERT( ")
        for i in range(GateNum):
            fout.write("( Y_" + str(y) + " =  T_" + str(i))
            if (i == GateNum - 1):
                fout.write("));\n")
            else:
                fout.write(" ) OR ")


def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")

def thread_func(threads, filestr):
    global result
    order = "stp -p ./" + str(filestr) + ".cvc --cryptominisat --threads 1"# > " + filestr + ".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    # s=(os.popen(order))
    os.system(order)
    end_time = time.time()
    
    if result==0:
        print(filestr, (end_time - start_time) * 1000, 'ms')
        result=1
        fouts = open(filestr + ".txt", 'a+')
        # fouts.write(str(s.read()))
        fouts.write(str(i) + str((end_time - start_time) * 1000))
        fouts.close()
        
if __name__ == '__main__':
    result = 0
    for i in range(0,1):#(len(cipher)):
        result=0
        print(cipher[i])
        Cipherstr = cipher[i]
        bitnum = BN[i]
        GateNum =BGC[i]
        
        Size = pow(2, bitnum)
        Sbox = cipherSbox[i]
        QNum = 2 * GateNum
        aNum = 4 * (2 * bitnum + GateNum - 1) * GateNum / 2 + bitnum * bitnum + GateNum * bitnum
        bNum = GateNum

        filestr = Cipherstr+"newbgc"
        fout = open(filestr + "0.cvc", 'w')
        State_Variate(fout, bitnum, Size, GateNum, QNum, bNum)
        Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, Sbox)
        Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum)
        Objective(fout)
        fout.close()
        fout0 = open(filestr + "1.cvc", 'w')
        fout1 = open(filestr + "2.cvc", 'w')
        # fout2=open(filestr + ".txt", 'w')
        b0str = ""
        b1str = ""
        for j in range(0, QNum, 2):
            b0str = b0str + "ASSERT( BVGT(Q_" + str(j) + ", Q_" + str(j + 1) + "));\n"
            b1str = b1str + "ASSERT( BVGT(Q_" + str(j + 1) + ", Q_" + str(j) + "));\n"
        lines0 = []
        lines = []
        f = open(filestr + "0.cvc", 'r')
        s = ""
        s0 = ""
        for line in f:
            lines.append(line)
            lines0.append(line)
        lines0.insert(5 + 2 * bitnum + 2 * GateNum, b0str)
        lines.insert(5 + 2 * bitnum + 2 * GateNum, b1str)
        s = ''.join(lines)
        s0 = ''.join(lines0)
        fout0.write(s0)
        f.close()
        # fout0=open(filestr + ".cvc", 'w')
        fout1.write(s)
        fout0.close()
        fout1.close()
        # fout2.close()
        # start---------------
        # time.sleep(1)
        resstr = ""
        threads = []
        # thread_func(filestr,filestr)
        for j in range(0, 3):
            p = threading.Thread(target=thread_func, args=(threads, str(filestr) + str(j),))
            threads.append(p)
        # print(threads)
        # p.start()

        for t in threads:
            t.start()
        x = 1
        # print(result)
        while (x):
            # print(result)
            xx=0
            #end_time = time.time()
            #if end_time - start_time > 600:
            #    xx=1
            if result == 1:  # len(cipher):
                x = 0
                xx=1
            if xx:
                order = "ps -ef|grep " + Cipherstr
                res = os.popen(order).read()
                # print(res)
                for line in res.splitlines():
                    s = line.split()
                    # print(s)
                    for y0 in range(1):
                        if "./"+filestr+"0.cvc" in s or "./"+filestr+"1.cvc" in s or "./"+filestr+"2.cvc" in s:
                            # print(s[1])
                            r = os.popen("kill -9 " + s[1]).read()

        # print(result)
    os._exit(0)

