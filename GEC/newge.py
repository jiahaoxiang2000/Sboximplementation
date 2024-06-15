import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
import subprocess
from itertools import combinations

result_str = 0
result = 0
A = [[0 for i in range(256)] for i in range(8)]
# 0  UMC 180nm 1 SMIC 130nm
cost = [
    [
        "0bin00001000",
        "0bin00000110",
        "0bin00000100",
        "0bin00000011",
        "0bin00000100",
        "0bin00000011",
        "0bin00000010",
        "0bin00000010",
        "0bin00000010",
        "0bin00001110",
        "0bin00001110",
        "0bin00000110",
        "0bin00000100",
        "0bin00000110",
        "0bin00000100",
        "0bin00001000",
        "0bin00000110",
    ],
    [
        "0bin00001000",
        "0bin00001000",
        "0bin00000101",
        "0bin00000011",
        "0bin00000101",
        "0bin00000011",
        "0bin00000011",
        "0bin00000011",
        "0bin00000011",
        "0bin00010010",
        "0bin00010011",
        "0bin00000110",
        "0bin00000110",
        "0bin00000110",
        "0bin00000110",
        "0bin00001000",
        "0bin00001000",
    ],
]  # the GE of different library
Gatetype = [
    "XOR",
    "XNOR",
    "AND",
    "NAND",
    "OR",
    "NOR",
    "NOT",
    "NOT",
    "NOT",
    "XOR3",
    "XNOR3",
    "AND3",
    "NAND3",
    "OR3",
    "NOR3",
    "MAOI1",
    "MOAI1",
]
GateVal = [
    "0bin00000010",
    "0bin00000011",
    "0bin00000100",
    "0bin00000101",
    "0bin00000110",
    "0bin00000111",
    "0bin00001001",
    "0bin00001011",
    "0bin00010001",
    "0bin00010010",
    "0bin00010011",
    "0bin00100000",
    "0bin00100001",
    "0bin01110110",
    "0bin01110111",
    "0bin10110000",
    "0bin10110001",
]


def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num //= 2
    return res


def State_Variate(fout, bitnum, Size, GateNum, QNum, scl):
    # State Variate
    # x
    for i in range(bitnum):
        fout.write("X_" + str(i))
        if i == bitnum - 1:
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # y
    for i in range(bitnum):
        fout.write("Y_" + str(i))
        if i == bitnum - 1:
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # t
    for t in range(GateNum):
        fout.write("T_" + str(t))
        if t == GateNum - 1:
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # q
    for i in range(QNum):
        fout.write("Q_" + str(i))
        if i == QNum - 1:
            fout.write(" : BITVECTOR( " + str(Size) + " );\n")
        else:
            fout.write(" , ")
    # B
    for i in range(GateNum):
        fout.write("B_" + str(i))
        if i == GateNum - 1:
            fout.write(" : BITVECTOR( " + str(8) + " );\n")
        else:
            fout.write(" , ")
    # C
    for i in range(GateNum):
        fout.write("C_" + str(i))
        if i == GateNum - 1:
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
        for j in range(bit_num - 1, -1, -1):
            A[j][i] = tem % 2
            tem //= 2


