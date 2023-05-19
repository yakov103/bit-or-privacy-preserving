from flask import Flask, request, jsonify
import requests
import time
import random
from sympy import is_quad_residue

app = Flask(__name__)

#tools
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
        r = random.randint(2, self.q - 1)
        if self.bit == 0:
            cA = (pow(self.g, r, self.p), pow(self.g, r * self.k, self.p))
        else:
            cA = (pow(self.g, r, self.p), (self.g * pow(self.g, r * self.k, self.p)) % self.p)
        return cA, self.q, self.g, pow(self.g, self.k, self.p)


    def secureResult(self, cB):
        return divide(cB[1], pow(cB[0], self.k, self.p), self.p)


    def fing_g(self):
        while True:
            candidate = random.randint(2, self.p - 2)
            if is_quad_residue(candidate, self.p):
                return candidate

@app.route('/start', methods=['POST'])
def start():
    private_data = request.get_json()
    # do some calculations
    q = 23
    Alice_instance = Alice(int(private_data['bA']), q )
    public_data = {}
    public_data['cA'], public_data['q'], public_data['g'], public_data['gk'] = Alice_instance.send()
    public_data['bB'] = 0
    # send to server B and wait for a response
    response = requests.post('http://localhost:5001/calculate', json=public_data)
    rst_from_bob = response.json()
    decrypted_result = Alice_instance.secureResult(rst_from_bob['bB'])
    if decrypted_result == 1:
        data = {'result': '0'}
    else:
        data = {'result': '1'}

    # send back to server B and third party
    requests.post('http://localhost:5001/end', json=data)
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(port=5000)
