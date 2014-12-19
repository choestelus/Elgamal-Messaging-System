def testgen(total_num):
    return len(total_num) == len(set(total_num))
 
def test_z(generator_num, n):
    bag = []
    for i in range(1, n):
        t = pow(generator_num, i, n)
        bag.append(t)
        return testgen(bag)
 
def generator(num):
    generator_list = []
    for i in range(1,num - 1):
        if test_z(i, num) == True:
            generator_list.append(i)
        print i, test_z(i, num)
    return generator_list
 
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
