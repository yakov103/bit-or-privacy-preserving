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

class Bob(Participant):
    def __init__(self, bit):
        super().__init__(bit)

    def send(self, cA, q, g, gk):
        r_ = random.randint(2, q - 1)
        p = 2 * q + 1
        if self.bit == 0:
            cB = (pow(cA[0], r_, p), pow(cA[1], r_, p))
        else:
            cB = (pow(cA[0], r_, p), multiply_modulo_big(pow(g, r_, p) , pow(cA[1], r_, p), p))
        return cB

@app.route('/calculate', methods=['POST'])
def calculate():
    public_data_from_Alice = request.get_json()
    Bob_Instace = Bob(public_data_from_Alice['bB'])
    rst_data = {}
    rst_data['bB'] = Bob_Instace.send(public_data_from_Alice['cA'], public_data_from_Alice['q'], public_data_from_Alice['g'], public_data_from_Alice['gk'])


    # do some calculations

    return jsonify(rst_data), 200

@app.route('/end', methods=['POST'])
def end():
    data = request.get_json()
    # get final result from server A
    print(f"Final result is: {data['result']}")
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(port=5001)
