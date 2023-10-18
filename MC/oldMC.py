import os
import time
import threading
from datetime import datetime
import inspect
import ctypes

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
        for j in range(inputBitNum - 1, -1, -1):
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
    CipherStr = "craft"  # cipher name
    Sbox = [12, 10, 13, 3, 14, 11, 15, 7, 8, 9, 1, 5, 0, 2, 4, 6]  # craft S-box
    MC = 8  # number of AND gates
    inputBitNum = 4  # number of S-box inputs
    for GateNum in range(MC, 1, -1):
        Size = pow(2, inputBitNum)  # 2^n length
        QNum = 2 * GateNum  # total number of 2-input gates' inputs
        aNum = (2 * (
                    inputBitNum + 1) + GateNum - 1) * GateNum + inputBitNum * inputBitNum + GateNum * inputBitNum  # number of variate A
        if not os.path.exists("./oldmc"):
            os.system("mkdir ./oldmc")
        if not os.path.exists("./oldmc/" + CipherStr):
            os.system("mkdir ./oldmc/" + CipherStr)
        filestr = "./oldmc/" + CipherStr + "/oldmc" + str(GateNum)  # encoding modle to file
        if not os.path.exists("./" + CipherStr):
            os.system("mkdir ./" + CipherStr)
        fout = open(filestr + ".cvc", 'w')
        State_Variate(fout, aNum, inputBitNum, Size, GateNum, QNum)  # define Variate X, Y A, T, Q
        Trival_Constraint(fout, aNum, inputBitNum, Size, Sbox)  # Constraints of X, Y A, T, Q
        Logic_Constraint(fout, inputBitNum, GateNum)  # Encoding of gates' inputs and outputs, S-box outputs
        Objective(fout)
        fout.close()

        order = "stp -p " + str(filestr) + ".cvc --cryptominisat --threads 1 "
        start_time = time.time()

        # os.system(order)  # Execute the command to solve
        s = (os.popen(order).read())  # s is solve
        end_time = time.time()
        fouts = open(filestr + ".txt", 'a+')
        fouts.write(str(s))
        fouts.write("searchtime:" + str((end_time - start_time) * 1000))
        fouts.close()
        print("finsh", filestr, float(end_time - start_time) * 1000.0, "ms")
