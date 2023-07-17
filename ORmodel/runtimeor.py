import random
import time
if __name__ == '__main__':
    for xixi in range(10):
        print("----start_time---",time.time())
        A = [0 for i in range(48)]
        for i in range(48):
            x = random.getrandbits(16)
            while x in A:
                x = random.getrandbits(16)
            A[i] = x
        start_time = time.time()
        for ii in range(4):
            q=A[ii]
            x=0
            #for i in range(10000):
            for i in range(1000):
                x=(q==A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3] )
        end_time = time.time()
        print((end_time - start_time)/4)
        start_time = time.time()
        for ii in range(8):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3])| (q == A[4]) | (q == A[5]) |\
                    (q == A[6]) | (q == A[7])
        end_time = time.time()
        print((end_time - start_time)/8)
        start_time = time.time()
        for ii in range(12):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7]) | (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11])
        end_time = time.time()
        print((end_time - start_time)/12)
        start_time = time.time()
        for ii in range(16):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7])| (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11])| \
                    (q == A[11])|(q == A[11]) | (q == A[12]) | (q == A[13]) | (q == A[14]) | (q == A[15])
        end_time = time.time()
        print((end_time - start_time)/16)
        start_time = time.time()
        for ii in range(20):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7]) | (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11]) | \
                    (q == A[11]) | (q == A[11]) | (q == A[12]) | (q == A[13]) | (q == A[14]) | (q == A[15])| \
                    (q == A[16]) | (q == A[17]) | (q == A[18]) | (q == A[19])
        end_time = time.time()
        print((end_time - start_time)/20)
        start_time = time.time()
        for ii in range(24):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7]) | (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11]) | \
                    (q == A[11]) | (q == A[11]) | (q == A[12]) | (q == A[13]) | (q == A[14]) | (q == A[15]) | \
                    (q == A[16]) | (q == A[17]) | (q == A[18]) | (q == A[19])|(q == A[20]) | (q == A[21]) | (q == A[22]) | (q == A[23])
        end_time = time.time()
        print((end_time - start_time)/24)

        for ii in range(32):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7]) | (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11]) | \
                    (q == A[11]) | (q == A[11]) | (q == A[12]) | (q == A[13]) | (q == A[14]) | (q == A[15]) | \
                    (q == A[16]) | (q == A[17]) | (q == A[18]) | (q == A[19])|(q == A[20]) | (q == A[21]) | \
                    (q == A[22]) | (q == A[23])|(q == A[24]) | (q == A[25]) | (q == A[26]) | (q == A[27]) | \
                    (q == A[28]) | (q == A[29]) | (q == A[30]) | (q == A[31])
        end_time = time.time()
        print((end_time - start_time)/32)

        start_time = time.time()
        for ii in range(40):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7]) | (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11]) | \
                    (q == A[11]) | (q == A[11]) | (q == A[12]) | (q == A[13]) | (q == A[14]) | (q == A[15]) | \
                    (q == A[16]) | (q == A[17]) | (q == A[18]) | (q == A[19])|(q == A[20]) | (q == A[21]) | \
                    (q == A[22]) | (q == A[23])|(q == A[24]) | (q == A[25]) | (q == A[26]) | (q == A[27]) | (q == A[28]) | \
    (q == A[29]) | (q == A[30]) | (q == A[31]) | (q == A[32]) | (q == A[33]) | \
    (q == A[34]) | (q == A[35]) | (q == A[36]) | (q == A[37]) | (q == A[38]) | \
    (q == A[39])
        end_time = time.time()
        print((end_time - start_time)/40)

        start_time = time.time()
        for ii in range(48):
            q = A[ii]
            x = 0
            #for i in range(10000):
            for i in range(1000):
                x = (q == A[0]) | (q == A[1]) | (q == A[2]) | (q == A[3]) | (q == A[4]) | (q == A[5]) | \
                    (q == A[6]) | (q == A[7]) | (q == A[8]) | (q == A[9]) | (q == A[10]) | (q == A[11]) | \
                    (q == A[11]) | (q == A[11]) | (q == A[12]) | (q == A[13]) | (q == A[14]) | (q == A[15]) | \
                    (q == A[16]) | (q == A[17]) | (q == A[18]) | (q == A[19])|(q == A[20]) | (q == A[21]) | \
                    (q == A[22]) | (q == A[23])|(q == A[24]) | (q == A[25]) | (q == A[26]) | (q == A[27]) | (q == A[28]) | \
    (q == A[29]) | (q == A[30]) | (q == A[31]) | (q == A[32]) | (q == A[33]) | \
    (q == A[34]) | (q == A[35]) | (q == A[36]) | (q == A[37]) | (q == A[38]) | \
    (q == A[39]) | (q == A[40]) | (q == A[41]) | (q == A[42]) | (q == A[43]) | \
    (q == A[44]) | (q == A[45]) | (q == A[46]) | (q == A[47])
        end_time = time.time()
        print((end_time - start_time)/48)
