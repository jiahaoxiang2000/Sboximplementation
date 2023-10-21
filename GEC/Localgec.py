import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
import subprocess
from itertools import combinations

A = [[0 for i in range(256)] for j in range(8)]
result = 0
result_str = 0

cost = [
    ["0bin00001000", "0bin00000110",
     "0bin00000100", "0bin00000011",
     "0bin00000100", "0bin00000011",
     "0bin00000010", "0bin00000010",
     "0bin00000010", "0bin00001110",
     "0bin00001110", "0bin00000110",
     "0bin00000100", "0bin00000110",
     "0bin00000100", "0bin00001000",
     "0bin00000110"],
    ["0bin00001000", "0bin00001000",
     "0bin00000101", "0bin00000011",
     "0bin00000101", "0bin00000011",
     "0bin00000011", "0bin00000011",
     "0bin00000011", "0bin00010010",
     "0bin00010011", "0bin00000110",
     "0bin00000110", "0bin00000110",
     "0bin00000110", "0bin00001000",
     "0bin00001000"]
]  # the GE of different library
Gatetype = ["XOR", "XNOR", "AND", "NAND", "OR", "NOR", "NOT", "NOT", "NOT", "XOR3", "XNOR3",
            "AND3", "NAND3", "OR3", "NOR3", "MAOI1", "MOAI1"]
GateVal = ["0bin00000010", "0bin00000011", "0bin00000100", "0bin00000101", "0bin00000110",
           "0bin00000111", "0bin00001001", "0bin00001011", "0bin00010001", "0bin00010010",
           "0bin00010011", "0bin00100000", "0bin00100001", "0bin01110110", "0bin01110111",
           "0bin10110000", "0bin10110001"]


def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num //= 2
    return res


