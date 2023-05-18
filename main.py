import random

def xgcd(a, b):
    """Euclid's extended algorithm:
    Given a, b, find gcd, x, y that solve the equation:
    ax + by = gcd(a, b)
    """
    x, y = 0, 1
    u, v = 1, 0
    gcd = b
    while a != 0:
        q, r = divmod(gcd, a)
        m, n = x - u * q, y - v * q
        gcd, a, x, y, u, v = a, r, u, v, m, n
    return gcd, x, y

def divide(A, B, m):
    """Modular division:
    Returns integer z such that: z * B mod m == A.
    If there is more than one (i.e. when gcd(B, m) > 1) - returns the smallest such integer.
    """
    assert 0 <= A < m, 'Invalid A value'
    assert 0 <= B < m, 'Invalid B value'

    gcd, x, y = xgcd(B, m)
    if A % gcd == 0:
        q = A // gcd
        return ((x + m) * q) % (m // gcd)
    else:
        raise ValueError('no quotient')


def multiply_modulo_big(num1, num2, m):
    num1 %= m
    result = 0
    while num2 > 0:
        if num2 % 2 == 1:
            result = (result + num1) % m
        num1 = (num1 * 2) % m
        num2 //= 2
    return result


#is_prime function
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    else:
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
    return True


class Participant:
    def __init__(self, bit):
        self.bit = bit


class Alice(Participant):
    def __init__(self, bit, q):
        super().__init__(bit)
        self.q = q
        self.k = random.randint(0, q - 1)
        self.p = 2 * self.q + 1
        self.g = self.fing_g()

        #print(f"k={self.k} g={self.g}")

    def send(self):
        r = random.randint(0, self.q - 1)
        if self.bit == 0:
            cA = (pow(self.g, r, self.p), pow(self.g, r * self.k, self.p))
        else:
            cA = (pow(self.g, r, self.p), (self.g * pow(self.g, r * self.k, self.p)) % self.p)
        return cA, self.q, self.g, pow(self.g, self.k, self.p)


    def secureResult(self, cB):
        return divide(cB[1], pow(cB[0], self.k, self.p), self.p)


    def fing_g(self):
        x = random.randint(2, self.p)
        p = pow(x,2,self.p)
        while not is_prime(x):
            x = random.randint(2, self.p)
            p = pow(x, 2, self.p)
        #print(f"x={x}")
        return x


class Bob(Participant):
    def __init__(self, bit):
        super().__init__(bit)

    def send(self, cA, q, g, gk):
        r_ = random.randint(0, q - 1)
        p = 2 * q + 1
        if self.bit == 0:
            cB = (pow(cA[0], r_, p), pow(cA[1], r_, p))
        else:
            cB = (pow(cA[0], r_, p), multiply_modulo_big(pow(g, r_, p) , pow(cA[1], r_, p), p))
        return cB


def run_protocol(bA, bB, q):
    Alice_instance = Alice(bA, q)
    Bob_instance = Bob(bB)
    cA, q, g, gk , = Alice_instance.send()
    #print(f"from Alice : cA= {cA} q = {q}, g = {g}, gk = {gk}")
    cB = Bob_instance.send(cA, q, g, gk)
    #print(f"from Bob : cB= {cB}")
    decrypted = Alice_instance.secureResult(cB)
    #print(f"decrypted = {decrypted}")
    if decrypted == 1:
        return 0
    else:
        return 1


# Testing
bA = 0
bB = 1
q = 23



for i in range(100):
    print(run_protocol(bA, bB, q))  # Outputs: 1
