from GM import GroupManager
from user import User
from verifier import Verifier
from sysParam import SystemParam

groupManager = GroupManager()
print("We start...........")
#Set up
systemParameter = groupManager.genSysParam() #GM tạo tham số hệ thống
sParam = SystemParam(systemParameter) #Khởi tạo lớp tham số hệ thống dùng chung

(n, a, a0, y, g, h) = groupManager.setup(512)
print("n: ", n)
#Join
print("Join start.....")
user1 = User()
C1_is_in_cyclic_group = False
while ( not C1_is_in_cyclic_group):
    #Joint 1: generate secret exponent and calculate C1
    print("User create C1")
    C1, r_ex = user1.gen_random_element(n, g, h, sParam.lambda_2)
    #Join2: user check C1 and gen random alpha & beta values
    print("GM check C1 and create alpha, beta")
    alpha, beta = groupManager.join2(C1, n, sParam.lambda_2)
    if (alpha and beta): C1_is_in_cyclic_group = True

C2_is_in_cyclic_group = False
e = A = 0
while ( not C2_is_in_cyclic_group):
    #Join3: User calculate C2
    print("User create C2")
    C2 = user1.join3(a, n, alpha, beta, sParam.lambda_1, sParam.lambda_2)
    #Join4: GM check C2 is in QR(n) --> create user certificate [Ai, ei]
    print("GM check C2 and create member certificate")
    e, A = groupManager.join4(C2, n, a0, sParam.gamma_1, sParam.gamma_2)
    if (e and A): C2_is_in_cyclic_group = True

print("Join OK: ",user1.join5(n, a, a0, A, e))


#================Sign================================
user1Message = "hallo man" 
#signature format (c, s1, s2, s3, s4, T1, T2, T3)
user1Signature = user1.sign(user1Message, a, a0, g, h, y, sParam.l_p, n, sParam.lambda_1, sParam.lambda_2, sParam.gamma_1, sParam.gamma_2, sParam.epsilon, sParam.k)
print("Sign successful")
print("Signature: ", user1Signature[0])
#==========Verify signature==================

verifier1 = Verifier()
if (verifier1.verify(user1Signature[0], user1Signature[1], user1Signature[2], user1Signature[3], user1Signature[4], user1Signature[5], user1Signature[6], user1Signature[7], user1Message, a, a0, g, h, y, n, sParam.lambda_1, sParam.gamma_1) == 1): print("Yeah, verification successful")
else: print("OOPS, Verification Failed")