def State_Variate(fout, bitnum, Size, GateNum, QNum, scl, yN, TTstr):
    # State Variate
    # x
    for i in range(bitnum):
        fout.write('X_' + str(i))
        if (i == bitnum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # y
    for i in range(yN):
        fout.write("Y_" + str(i))
        if (i == yN - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # t
    for t in range(GateNum + len(TTstr)):
        fout.write("T_" + str(t))
        if (t == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # q
    for i in range(QNum):
        fout.write("Q_" + str(i))
        if (i == QNum - 1):
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # B
    for i in range(GateNum):
        fout.write("B_" + str(i))
        if (i == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(8) + " );\n")
        else:
            fout.write(" , ")
    # C
    for i in range(GateNum):
        fout.write("C_" + str(i))
        if (i == GateNum - 1):
            fout.write(" : BITVECTOR( " + str(8) + " );\n")
        else:
            fout.write(" , ")
    # Logic cost
    fout.write("Cost : ARRAY BITVECTOR(8) OF BITVECTOR(8);\n")
    # GEC
    fout.write("GEC : BITVECTOR( 8 );\n")
    fout.write("ASSERT( Cost[0bin00000000] = 0bin00000000 );\n")
    fout.write("ASSERT( Cost[0bin00000001] = 0bin00000000 );\n")
    fout.write("ASSERT( Cost[0bin00001000] = 0bin00000000 );\n")
    fout.write("ASSERT( Cost[0bin00001010] = 0bin00000000 );\n")
    fout.write("ASSERT(Cost[0bin00010000] = 0bin00000000 );\n")
    fout.write("ASSERT( Cost[0bin00000010] = " + cost[scl][0] + " );\n")  # XOR
    fout.write("ASSERT( Cost[0bin00000011] = " + cost[scl][1] + " );\n")  # XNOR
    fout.write("ASSERT( Cost[0bin00000100] = " + cost[scl][2] + " );\n")  # AND
    fout.write("ASSERT( Cost[0bin00000101] = " + cost[scl][3] + " );\n")  # NAND
    fout.write("ASSERT( Cost[0bin00000110] = " + cost[scl][4] + " );\n")  # OR
    fout.write("ASSERT( Cost[0bin00000111] = " + cost[scl][5] + " );\n")  # NOR
    fout.write("ASSERT( Cost[0bin00001001] = " + cost[scl][6] + " );\n")  # NOT
    fout.write("ASSERT( Cost[0bin00001011] = " + cost[scl][7] + " );\n")  # NOT
    fout.write("ASSERT( Cost[0bin00010001] = " + cost[scl][8] + " );\n")  # NOT
    fout.write("ASSERT( Cost[0bin00010010] = " + cost[scl][9] + " );\n")  # XOR3
    fout.write("ASSERT( Cost[0bin00010011] = " + cost[scl][10] + " );\n")  # XNOR3
    fout.write("ASSERT( Cost[0bin00100000] = " + cost[scl][11] + " );\n")  # AND3
    fout.write("ASSERT( Cost[0bin00100001] = " + cost[scl][12] + " );\n")  # NAND3
    fout.write("ASSERT( Cost[0bin01110110] = " + cost[scl][13] + " );\n")  # OR3
    fout.write("ASSERT( Cost[0bin01110111] = " + cost[scl][14] + " );\n")  # NOR3
    fout.write("ASSERT( Cost[0bin10110000] = " + cost[scl][15] + " );\n")  # MAOI1
    fout.write("ASSERT( Cost[0bin10110001] = " + cost[scl][16] + " );\n")  # MOAI1


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


def Trival_Constraint(fout, bitnum, Size, GateNum, Sbox, yN, Yelem, constr, lg):
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
    for i in range(yN):
        fout.write("ASSERT( Y_" + str(i) + " = 0bin")
        for j in range(Size):
            fout.write(str(A[Yelem[i]][j]))
        fout.write(" );\n")
    for i in range(GateNum):
        if len(lg) > 0 and len(lg) < 17:
            fout.write("ASSERT(")
            for i0 in range(len(lg)):
                if lg[i0] in Gatetype:
                    fout.write("( B_" + str(i) + "=" + GateVal[Gatetype.index(lg[i0])] + ")")
                    if i0 < len(lg) - 1:
                        fout.write(" OR ")
            fout.write(");\n")
        else:
            fout.write("ASSERT( (B_" + str(i) + "[7:3] = 0bin00000) OR (B_" + str(i) + "[7:2] = 0bin000010) OR (B_" +
                       str(i) + "[7:2] = 0bin000100) OR (B_" + str(i) + "[7:1] = 0bin0111011) OR (B_" +
                       str(i) + "[7:1] = 0bin0010000) OR (B_" + str(i) + "[7:1] = 0bin1011000) );\n")


def Logic_SubConstraint(fout, bitnum, Size, GateNum, Qsum, Tsum, depth, Bsum):
    countQ = Qsum
    countT = Tsum
    countB = Bsum
    for k in range(GateNum):
        for q in range(4):
            if depth == 0 or q == 0 or q == 2:
                fout.write("ASSERT( ")
                for i in range(bitnum):
                    fout.write("( Q_" + str(countQ) + " = X_" + str(i) + ")")
                    if (depth == 0 and Tsum == 0 and i == bitnum - 1):
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

        fout.write("ASSERT( T_" + str(countT) + " = BVXOR((IF B_" + str(countB) + "[7:7] = 0bin1 THEN ~(Q_" + str(
            countQ - 4) + "&Q_" +
                   str(countQ - 3) + ")& ~Q_" + str(countQ - 2) + "& Q_" + str(countQ - 1) + " ELSE " + xx0 +
                   " ENDIF ), BVXOR((IF B_" + str(countB) + "[6:6] = 0bin1 THEN Q_" + str(countQ - 2) +
                   " & BVXOR(Q_" + str(countQ - 4) + ", Q_" + str(countQ - 3) + ") ELSE " + xx0 +
                   " ENDIF), BVXOR((IF B_" + str(countB) + "[5:5] = 0bin1 THEN Q_" + str(countQ - 4) + " & Q_" +
                   str(countQ - 3) + " & Q_" + str(countQ - 2) + " ELSE  " + xx0 + " ENDIF)"
                   + ", BVXOR((IF B_" + str(countB) + "[4:4] = 0bin1 THEN Q_" + str(
            countQ - 2) + " ELSE " + xx0 + " ENDIF)"
                   + ", BVXOR((IF B_" + str(countB) + "[3:3] = 0bin1 THEN Q_" + str(
            countQ - 3) + " ELSE " + xx0 + " ENDIF)"
                   + ", BVXOR((IF B_" + str(countB) + "[2:2] = 0bin1 THEN Q_" + str(countQ - 4) + "& Q_" + str(
            countQ - 3) + " ELSE " + xx0 + " ENDIF )"
                   + ", BVXOR((IF B_" + str(countB) + "[1:1] = 0bin1 THEN BVXOR(Q_" + str(countQ - 4) + ",Q_" + str(
            countQ - 3) + ") ELSE " + xx0 + " ENDIF )"
                   + ", (IF B_" + str(
            countB) + "[0:0] = 0bin1 THEN " + xx1 + " ELSE " + xx0 + " ENDIF))))))))); \n")
        countB += 1
        countT += 1


def Logic_Constraint(fout, bitnum, Size, GateNum, MinGEC, depth, SS, yN, TTstr):
    countB = 0
    countQ = 0
    countT = 0
    for k in range(0, len(TTstr)):
        fout.write(TTstr[k] + "\n")
        countT += 1
    for d in range(depth):
        Logic_SubConstraint(fout, bitnum, Size, SS[d], countQ, countT, d, countB)
        countQ = countQ + 4 * SS[d]
        countT = countT + SS[d]
        countB = countB + SS[d]
    # Y
    for y in range(yN):
        fout.write("ASSERT( ")
        for i in range(GateNum + len(TTstr)):
            fout.write("( Y_" + str(y) + " =  T_" + str(i))
            if (i == GateNum + len(TTstr) - 1):
                fout.write("));\n")
            else:
                fout.write(" ) OR ")
    for i in range(GateNum):
        fout.write("ASSERT( C_" + str(i) + " = Cost[ B_" + str(i) + "] );\n")

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


def thread_func(threads, filestr):
    global result
    global result_str
    order = "stp -p " + str(filestr) + ".cvc "  # > " + filestr + ".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    # s=(os.popen(order))
    # os.system(order)
    s = (os.popen(order).read())
    print(s)
    resultstr = s
    end_time = time.time()
    # for t in threads:
    #    if
    # print(file,(end_time-start_time)*1000,'ms')

    if result == 0:
        # print(filestr,(end_time-start_time)*1000,'ms')
        result = 1
        fouts = open(filestr + ".txt", 'w')
        # resultstr=s
        fouts.write(s)
        fouts.write("time:" + str((end_time - start_time) * 1000))
        fouts.close()


def combination_impl(l, n, stack, length, SS):
    if n == 0:
        if len(stack) == length:
            ss = []
            for i in range(len(stack)):
                ss.append(stack[i])
            # print(ss)
            SS.append(ss)
        return
    for i in range(0, len(l)):
        if l[i] <= n:
            stack.append(l[i])
            combination_impl(l, n - l[i], stack, length, SS)
            stack.pop()
        else:
            break


if __name__ == '__main__':
    Cipherstr = "PROST"
    Sbox = [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3]  # PROST
    GN = 8  # number of gates
    GEC = 37  # number of gates
    bitnum = 4
    lg = ["NAND", "OR"]
    scl = 1
    dup = 4
    dsign = 1  # depth

    for GateNum in range(13, 14):
        y0 = []
        # y0 = [2]
        # y0.append(k0)
        yN = 1
        yystr = []  # [0,2]#[0,1,2]#[2,3,4]

        TTstr = []  # [ 0x0FF0,0x33CC,0x32E5,0x9B70,0xCC33,0xCFF3,0x0303,0x5656,0x59A6,0xFCC0,0xA995,0xFED6]

        constr = []
        result = 0
        for GateNum in range(GN, 1, -1):
            items = []
            result = 0
            MinGEC = GEC
            Size = pow(2, bitnum)
            QNum = 4 * GateNum
            bNum = GateNum

            yy = []
            l = []
            for y in range(bitnum):
                if y not in yystr:
                    items.append(y)
            for c in combinations(items, yN):  # Obtain any n0 outputs of S-box
                yy.append(c)
            tttstr = [[]]
            for j in range(1, GateNum + 1):
                l.append(j)
            issolver = 0
            stardepth = GateNum
            if dsign:  # parallel implementation
                stardepth = dup
            for depth in range(stardepth, 1, -1):
                SStr = []
                combination_impl(l, GateNum, [], depth, SStr)
                SStr0 = []
                for dd in range(len(SStr)):
                    SS = SStr[len(SStr) - dd - 1]
                    ff = 1
                    gs = yN
                    g0 = 0
                    for sd in range(len(SS)):
                        if SS[len(SS) - sd - 1] > gs + g0:
                            ff = 0
                            break
                        g0 = g0 + gs - SS[len(SS) - sd - 1]
                        gs = 2 * SS[len(SS) - sd - 1]
                    if (ff):
                        SStr0.append(SS)
                for d in range(len(SStr0)):
                    # print(d, ss,sum, GateNum, depth)
                    SS = SStr0[d]
                    for y in range(len(yy)):  # Encoding and solve any n outputs of S-box using thread
                        y0 = yy[y]
                        sz = ""
                        for szindex in range(len(y0)):
                            sz = sz + str(y0[szindex])
                        print(y0, SS)
                        filestr = "./localgec/" + Cipherstr + "/11"

                        if not os.path.exists("./localgec"):
                            os.system("mkdir ./localgec")
                        if not os.path.exists("./localgec" + Cipherstr):
                            os.system("mkdir ./localgec/" + Cipherstr)
                        if not os.path.exists("./localgec/" + Cipherstr + "/11"):
                            os.system("mkdir ./localgec/" + Cipherstr + "/11")
                        filestr = "./localgec/" + Cipherstr + "/11/" + Cipherstr + "GEC" + str(MinGEC) + str(GateNum) + sz
                        fout = open(filestr + ".cvc", 'w')
                        State_Variate(fout, bitnum, Size, GateNum, QNum, scl, yN, TTstr)
                        Trival_Constraint(fout, bitnum, Size, GateNum, Sbox, yN, y0, constr,lg)
                        Logic_Constraint(fout, bitnum, Size, GateNum, MinGEC, depth, SS, yN, TTstr)
                        Objective(fout)
                        fout.close()
                        x = 1
                        while (x):
                            order = "stp -p " + str(filestr) + ".cvc  --cryptominisat --threads 1"  # > "+file+".txt "
                            # print(order)
                            start_time = time.time()
                            # print(i,start_time)
                            # s=(os.popen(order))
                            # os.system(order)
                            s = (os.popen(order).read())
                            result_str = s
                            print(s)
                            if "Invalid." in s:
                                issolver = 1
                                Astr = []
                                AAstr = []
                                Ystr = ""
                                for line in result_str.splitlines():
                                    s0 = line.split()
                                    if "Valid." in s0[0]:
                                        # MinGEC=MinGEC+1
                                        x = 0
                                        break
                                    if "Y_" in s0[1]:
                                        Ystr = int(s0[3], 16)
                                        break
                                ttstr = []
                                GE = 0
                                for line in result_str.splitlines():
                                    s0 = line.split()
                                    isture = 0
                                    print(s0)
                                    if len(s0) > 2 and "T_" in s0[1] and int(s0[3], 16) != Ystr:
                                        Astr.append("".join(s0))
                                        ttstr.append(int(s0[3], 16))
                                    if len(s0) > 2 and "T_" in s0[1]:
                                        AAstr.append("".join(s0))
                                    if len(s0) > 2 and "GEC" in s0[1]:
                                        GE = int(s0[3], 16)
                                if dsign!=1 and MinGEC> GE:
                                    MinGEC = GE
                                fstr = "./localgec/" + Cipherstr + "/11/" + Cipherstr + str(
                                    GE) + "GE" + sz + "Gate" + str(GateNum)
                                foutc = open(fstr + ".txt", 'a+')
                                foutc.write(s)
                                foutc.close()
                                # else:
                                #    AAstr.append(s)
                                # print(AAstr)
                                # print(Astr)
                                # print(Ystr)
                                if len(Astr) > 0:
                                    ttstr.sort()
                                    # print(ttstr,tttstr)
                                    if (len(tttstr) < y + 1) or ((len(tttstr) > y) and ttstr not in tttstr[y]):
                                        filestr1 = "./localgec/" + Cipherstr + "/11/" + str(
                                            GE) + "GE" + sz + "Gate" + str(GateNum)
                                        fout1 = open(filestr1 + ".txt", 'a+')
                                        fout1.write("\n".join(AAstr) + "\n\n")
                                        fout1.close()
                                        if len(tttstr) < y + 1:
                                            tttstr.append(ttstr)
                                        else:
                                            tttstr[y].append(ttstr)
                                    f = open(filestr + ".cvc", 'r')
                                    lines = []
                                    b1str = "ASSERT("
                                    for i0 in range(len(Astr)):
                                        b1str = b1str + " (NOT" + (
                                            (Astr[i0].replace("ASSERT", "")).replace(";", "")) + ") "
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
                                filestr = "./localgec/"+Cipherstr+"/11/" + Cipherstr + "GEC" +str(MinGEC)+ str(GateNum)+sz
                                os.system("rm -f "+ filestr+".cvc")
                                x = 0

