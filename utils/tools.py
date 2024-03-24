def xoodyak_sbox_1(A):
    A2 = int(A[2])
    A1 = int(A[1])
    A0 = int(A[0])

    B2 = ~A1 & A2
    B1 = ~A2 & A0
    B0 = ~A0 & A1

    # output
    return f'{B0}{B1}{B2}'


def NOT(q_0):
    return not q_0


def MAOI1(q_0, q_1, q_2, q_3):
    return NOT(q_0 & q_1 | NOT(q_2 | q_3))


def MOAI1(q_0, q_1, q_2, q_3):
    return NOT(NOT(q_0 & q_1) & (q_2 | q_3))


def AND3(q_0, q_1, q_2):
    return q_0 & q_1 & q_2


def craft_verify():
    sbox = [12, 10, 13, 3, 14, 11, 15, 7, 8, 9, 1, 5, 0, 2, 4, 6]
    for i in range(16):
        X = f'{i:04b}'
        X_0 = int(X[0])
        X_1 = int(X[1])
        X_2 = int(X[2])
        X_3 = int(X[3])

        # depth 1
        T_0 = MAOI1(X_0, X_1, X_0, X_1)
        T_1 = AND3(X_3, X_2, X_3)
        T_2 = MAOI1(X_1, X_2, X_0, X_3)
        T_3 = MOAI1(X_1, X_0, X_2, X_2)
        # depth 2
        T_4 = MOAI1(X_3, T_0, T_3, T_3)
        T_5 = MOAI1(T_3, T_0, X_0, T_1)
        T_6 = MAOI1(X_0, T_0, X_3, T_0)
        T_7 = MOAI1(X_0, T_1, T_2, T_2)

        Y_0 = T_5
        Y_1 = T_7
        Y_2 = T_6
        Y_3 = T_4

        Y = int(str(int(Y_0)) + str(int(Y_1)) + str(int(Y_2)) + str(int(Y_3)), 2)

        if sbox[i] != Y:
            print(f'sbox verify fail')


if __name__ == '__main__':
    craft_verify()
