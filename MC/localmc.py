import os
import time
import threading
from datetime import datetime
import inspect
import ctypes
import subprocess
from itertools import combinations

A = [[0 for i in range(256)] for j in range(8)]
resstr = ""

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
    for i in range((QNum + bitnum)):
        fout.write("A_" + str(i))
        if (i == QNum + bitnum - 1):
            fout.write(" : BITVECTOR( " + str((bitnum + GateNum)+len(TTstr)+1)+ " );\n")
        elif ((i + 1) % 2 == 0 and i < QNum):
            fout.write(" : BITVECTOR( " + str((bitnum+len(TTstr) + i // 2 + 1))+ " );\n")
        else:
            fout.write(" , ")

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


def Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,Sbox,yN,Yelem):
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
    for i in range(0, QNum, 2):
        fout.write("ASSERT( BVGE(A_" + str(i) + ", A_" + str(i + 1) + "));\n")

def Logic_SubConstraint(fout, bitnum, Size, GateNum, Qsum, Tsum,depth,lenght):
    countQ=Qsum
    countT=Tsum
    for k in range(GateNum):
        # Q
        for q in range(2):
            fout.write("ASSERT(  Q_" + str(countQ) + " = ")
            for i in range(bitnum+1):
                x = "( IF A_" + str(countQ) + "[" + str(lenght - i) + ":" + str(lenght - i) + "]=0bin1 THEN "
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
                if (depth==0  and i == bitnum):
                    fout.write(x)
                else:
                    fout.write("BVXOR( " + str(x) + ", ")
            for i in range(Tsum):
                x = "( IF A_" + str(countQ) + "[" + str(lenght-bitnum- 1 - i) + ":" + str(
                        lenght-bitnum - 1 - i) + "]=0bin0 THEN  0bin"
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
                    fout.write( " );\n")
                else:
                    fout.write(" )")
            countQ =countQ+1
        #print("T_" + str(countT) + " = Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1) )
        fout.write("ASSERT( T_" + str(countT) + " = Q_" + str(countQ - 2) + " & Q_" + str(countQ - 1) + " );\n")
        countT += 1

def Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,depth,SS):
    countA = 0
    countB = 0
    countQ = 0
    countT = 0
    countX = 0
    countY = 0
    lenght = bitnum
    #print(SS)
    #print(depth)
    for d in range(depth):
        #print(d,countT)
        Logic_SubConstraint(fout, bitnum, Size, SS[d], countQ, countT, d,lenght)
        countQ=countQ+2*SS[d]
        countT = countT + SS[d]
        lenght = lenght+ SS[d]
        #print(lenght)
        # Y
    for y in range(1):
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

def thread_func(t,filestr,i):
    global result
    order = "stp -p " + str(filestr) + ".cvc --cryptominisat --threads 18 "#> " + filestr + ".txt "
    # print(order)
    start_time = time.time()
    # print(i,start_time)
    s=(os.popen(order).read())
    #os.system(order)
    print(s)
    end_time = time.time()
    # for t in threads:
    #    if
    # print(file,(end_time-start_time)*1000,'ms')

   
    print(filestr,(end_time-start_time)*1000,'ms')
    if "Invalid." in s:
        result =i
        fouts=open(filestr+"Yes.txt",'a+')
        fouts.write(str(s))
        fouts.write(str((end_time - start_time)*1000))
        fouts.close()
    elif "Valid." in s:
        result =i
        fouts=open(filestr+"No.txt",'a+')
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
    yN = 1  # part of S-box outputs
    yystr = []  # the part of S-box output with solution if Y_2,Y_3 has solution, yystr=[2,3]

    TTstr = []  # the solution of part S-box output, its value is [T_0,T_1...]

    constr = []  # Exclude existing solutions realized by S-box NOT(T_0=0xf22f)
    Cipherstr = "Present"  # ciphername
    Sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]  # PROST# S-box
    MC = 8  # number of AND gates
    bitnum = 4  # number of S-box inputs
    for GateNum in range(MC, 1, -1):
        Size = pow(2, bitnum)
        QNum = 2 * GateNum
        items=[]
        aNum = 4 * (2 * bitnum + GateNum - 1) * GateNum / 2 + bitnum * bitnum + GateNum * bitnum
        bNum = GateNum
        yy=[]
        for y in range(bitnum):
            if y not in yystr:
                items.append(y)
        for c in combinations(items, yN):
            yy.append(c)
        print(yy)
        l=[]
    for j in range(1, GateNum + 1):
        l.append(j)
    for depth in range(1, GateNum+1):
        SStr = []
        combination_impl(l, GateNum, [], depth, SStr)
        SStr0=[]
        for dd in range(len(SStr)):
            SS = SStr[len(SStr) - dd - 1]
            ff=1
            gs=1
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
        #print(SStr0)
        result =0
        for y0 in range(len(yy)):
            for d in range(len(SStr0)):
                strz=""
                for yy0 in range(len(yy[y0])):
                    strz=strz+str(yy[y0][yy0])
                if not os.path.exists("./localmc"):
                    os.system("mkdir ./localmc")
                if not os.path.exists("./localmc/"+Cipherstr):
                    os.system("mkdir ./localmc/"+Cipherstr)
                if not os.path.exists("./localmc/"+Cipherstr+"/11"):
                    os.system("mkdir ./localmc/"+Cipherstr+"/11")
                filestr = "./localmc/"+Cipherstr+"/11/"+Cipherstr+"LocalMC"+str(GateNum)+strz
                fout=open(filestr + ".cvc", 'w')
                SS=SStr0[d]
                print(SS)
                State_Variate(fout, bitnum, Size, GateNum, QNum, bNum,yN,TTstr)
                Trival_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,Sbox,yN,yy[y0])
                Logic_Constraint(fout, bitnum, Size, GateNum, QNum, bNum,depth,SS)
                Objective(fout)
                fout.close()
                #threads = []
                #thread_func(filestr,filestr)
                #p = threading.Thread(target=thread_func, args=(threads,str(filestr),yy[y0][0]+1,))
                    #threads.append(p)
                # print(threads)
                #p.start()
                x = 1
                tttstr=[]
                # print(result)
                while (x):
                    # print(result)
                    order = "stp -p " + str(filestr) + ".cvc --cryptominisat --threads 1 "#> " + filestr + ".txt "
                    # print(order)
                    start_time = time.time()
                    # print(i,start_time)
                    s=(os.popen(order).read())
                    #os.system(order)
                    print(s)
                    end_time = time.time()
                    # for t in threads:
                    #    if
                    # print(file,(end_time-start_time)*1000,'ms')
                    print(filestr,(end_time-start_time)*1000,'ms')
                    if "Invalid." in s:
                        fouts=open(filestr+"Yes.txt",'a+')
                        fouts.write(str(s))
                        fouts.write(str((end_time - start_time)*1000))
                        fouts.close()
                        issolver=1
                        Astr = []
                        AAstr = []
                        Ystr = ""
                        for line in s.splitlines():
                            s0 = line.split()
                            if "Y_" in s0[1]:
                                Ystr = int(s0[3], 16)
                                break
                        ttstr = []
                        for line in s.splitlines():
                                s0 = line.split()
                                isture = 0
                                #print(s0)
                                if len(s0) > 2 and "T_" in s0[1] and int(s0[3], 16) != Ystr:
                                    Astr.append("".join(s0))
                                    ttstr.append(int(s0[3], 16))
                                if len(s0) > 2 and "T_" in s0[1]:
                                    AAstr.append("".join(s0))
                        fstr = "./localmc/"+Cipherstr+"/11/" + Cipherstr+str(GateNum)+strz
                        foutc = open(fstr + ".txt", 'a+')
                        foutc.write(s)
                        foutc.close()
                            # else:
                            #    AAstr.append(s)
                            # print(AAstr)
                        #print(Astr)
                        #print(ttstr,tttstr)
                        if len(Astr) > 0:
                            ttstr.sort()
                            if ttstr not in tttstr:
                                filestr1 = "./localmc/"+Cipherstr+"/11/" + str(GateNum)+strz
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

                        print(os.system("rm -f "+filestr+".cvc"))
                        x=0
