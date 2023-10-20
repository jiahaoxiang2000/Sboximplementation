import os
import time
import threading
from datetime import datetime
import inspect
import ctypes

result = 0

A = [[0 for i in range(256)] for j in range(8)]
resstr = ""
resultstr = ""


def tobits(num, bit_len):
    # tobinary string
    res = ""
    for pos in range(bit_len):
        res = str(num % 2) + res
        num /= 2
    return res


def State_Variate(fout, bitnum, Size, GateNum, QNum, bNum, SS):
    """
    write X Y T Q A all define
    :param fout: wirte file handler
    :param bitnum: sbox input bit
    :param Size: 2**bitnum
    :param GateNum: number of Gate
    :param QNum: input wire number of gate
    :param bNum:
    :param SS: number of gate in different depth
    """
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
    # print(SS)
    len0 = 1
    sum = SS[0]
    star = 0
    for i in range((QNum + bitnum * bitnum)):
        fout.write("A_" + str(i))
        if i == QNum + (bitnum * bitnum) - 1:
            fout.write(" : BITVECTOR( " + str((bitnum + GateNum)) + " );\n")
        elif ((i + 1) % 2 == 0 and i < QNum):
            fout.write(" : BITVECTOR( " + str((bitnum + len0)) + " );\n")
            if (2 * sum == i + 1):
                len0 = len0 + +SS[star]
                if star < len(SS) - 1:
                    sum = sum + SS[star + 1]
                    star = star + 1
            # print("sum",sum,"le0",len0)
        else:
            fout.write(" , ")
        # print(i,len0)


def Decompose(flag, Sbox, Size, bitnum):
    """
    decompose S-box ; letter endian
    :param flag:  0: X 1:Y
    :param Sbox:  S-box
    :param Size:  size of S-box
    :param bitnum: number of S-box inputs
    """
    # i is size of S-box equal 2**bitNum
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
    """
        set input and output of S-box constraints
    :param fout: file
    :param bitnum: bit number of sbox input
    :param Size: binary number of sbox input value
    :param GateNum: gate number of sbox
    :param QNum: input number of gate
    :param bNum:
    :param Sbox: sbox
    """
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

    # for i in range(QNum // 2):
    #    fout.write("ASSERT( BVGT( A_" + str(2 * i) + ", A_" + str(2 * i + 1) + " ) );\n")


def Logic_SubConstraint(fout, bitnum, Size, GateNum, Qsum, Tsum, depth, lenght):
    """
        write Q and T constraints
    :param fout: file
    :param bitnum:
    :param Size:
    :param GateNum:
    :param Qsum:
    :param Tsum:
    :param depth:
    :param lenght:
    """
    countQ = Qsum
    countT = Tsum
    for k in range(GateNum):
        # Q
        for q in range(2):
            fout.write("ASSERT(  Q_" + str(countQ) + " = ")
            for i in range(bitnum + 1):
                x = "( IF A_" + str(countQ) + "[" + str(lenght - i) + ":" + str(lenght - i) + "]=0bin1 THEN "
                xx = ""
                if (i != 0):
                    x = x + " X_" + str(i - 1)
                else:
                    xx = "0bin"
                    for j in range(Size):
                        xx = xx + str(1)
                x = x + xx + " ELSE 0bin"
                xx = ""
                for j in range(Size):
                    xx = xx + str(0)
                x = x + xx
                x = x + " ENDIF )"
                if (depth == 0 and i == bitnum):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + str(x) + ", ")
            for i in range(Tsum):
                x = "( IF A_" + str(countQ) + "[" + str(lenght - bitnum - 1 - i) + ":" + str(
                    lenght - bitnum - 1 - i) + "]=0bin0 THEN  0bin"
                xx = ""
                for j in range(Size):
                    xx = xx + str(0)
                x = x + xx + " ELSE T_" + str(i) + " ENDIF)"
                if (i == Tsum - 1):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + str(x) + ", ")
            for i in range(bitnum + Tsum + 1):
                if (i == bitnum + Tsum):
                    fout.write(" );\n")
                else:
                    fout.write(" )")
            countQ = countQ + 1
        # print("T_" + str(countT) + " = Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1) )
        fout.write("ASSERT( T_" + str(countT) + " = Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1) + " );\n")
        countT += 1


def Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, depth, SS):
    """
        write Q T Y constraints
    :param fout:
    :param bitnum:
    :param Size:
    :param GateNum:
    :param QNum:
    :param bNum:
    :param depth:
    :param SS:
    """
    countA = 0
    countB = 0
    countQ = 0
    countT = 0
    countX = 0
    countY = 0
    lenght = bitnum
    # print(SS)
    # print(depth)
    for d in range(depth):
        # print(d,countT)
        Logic_SubConstraint(fout, bitnum, Size, SS[d], countQ, countT, d, lenght)
        countQ = countQ + 2 * SS[d]
        countT = countT + SS[d]
        lenght = lenght + SS[d]
        # print(lenght)
        # Y
    for y in range(bitnum):
        fout.write("ASSERT(  Y_" + str(y) + " = ")
        for i in range(bitnum):
            x = "( IF A_" + str(countQ) + "[" + str(bitnum + countT - 1 - i) + ":" + str(
                bitnum + countT - 1 - i) + "]=0bin0 THEN 0bin"
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
        for i in range(bitnum + countT):
            if (i == bitnum + countT - 1):
                fout.write(" );\n")
            else:
                fout.write(" )")
        countQ += 1


def Objective(fout):
    """
    add some end code
    :param fout:
    """
    fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def time_stamp1():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s%03d" % (data_head, data_secs)
    return time_stamp


