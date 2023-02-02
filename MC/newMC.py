import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
result =0
cipher = ["PRESENT","SKINNY","LBlock", "PROST", "RECTANGLE", "PICCOLO", "GIFT",
          "elephant","TWINE","Minalpher","Keccak","ASCON","primate"]
cipherSbox = [
    [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2],  # PRESENT
    [12, 6, 9, 0, 1, 10, 2, 11, 3, 8, 5, 13, 4, 14, 7, 15],  # SKINNY
    [14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5],  # lblock
    [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3],  # PROST
    [6, 5, 12, 10, 1, 14, 7, 9, 11, 0, 3, 13, 8, 15, 4, 2],  ##rectangle
    [14, 4, 11, 2, 3, 8, 0, 9, 1, 10, 7, 15, 6, 12, 5, 13],  # picoolo
    [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14],  # GIFT
    [14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6],  # elephant
    [12, 0, 15, 10, 2, 11, 9, 5, 8, 3, 13, 7, 1, 14, 6, 4],  # TWINE
    [11, 3, 4, 1, 2, 8, 12, 15, 5, 13, 14, 0, 6, 9, 10, 7],  # Minalpher
    [0, 5, 10, 11, 20, 17, 22, 23, 9, 12, 3, 2, 13, 8, 15, 14, 18, 21, 24, 27, 6, 1, 4, 7, 26, 29, 16, 19, 30, 25, 28, 31],  # keccak
    [4, 11, 31, 20, 26, 21, 9, 2, 27, 5, 8, 18, 29, 3, 6, 28, 30, 19, 7, 14, 0, 13, 17, 24, 16, 12, 1, 25, 22, 10, 15, 23],  # ASCON
    [1, 0, 25, 26, 17, 29, 21, 27, 20, 5, 4, 23, 14, 18, 2, 28, 15, 8, 6, 3, 13, 7, 24, 16, 30, 9, 31, 10, 22, 12, 11, 19],  # primate
]
mc = [4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 7]
BN = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5]
A = [[0 for i in range(256)] for j in range(8)]
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
    for i in range((QNum + bitnum)):
        fout.write("A_" + str(i))
        if (i == QNum + bitnum - 1):
            fout.write(" : BITVECTOR( " + str((bitnum + GateNum))+ " );\n")
        elif ((i + 1) % 2 == 0 and i < QNum - 2):
            fout.write(" : BITVECTOR( " + str((bitnum + i // 2 + 1))+ " );\n")
        else:
            fout.write(" , ")

def Decompose(flag, Sbox, Size, bitnum):
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
    Decompose(0, Sbox, Size, bitnum)
    for i in range(bitnum):
        fout.write("ASSERT( X_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[i][j]))
        fout.write(" );\n")
    # Y
    Decompose(1, Sbox, Size, bitnum)
    for i in range(bitnum):
        fout.write("ASSERT( Y_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[i][j]))
        fout.write(" );\n")

    #for i in range(QNum // 2):
    #    fout.write("ASSERT( BVGT( A_" + str(2 * i) + ", A_" + str(2 * i + 1) + " ) );\n")

def Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum):
    countA = 0
    countB = 0
    countQ = 0
    countT = 0
    countX = 0
    countY = 0
    for k in range(GateNum):
        # Q
        for q in range(2):
            fout.write("ASSERT(  Q_" + str(countQ) + " = ")
            for i in range(bitnum+1):
                x = "( IF A_" + str(countQ) + "[" + str(bitnum + countT - i) + ":" + str(
                    bitnum + countT - i) + "]=0bin1 THEN "
                xx = ""
                if (i != 0):
                    x = x + " X_" + str(i - 1)
                else:
                    xx = "0bin"
                    for j in range(Size):
                        xx = xx + str(1)
                x = x + xx + " ELSE 0bin"
                xx=""
                for j in range(Size):
                    xx = xx + str(0)
                x = x + xx
                x = x + " ENDIF )"
                if (k == 0 and i == bitnum):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + str(x) + ", ")
            for i in range(countT):
                x = "( IF A_" + str(countQ) + "[" + str(countT - 1 - i) + ":" + str(
                        countT - 1 - i) + "]=0bin0 THEN  0bin"
                xx = ""
                for j in range(Size):
                    xx = xx + str(0)
                x = x + xx + " ELSE T_" + str(i) + " ENDIF)"
                if (i == countT - 1):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + str(x) + ", ")
            for i in range(bitnum + countT + 1):
                if (i == bitnum + countT):
                    fout.write( " );\n")
                else:
                    fout.write(" )")
            countQ =countQ+1
        fout.write("ASSERT( T_" + str(countT) + " = Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1) + " );\n")
        countT += 1
        # Y
    for y in range(bitnum):
        fout.write("ASSERT(  Y_" + str(y) + " = ")
        for i in range(bitnum):
            x = "( IF A_" + str(countQ) + "[" + str(bitnum + countT - 1 - i) + ":" + str(bitnum + countT - 1 - i) + "]=0bin0 THEN 0bin"
            xx = ""
            for j in range(Size):
                xx = xx + str(0)
            x = x + xx + " ELSE  X_" + str(i) + " ENDIF )"
            fout.write("BVXOR( " + x + ", ")
        for i in range(GateNum):
            x = "( IF A_" + str(countQ) + "[" + str(countT - 1 - i) + ":" + str(countT - 1 - i) + "]=0bin0 THEN  0bin"
            xx = ""
            for j in range(Size):
                xx = xx + str(0)
            x = x + xx + " ELSE T_" + str(i) + " ENDIF )"
            if (i == GateNum - 1):
                fout.write(x)
            else:
                fout.write("BVXOR( " + x + ", ")
        for i in range( bitnum + countT):
            if (i == bitnum + countT - 1):
                fout.write(" );\n")
            else:
                fout.write(" )")
        countQ+=1
def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")

def thread_func(threads, filestr):
    global result
    order = "stp -p ./" + str(filestr) + ".cvc --cryptominisat --threads 1 > " + filestr + ".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    # s=(os.popen(order))
    os.system(order)
    end_time = time.time()
    
    if result==0:
        print(filestr, (end_time - start_time) * 1000, 'ms')
        result = 1
        fouts = open(filestr + ".txt", 'a+')
        # fouts.write(str(s.read()))
        fouts.write(str((end_time - start_time) * 1000))
        fouts.close()
        # print(i,res.read())
        # print(i, end_time - start_time)

if __name__ == '__main__':
    result = 0
    for i in range(0,1):#(len(cipher)):
        print(cipher[i])
        Cipherstr = cipher[i]
        bitnum = BN[i]
        GateNum = mc[i]
        Size = pow(2, bitnum)
        Sbox = cipherSbox[i]
        QNum = 2 * GateNum
        aNum = 4 * (2 * bitnum + GateNum - 1) * GateNum / 2 + bitnum * bitnum + GateNum * bitnum
        bNum = GateNum

        filestr = Cipherstr + "newmc"
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
            b0str = b0str + "ASSERT( BVGT(A_" + str(j) + ", A_" + str(j + 1) + "));\n"
            b1str = b1str + "ASSERT( BVGT(A_" + str(j + 1) + ", A_" + str(j) + "));\n"
        lines0 = []
        lines = []
        f = open(filestr + "0.cvc", 'r')
        s = ""
        s0 = ""
        for line in f:
            lines.append(line)
            lines0.append(line)
        lines0.insert(4 + 2 * bitnum + GateNum, b0str)
        lines.insert(4 + 2 * bitnum + GateNum, b1str)
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
            x=1
        #print(result)
        while(x):
            #print(result)
            if result == 1:#len(cipher):
                x=0
                order="ps -ef|grep "+filestr
                res=os.popen(order).read()
                #print(res)
                for line in res.splitlines():
                    s=line.split()
                    #print(s)
                    if "./"+filestr+"0.cvc" in s or "./"+filestr+"1.cvc" in s or "./"+filestr+"2.cvc" in s:
                    # print(s[1])
                        r=os.popen("kill -9 "+s[1]).read()

        os._exit(0)


