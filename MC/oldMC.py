import os
import time
import threading
from datetime import datetime
import inspect
import ctypes

cipher = ["PROST", "PICCOLO", "PICCOLO-1", "LBlock", "RECTANGLE", "RECTANGLE-1", "Keccak"]
cipherSbox = [
    [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3],  # PROST
    [14, 4, 11, 2, 3, 8, 0, 9, 1, 10, 7, 15, 6, 12, 5, 13],  # picoolo
    [6, 8, 3, 4, 1, 14, 12, 10, 5, 7, 9, 2, 13, 15, 0, 11],  # picoolo-1
    [14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5],  # lblock
    [6, 5, 12, 10, 1, 14, 7, 9, 11, 0, 3, 13, 8, 15, 4, 2],  ##rectangle
    [9, 4, 15, 10, 14, 1, 0, 6, 12, 7, 3, 8, 2, 11, 5, 13],  # rectangle-1
    [0, 5, 10, 11, 20, 17, 22, 23, 9, 12, 3, 2, 13, 8, 15, 14, 18, 21, 24, 27, 6, 1, 4, 7, 26, 29, 16, 19, 30, 25, 28,
     31],  # keccak
]
mc = [8, 10, 10, 11, 12, 12, 13]  # S-box's BGC of cipher
BN = [4, 4, 4, 4, 4, 4, 5]  # number of S-box inputs
A = [[0 for i in range(256)] for j in range(8)]

resstr = ""


def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num /= 2
    return res


def State_Variate(fout, aNum, bitnum, Size, GateNum, QNum):
    # State Variate
    # X
    for i in range(bitnum):
        fout.write('X_' + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # Y
    for i in range(bitnum):
        fout.write("Y_" + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # T
    for t in range(GateNum):
        fout.write("T_" + str(t))
        if (t == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # A
    for i in range(aNum):
        fout.write("A_" + str(i))
        if (i == aNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # Q
    for i in range(QNum):
        fout.write("Q_" + str(i))
        if (i == QNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")


def Decompose(flag, Sbox):
    # get sbox's inputs and outputs
    for i in range(Size):
        tem = ""
        if flag == 0:
            tem = i
        else:
            tem = Sbox[i]
        for j in range(bitnum - 1, -1, -1):
            A[j][i] = tem % 2
            tem //= 2


def Trival_Constraint(fout, aNum, bitnum, Size, Sbox):
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
    # A
    for i in range(aNum):
        fout.write("ASSERT( A_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write("1")
        fout.write(" OR A_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write("0")
        fout.write(" );\n")


def Logic_Constraint(fout, bitnum, GateNum):
    countA = 0
    countQ = 0
    countT = 0
    for k in range(GateNum):
        # Q
        for q in range(2):
            # encoding Q, input of gates
            fout.write("ASSERT(  Q_" + str(countQ) + " = ")
            for i in range(bitnum + 1):
                x = ""
                if i == 0:
                    x = "A_" + str(countA)
                else:
                    x = "A_" + str(countA) + " & X_" + str(i - 1)
                if (k == 0 and i == bitnum):
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
            for i in range(bitnum + countT + 1):
                if (i == bitnum + countT):
                    fout.write(" );\n")
                else:
                    fout.write(" )")
            countQ += 1

        # T encoding output of gates
        fout.write("ASSERT( T_" + str(countT) + " = Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1) + " ); \n")
        countT += 1
    # Y  encoding output of S-box
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


def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")


if __name__ == '__main__':
    for i in range(1):  # (len(cipher)):
        Cipherstr = cipher[i]  # ciphername
        bitnum = BN[i]  # number of S-box inputs
        GateNum = mc[i]  # number of AND gates
        Size = pow(2, bitnum)  # 2^n length
        Sbox = cipherSbox[i]  # S-box
        QNum = 2 * GateNum  # total number of 2-input gates' inputs
        aNum = (2 * (bitnum + 1) + GateNum - 1) * GateNum + bitnum * bitnum + GateNum * bitnum  # number of variate A

        filestr = Cipherstr + "oldmc"  # encoding modle to file
        fout = open(filestr + ".cvc", 'w')
        State_Variate(fout, aNum, bitnum, Size, GateNum, QNum)  # define Variate X, Y A, T, Q
        Trival_Constraint(fout, aNum, bitnum, Size, Sbox)  # Constraints of X, Y A, T, Q
        Logic_Constraint(fout, bitnum, GateNum)  # Encoding of gates' inputs and outputs, S-box outputs
        Objective(fout)
        fout.close()

        order = "stp -p ./" + str(
            filestr) + ".cvc --cryptominisat --threads 1 "  # > "+filestr+".txt " # command: cvc to cnf for cryptominisat

        start_time = time.time()

        os.system(order)  # Execute the command to solve
        # s=(os.popen(order)) #s is solve
        end_time = time.time()
        fouts = open(filestr + ".txt", 'a+')
        # fouts.write(str(s.read()))
        fouts.write("searchtime:" + str((end_time - start_time) * 1000))
        fouts.close()
        print("finsh", filestr, float(end_time - start_time) * 1000.0, "ms")

