import random
import time
import os
if __name__ == '__main__':
 
    AA = [[0 for i in range(48)] for j in range(2)]
    Size = 32
    l=[16,32]  

    for kk in range(len(l)):
        k=l[kk]
        Size = k
        for i in range(4,52,4):
            for f in range(0,100):
                qbitnum = 1
                if (f%i==0):
                    for ii in range(len(l)):
                        for i0 in range(48):
                            x=random.getrandbits(l[ii])
                            while x in AA[ii]:
                                x = random.getrandbits(l[ii])
                            AA[ii][i0]= x
                A=AA[kk]           
                bitnum = i    
                countAA = bitnum
                #bit-sliced model begin
                filestr = "./QA/QA_" + str(i) + "_" + str(Size) + "_" + str(f) + ".cvc"
                fout = open(filestr, 'w')
                for i0 in range(0,bitnum):
                    fout.write("X_" +str(i0))
                    if (i0 == bitnum - 1):
                        fout.write(" : BITVECTOR( "+str(Size )+" );\n")
                    else:
                        fout.write(", ")
                #y
                for i0 in range(0,1):
                    fout.write("Q: BITVECTOR( "+str(Size )+" );\n")
                for i0 in range(0, 1):
                    fout.write("Y : BITVECTOR( " + str(Size) + " );\n")
                #A
                for i0 in range(0,bitnum):
                    fout.write("A_" +str(i0))
                    if (i0 == bitnum - 1):
                        fout.write(" : BITVECTOR( "+str(Size )+" );\n")
                    else:
                        fout.write(", ")
                for i0 in range(0, bitnum):
                    fout.write("ASSERT( X_" + str(i0)+" = 0bin")
                    x = A[i0]
                    for j0 in range(0, Size):
                        fout.write(str(x>>(Size-1-j0)&0x1))
                    fout.write(");\n")
                #Y
                
                fout.write("ASSERT( Y = 0bin")
                x = A[f%(bitnum)]
                for j0 in range(0, Size):
                    fout.write(str(x >> (Size - 1 - j0) &0x1))
                fout.write(");\n")
                
                for i0 in range(0, bitnum):
                    fout.write("ASSERT( A_" +str(i0)+" = 0bin")
                    for j0 in range(0, Size):
                        fout.write(str(1))
                    fout.write(" OR A_" +str(i0)+" = 0bin")
                    for j0 in range(0, Size):
                        fout.write(str(0))
                    fout.write(");\n")
                xx0 = "0bin"
                xx1 = "0bin"
                for j0 in range(0, Size):
                    xx0 = xx0 + str(0)
                    xx1 = xx1 + str(1)
                #Q_a
                for i0 in range(0,bitnum):
                    for i1 in range(i0+1,bitnum):
                        fout.write("ASSERT( A_" +str(i0)+ " & A_" +str(i1)+ " = " + xx0 + " );\n")
                fout.write("ASSERT(  Q = ")
                countA=0
                for i0 in range(0,bitnum):
                    x = "A_" + str(countA)
                    x = x + " & X_" + str(i0)
                    if (i0 == bitnum-1):
                        fout.write(x)
                    else:
                        fout.write("BVXOR( " + x + ", ")
                    countA=countA+1
                for i0 in range(0,bitnum):
                    if (i0 == bitnum-1):
                        fout.write(");\n")
                    else:
                        fout.write(" )")
                #Q
                fout.write("ASSERT(  Y = Q );\n")
                fout.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")
            #bit-sliced model end
            #or-encoding model begin
            #for f in range(0,bitnum):
                filestr = "./OR/OR_" + str(i) + "_" + str(Size) + "_" + str(f) + ".cvc"

                fout0 = open(filestr, 'w')
                for i0 in range(0,bitnum):
                    fout0.write("X_" +str(i0))
                    if (i0 == bitnum - 1):
                        fout0.write(" : BITVECTOR( "+str(Size )+" );\n")
                    else:
                        fout0.write(", ")
                #y
                for i0 in range(0,1):
                    fout0.write("Q: BITVECTOR( "+str(Size )+" );\n")
                for i0 in range(0, 1):
                    fout0.write("Y : BITVECTOR( " + str(Size) + " );\n")

                for i0 in range(0, bitnum):
                    fout0.write("ASSERT( X_" + str(i0)+" = 0bin")
                    x = A[i0]
                    for j0 in range(0, Size):
                        fout0.write(str(x>>(Size-1-j0)&0x1))
                    fout0.write(");\n")
                #Y
                
                fout0.write("ASSERT( Y = 0bin")
                x = A[f%(bitnum)]
                for j0 in range(0, Size):
                    fout0.write(str(x >> (Size - 1 - j0)&0x1))
                fout0.write(");\n")
                
                
                fout0.write("ASSERT(  ")
                countA=0
                for i0 in range(0,bitnum):
                    x = "(Q =  X_" + str(i0)+")"
                    if (i0 == bitnum-1):
                        fout0.write(x+");\n")
                    else:
                        fout0.write(x+" OR ")

                fout0.write("ASSERT(  Y = Q );\n")
                fout0.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")
            #or-encoding model end

            #bit model begin
                filestr = "./QAbit/QAbit_" + str(i) + "_" + str(Size) + "_" + str(f) + ".cvc"

                fout1 = open(filestr, 'w')
                for i0 in range(0, bitnum):
                    for j0 in range(0,Size):
                        fout1.write("x_" + str(i0)+"_" + str(j0))
                        if (i0 == bitnum - 1&j0==Size-1):
                            fout1.write(" : BITVECTOR(1);\n")
                        else:
                            fout1.write(", ")
                for j0 in range(0, Size):
                    fout1.write("y_" + str(j0))
                    if (j0 == Size - 1):
                        fout1.write(" : BITVECTOR(1);\n")
                    else:
                        fout1.write(", ")
                for j0 in range(0, Size):
                    fout1.write("q_" + str(j0))
                    if (j0 == Size - 1):
                        fout1.write(" : BITVECTOR(1);\n")
                    else:
                        fout1.write(", ")
                #a
                for i0 in range(0, bitnum):
                    fout1.write("a_" +str(i0))
                    if (i0 == bitnum - 1):
                        fout1.write(" : BITVECTOR(1);\n")
                    else:
                        fout1.write(", ")
                for i0 in range(0, bitnum):
                    for j0 in range(0,Size):
                        fout1.write("ASSERT(x_" + str(i0)+"_" + str(j0)+"=0bin")
                        fout1.write(str((A[i0]>>(Size-1-j0)&0x1))+");\n")
                
                
                for j0 in range(0, Size):
                    fout1.write("ASSERT(y_" + str(j0)+" = 0bin")
                    fout1.write(str((A[f%(bitnum)] >> (Size - 1 - j0) &0x1)) + ");\n")
                
                #for i0 in range(0, bitnum):
                #    fout1.write("ASSERT(a_" +str(i0)+" = 0bin1 OR a_"+str(i0)+" = 0bin0);\n")
                for i0 in range(0, bitnum):
                    for i1 in range(i0 + 1, bitnum):
                        fout1.write("ASSERT( a_" + str(i0) + " & a_" + str(i1) + " = 0bin0 );\n")
                for j0 in range(0, Size):
                    countA = 0
                    fout1.write( "ASSERT(q_" +str( j0 )+ " = ")
                    for i0 in range(0, bitnum):
                        x = "a_" + str(countA)+ " & x_" + str(i0) + "_" + str(j0)
                        if (i0 == bitnum-1):
                            fout1.write(x)
                        else:
                            fout1.write("BVXOR( " +x +", ")
                        countA=countA+1
                    for i1 in range(0, bitnum):
                        if (i1 == bitnum-1):
                            fout1.write(" );\n")
                        else:
                            fout1.write(" )")
                for j0 in range(0, Size):
                    fout1.write("ASSERT(  y_"+str(j0)+ " = q_" +str(j0)+ " ); \n" )
                fout1.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")


