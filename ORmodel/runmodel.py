import random
import time
import os
if __name__ == '__main__':
    for iter in range(100):
        l=[16,32]           
        order="rm -f ./OR/*.cvc"
        os.popen(order).read() 
        order="rm -f ./QA/*.cvc"
        os.popen(order).read() 
        order="rm -f ./QAbit/*.cvc"
        os.popen(order).read() 
        order="python ./genratemodel.py"
        os.popen(order).read()

        filestr = "./res.txt"
        fout = open(filestr, 'w')

        print("QAbit")
        fout.write("QAbit\n")
        for kk in range(len(l)):
            k=l[kk]
            for i in range(4,32,4):
                sum=0
            
                start_time = time.time()
                for f in range(0,100):
                    s=""
                    for i0 in range(10):
                        order="stp ./QAbit/QAbit_"+str(i)+"_"+str(k)+"_"+str(f)+".cvc" # --cryptominisat --threads 1"
                        #print(order,i0,start_time)
                        s=(os.popen(order))
                        #os.system(order)
                end_time = time.time()
                #print(s.read())    
                result=1
                #print("QAbit",(end_time - start_time), 'ms')
                print((end_time - start_time))
                fout.write(str(end_time - start_time)+"\n")
        
        print("QA")
        fout.write("QA\n")
        for kk in range(len(l)):
            k=l[kk]
            for i in range(4,32,4):
                sum=0    
                
                start_time = time.time()
                #print(i,k)
                s=""
                for f in range(0,100):
                    for i0 in range(10):
                        order="stp ./QA/QA_"+str(i)+"_"+str(k)+"_"+str(f)+".cvc" #--cryptominisat --threads 1"
                        #print(order,f,start_time)
                        s=(os.popen(order))
                        #print(s.read())
                end_time = time.time()
                #print(s.read())
                result=1
                #print("QA",(end_time - start_time), 'ms')
                print((end_time - start_time))
                fout.write(str(end_time - start_time)+"\n")
        print("OR")
        fout.write("OR\n")
        for kk in range(len(l)):
            k=l[kk]
            for i in range(4,32,4):
                sum=0
                         
                start_time = time.time()
                for f in range(0,100):
                    s=""
                    for i0 in range(10):
                        order="stp ./OR/OR_"+str(i)+"_"+str(k)+"_"+str(f)+".cvc" # --cryptominisat --threads 1"
                        #print(order,i0,start_time)
                        s=(os.popen(order))
                        #os.system(order)
                end_time = time.time()
                #print(s.read)()
                result=1
                #print("OR",(end_time - start_time), 'ms')
                print((end_time - start_time))
                fout.write(str(end_time - start_time)+"\n")
        fout.close()
   
            
