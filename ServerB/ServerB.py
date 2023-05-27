import asyncio
from flask import Flask, request, jsonify
import requests
import time
import random
from sympy import is_quad_residue, isprime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

bob_ready = False
public_data_from_Alice_received = False

@app.route('/health', methods=['GET'])
def health():
    i = 0
    while not bob_ready:
        time.sleep(0.1)
        i += 1
        if i % 20 == 0:
            print("Bob is waiting for Alice")
            print(f"bob_ready={bob_ready}")
    return jsonify({'status': 'ok'}), 200
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
# def isprime(n):
#     if n <= 1:
#         return False
#     elif n <= 3:
#         return True
#     else:
#         for i in range(2, int(n**0.5) + 1):
#             if n % i == 0:
#                 return False
#     return True



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

@app.route('/BobBit', methods=['POST'])
@cross_origin()
def BobBit():
    global bob_instance
    global bob_ready
    global public_data_from_Alice_received
    global data
    bob_ready = False
    public_data_from_Alice_received = False
    private_data = request.get_json()
    if private_data is None:
        return jsonify({'error': 'No data provided'}), 400
    if 'bB' not in private_data:
        return jsonify({'error': 'No bit provided'}), 400
    if int(private_data['bB']) not in [0, 1]:
        return jsonify({'error': 'Invalid bit provided'}), 400
    bob_instance = Bob(int(private_data['bB']))
    bob_ready = True
    # wait for Alice to health check localhost:5001/health
    # send health check to Alice without the private data
    print("Bob is ready")
    alice_health = requests.get("http://localhost:5000/health")
    print(alice_health.status_code)
    # wait for Alice to send public data
    i = 0
    while not public_data_from_Alice_received:
        i += 1
        time.sleep(0.1)
        if i % 20 == 0:
            print("Bob is waiting for Alice")
            print(f"public_data_from_Alice_received={public_data_from_Alice_received}")
    # return data
    return jsonify(data), 200





@app.route('/calculate', methods=['POST'])
def calculate():
    public_data_from_Alice = request.get_json()
    print(public_data_from_Alice)
    rst_data = {}
    print(bob_instance.bit)
    rst_data['cB'] = bob_instance.send(public_data_from_Alice['cA'], public_data_from_Alice['q'], public_data_from_Alice['g'], public_data_from_Alice['gk'])
    print(rst_data)
    # do some calculations
    return jsonify(rst_data), 200

@app.route('/end', methods=['POST'])
def end():
    global public_data_from_Alice_received
    global data
    data = request.get_json()
    # get final result from server A
    public_data_from_Alice_received = True
    print(f"Final result is: {data['result']}")
    return jsonify(data), 200

if __name__ == "__main__":
    bob_ready = False
    app.run(port=5001, debug=True)