def Trival_Constraint(fout, bitnum, Size, GateNum, Sbox, lg):
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
    for i in range(GateNum):
        if len(lg) > 0 and len(lg) < 17:
            fout.write("ASSERT(")
            for i0 in range(len(lg)):
                if lg[i0] in Gatetype:
                    fout.write(
                        "( B_" + str(i) + "=" + GateVal[Gatetype.index(lg[i0])] + ")"
                    )
                    if i0 < len(lg) - 1:
                        fout.write(" OR ")
            fout.write(");\n")
        else:
            fout.write(
                "ASSERT( (B_"
                + str(i)
                + "[7:3] = 0bin00000) OR (B_"
                + str(i)
                + "[7:2] = 0bin000010) OR (B_"
                + str(i)
                + "[7:2] = 0bin000100) OR (B_"
                + str(i)
                + "[7:1] = 0bin0111011) OR (B_"
                + str(i)
                + "[7:1] = 0bin0010000) OR (B_"
                + str(i)
                + "[7:1] = 0bin1011000) );\n"
            )


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
                    if depth == 0 and Tsum == 0 and i == bitnum - 1:
                        fout.write(" );\n")
                    else:
                        fout.write(" OR ")

                for i in range(Tsum):
                    fout.write("( Q_" + str(countQ) + " = T_" + str(i) + ")")
                    if i == Tsum - 1:
                        fout.write(" );\n")
                    else:
                        fout.write(" OR ")
                countQ = countQ + 1
            else:
                fout.write("ASSERT( ")

                for i in range(Tsum):
                    fout.write("( Q_" + str(countQ) + " = T_" + str(i) + ")")
                    if i == Tsum - 1:
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
        fout.write(
            "ASSERT( T_"
            + str(countT)
            + " = BVXOR((IF B_"
            + str(countB)
            + "[7:7] = 0bin1 THEN ~(Q_"
            + str(countQ - 4)
            + "&Q_"
            + str(countQ - 3)
            + ")& ~Q_"
            + str(countQ - 2)
            + "& Q_"
            + str(countQ - 1)
            + " ELSE "
            + xx0
            + " ENDIF ), BVXOR((IF B_"
            + str(countB)
            + "[6:6] = 0bin1 THEN Q_"
            + str(countQ - 2)
            + " & BVXOR(Q_"
            + str(countQ - 4)
            + ", Q_"
            + str(countQ - 3)
            + ") ELSE "
            + xx0
            + " ENDIF), BVXOR((IF B_"
            + str(countB)
            + "[5:5] = 0bin1 THEN Q_"
            + str(countQ - 4)
            + " & Q_"
            + str(countQ - 3)
            + " & Q_"
            + str(countQ - 2)
            + " ELSE  "
            + xx0
            + " ENDIF)"
            + ", BVXOR((IF B_"
            + str(countB)
            + "[4:4] = 0bin1 THEN Q_"
            + str(countQ - 2)
            + " ELSE "
            + xx0
            + " ENDIF)"
            + ", BVXOR((IF B_"
            + str(countB)
            + "[3:3] = 0bin1 THEN Q_"
            + str(countQ - 3)
            + " ELSE "
            + xx0
            + " ENDIF)"
            + ", BVXOR((IF B_"
            + str(countB)
            + "[2:2] = 0bin1 THEN Q_"
            + str(countQ - 4)
            + "& Q_"
            + str(countQ - 3)
            + " ELSE "
            + xx0
            + " ENDIF )"
            + ", BVXOR((IF B_"
            + str(countB)
            + "[1:1] = 0bin1 THEN BVXOR(Q_"
            + str(countQ - 4)
            + ",Q_"
            + str(countQ - 3)
            + ") ELSE "
            + xx0
            + " ENDIF )"
            + ", (IF B_"
            + str(countB)
            + "[0:0] = 0bin1 THEN "
            + xx1
            + " ELSE "
            + xx0
            + " ENDIF))))))))); \n"
        )
        countB += 1
        countT += 1


def Logic_Constraint(fout, bitnum, Size, GateNum, MinGEC, depth, SS):
    countB = 0
    countQ = 0
    countT = 0
    for d in range(depth):
        Logic_SubConstraint(fout, bitnum, Size, SS[d], countQ, countT, d, countB)
        countQ = countQ + 4 * SS[d]
        countT = countT + SS[d]
        countB = countB + SS[d]
    # Y
    for y in range(bitnum):
        fout.write("ASSERT( ")
        for i in range(GateNum):
            fout.write("( Y_" + str(y) + " =  T_" + str(i))
            if i == GateNum - 1:
                fout.write("));\n")
            else:
                fout.write(" ) OR ")
    for i in range(GateNum):
        fout.write("ASSERT( C_" + str(i) + " = Cost[ B_" + str(i) + "] );\n")

    for i in range(GateNum):
        if i == 0:
            fout.write("ASSERT( GEC = BVPLUS( 8 , ")
        fout.write("C_" + str(i))
        if i == GateNum - 1:
            fout.write(" ) );\n")
        else:
            fout.write(" , ")
    fout.write("ASSERT( BVLT(GEC , 0bin" + tobits(MinGEC, 8) + ") );\n")


def Objective(fout):
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")


def thread_func(threads, file):
    global result
    global result_str
    order = (
        "stp -p " + str(file) + ".cvc --cryptominisat --threads 20 > " + file + ".txt "
    )
    start_time = time.time()
    s = os.popen(order).read()
    print(s)
    result_str = s
    end_time = time.time()

    if result == 0:
        result = 1
        fouts = open(file_str + ".txt", "w")
        result_str = s
        fouts.write(s)
        fouts.write("time:" + str((end_time - start_time) * 1000))
        fouts.close()


def combination_impl(l, n, stack, length, SS):
    if n == 0:
        if len(stack) == length:
            ss = []
            for i in range(len(stack)):
                ss.append(stack[i])
            SS.append(ss)
        return
    for i in range(0, len(l)):
        if l[i] <= n:
            stack.append(l[i])
            combination_impl(l, n - l[i], stack, length, SS)
            stack.pop()
        else:
            break