def thread_func(threads, filestr):
    global result
    global resultstr
    order = "stp -p " + str(filestr) + ".cvc --cryptominisat --threads 18"  # > "+file+".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    # s=(os.popen(order))
    # os.system(order)
    s = (os.popen(order).read())
    resultstr = s
    end_time = time.time()
    # for t in threads:
    #    if
    # print(f"run result :{s}")
    result = 1
    # print(f'file : {filestr} , cost time : {(end_time - start_time) * 1000}ms')
    # print(filestr)
    if "Invalid." in s:
        # print(filestr,(end_time-start_time)*1000,'ms')
        fouts = open(filestr + ".txt", 'w')
        # resultstr=s
        fouts.write(s)
        fouts.write("time:" + str((end_time - start_time) * 1000) + 'ms')
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
    Cipherstr = "Xoodyak"  # ciphername
    Sbox = [0, 5, 3, 2, 6, 1, 4, 7]  # PROST# S-box
    MC = 3  # number of AND gates
    bitnum = 3  # number of S-box inputs
    for GateNum in range(MC, MC - 1, -1):
        Size = pow(2, bitnum)
        QNum = 2 * GateNum
        bNum = GateNum
        l = []
        for j in range(1, GateNum + 1):
            l.append(j)
        for depth in range(1, GateNum + 1):
            SStr = []
            # get a different combination on depth and gate
            combination_impl(l, GateNum, [], depth, SStr)
            SStr0 = []

            #  filter SStr front level number of out pin cloud over behind level number of input pin
            for dd in range(len(SStr)):
                SS = SStr[len(SStr) - dd - 1]
                ff = 1
                gs = 1  # next level need number of wires
                g0 = 0
                for sd in range(len(SS)):
                    if SS[len(SS) - sd - 1] > gs + g0:
                        ff = 0
                        break
                    g0 = g0 + gs - SS[len(SS) - sd - 1]
                    gs = 2 * SS[len(SS) - sd - 1]
                if (ff):
                    SStr0.append(SS)

            x = 1
            val = 1
            issolver = 0
            print(f"SStr {SStr} , SStr0 {SStr0}")
            for d in range(len(SStr0) if len(SStr0) < 1 else 1):
                result = 0
                SS = SStr0[d]
                sz = ""
                for dd in range(len(SS)):
                    sz = sz + str(SS[dd])
                print(f'SS {SS}')

                if not os.path.exists("./mc"):
                    os.system("mkdir ./mc")
                if not os.path.exists("./mc/" + Cipherstr):
                    os.system("mkdir ./mc/" + Cipherstr)
                filestr = "./mc/" + Cipherstr + "/" + Cipherstr + "newmc_D" + str(depth) + '_' + sz
                fout = open(filestr + "_0.cvc", 'w')

                State_Variate(fout, bitnum, Size, GateNum, QNum, bNum, SS)
                Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, Sbox)
                Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum, depth, SS)
                Objective(fout)

                fout.close()

                fout0 = open(filestr + "_1.cvc", 'w')
                fout1 = open(filestr + "_2.cvc", 'w')
                # fout2=open(filestr + ".txt", 'w')

                # let the same Q_i not be input of one gate
                b0str = ""
                b1str = ""
                for j in range(0, QNum, 2):
                    b0str = b0str + "ASSERT( BVGT(A_" + str(j) + ", A_" + str(j + 1) + "));\n"
                    b1str = b1str + "ASSERT( BVGT(A_" + str(j + 1) + ", A_" + str(j) + "));\n"
                lines0 = []
                lines = []
                f = open(filestr + "_0.cvc", 'r')
                s = ""
                s0 = ""
                for line in f:
                    lines.append(line)
                    lines0.append(line)
                lines0.insert(4 + 2 * bitnum + GateNum, b0str)
                lines.insert(4 + 2 * bitnum + GateNum, b1str)
                s = ''.join(lines)
                s0 = ''.join(lines0)
                f.close()
                # fout0=open(filestr + ".cvc", 'w')
                fout0.write(s0)
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
                    p = threading.Thread(target=thread_func, args=(threads, str(filestr) + '_' + str(j),))
                    threads.append(p)
                # print(threads)
                # p.start()
                resultstr = ""
                result = 0
                ishassolver = 0
                for t in threads:
                    t.start()
                x = 1
                # print(result)
                while (x):
                    # print(result)
                    xx = 0
                    # end_time = time.time()
                    # if end_time - start_time > 600:
                    #    xx = 1
                    if result == 1:  # len(cipher):
                        x = 0
                        for line in resultstr.splitlines():
                            s = line.split()
                            if "Invalid." in s:
                                # print(resultstr)

                                # MinGEC=MinGEC-1
                                ishassolver = 1
                                result = 1
                                break
                            if "Valid." in s:
                                # print(resultstr)

                                # MinGEC=MinGEC-1
                                ishassolver = 0
                                result = 0
                                resultstr = ""
                                break
                        # print(depth,resultstr)
                        order = "ps -ef|grep " + filestr
                        # os.system(order)
                        res = os.popen(order).read()
                        for line in res.splitlines():
                            s = line.split()
                            if filestr + "_0.cvc" in s or filestr + "_1.cvc" in s or filestr + "_2.cvc" in s:
                                # print(s[1])
                                r = os.popen("kill -9 " + s[1]).read()
                                # print("---------------------")
                                # os.system(order)

                        # print(os.system("rm -f " + filestr + "*.cvc"))
                        # print("rm -f " + filestr + "*.cvc")
                    if ishassolver:
                        print(f"depth : {depth} \n\n")
                        break