if __name__ == "__main__":
    Cipherstr = "MIDORI_SB1"
    Sbox = [
        0x1,
        0x0,
        0x5,
        0x3,
        0xE,
        0x2,
        0xF,
        0x7,
        0xD,
        0xA,
        0x9,
        0xB,
        0xC,
        0x8,
        0x4,
        0x6,
    ]  # unknown
    GN = 10  # number of gates
    GEC = 60  # number of GEC
    bit_num = 4
    lg = []  # logic gate constraint
    scl = 0  # process library select
    dup = 2  # start depth
    design = 1  # depth
    for GateNum in range(GN, 1, -1):
        Size = pow(2, bit_num)
        QNum = 4 * GateNum
        bNum = GateNum
        MinGEC = GEC
        filter_list = []
        tttstr = []
        start_depth = GateNum
        if design:  # parallel implementation
            start_depth = dup
        for j in range(1, GateNum + 1):
            filter_list.append(j)
        for depth in range(start_depth, 1, -1):
            SStr = []
            combination_impl(filter_list, GateNum, [], depth, SStr)
            SStr0 = []
            # filter some level combination e.g. [1,1,5]
            for dd in range(len(SStr)):
                SS = SStr[dd]
                ff = 1
                gs = bit_num
                gx = 0
                for sd in range(len(SS)):
                    if SS[len(SS) - sd - 1] > gs + gx:
                        ff = 0
                        break
                    gx = gs + gx - SS[len(SS) - sd - 1]
                    gs = 2 * SS[len(SS) - sd - 1]
                if ff:
                    SStr0.append(SS)
            is_has_solver = 0
            print(f"SStr0 : {SStr0}")
            for d in range(len(SStr0)):
                SS = SStr0[d]
                print(f"SS : {SS}")
                sz = ""
                for dd in range(len(SS)):
                    sz = sz + str(SS[dd])

                if not os.path.exists("./gec"):
                    os.system("mkdir ./gec")
                if not os.path.exists("./gec/" + Cipherstr):
                    os.system("mkdir ./gec/" + Cipherstr)

                file_str = (
                    "./gec/"
                    + Cipherstr
                    + "/"
                    + Cipherstr
                    + "_d_"
                    + str(depth)
                    + "_"
                    + sz
                )  # encoding modle to file
                f_out = open(file_str + "_0.cvc", "w")
                State_Variate(f_out, bit_num, Size, GateNum, QNum, scl)
                Trival_Constraint(f_out, bit_num, Size, GateNum, Sbox, lg)
                Logic_Constraint(f_out, bit_num, Size, GateNum, MinGEC, depth, SS)
                Objective(f_out)
                f_out.close()
                # x = 1
                # while (x):
                order = (
                    "stp -p " + str(file_str) + "_0.cvc  --cryptominisat --threads 28"
                )  # > "+file+".txt "
                # print(order)
                start_time = time.time()
                # print(i,start_time)
                # s=(os.popen(order))
                # os.system(order)
                s = os.popen(order).read()
                end_time = time.time()
                result_str = s
                print(s)
                if "Invalid." in s:
                    print(file_str, (end_time - start_time) * 1000, "ms")
                    s = s + str((end_time - start_time) * 1000)
                    f_out_c = open(file_str + ".txt", "a+")
                    f_out_c.write(s)
                    f_out_c.close()

                # update .cvc by result
                # Astr = []
                # AAstr = []
                # Ystr = ""
                #
                # for line in result_str.splitlines():
                #     s = line.split()
                #     if "Valid." in s[0]:
                #         x = 0
                #         break
                #     if "Y_" in s[1]:
                #         Ystr = int(s[3], 16)
                #         break
                #
                # ttstr = []
                #
                # getMinGEC = ""
                # for line in result_str.splitlines():
                #     s = line.split()
                #     print(s)
                #     isture = 0
                #     if len(s) > 2 and "T_" in s[1] and int(s[3], 16) != Ystr:
                #         Astr.append("".join(s))
                #         ttstr.append(int(s[3], 16))
                #     if len(s) > 2 and "T_" in s[1]:
                #         AAstr.append("".join(s))
                #     if len(s) > 2 and "GEC" in s[1]:
                #         getMinGEC = int(s[3], 16)
                #     if "Valid." in s[0]:
                #         x = 0
                #         break
                # if len(Astr) > 0:
                #     ttstr.sort()
                #     if ttstr not in tttstr:
                #         filestr1 = "./gec/" + Cipherstr + "/" + str(GateNum) + "_" + str(MinGEC)
                #         fout1 = open(filestr1 + ".txt", 'a+')
                #         fout1.write("\n".join(AAstr) + "\n\n")
                #         fout1.close()
                #         tttstr.append(ttstr)
                #     f = open(file_str + "_0.cvc", 'r')
                #     lines = []
                #     # reduce search space by adding already result
                #     b1str = "ASSERT("
                #     for i0 in range(len(Astr)):
                #         b1str = b1str + " (NOT" + ((Astr[i0].replace("ASSERT", "")).replace(";", "")) + ") "
                #         if i0 == len(Astr) - 1:
                #             b1str = b1str + ");\n"
                #         else:
                #             b1str = b1str + "OR"
                #     # print(b1str)
                #
                #     for line in f:
                #         if design != 1 and "ASSERT( BVLT(GEC , 0bin" + tobits(MinGEC, 8) + ") );\n" in line:
                #             lines.append("ASSERT( BVLT(GEC , 0bin" + tobits(getMinGEC, 8) + ") );\n")
                #             MinGEC = getMinGEC
                #         else:
                #             lines.append(line)
                #     lines.insert(4 + 2 * bitnum + GateNum, b1str)
                #     s = ''.join(lines)
                #     f.close()
                #     f = open(file_str + "_0.cvc", 'w')
                #     f.write(s)
                #     f.close()
