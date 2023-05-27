import unittest
import requests


class TestAliceClient(unittest.TestCase):

    async def test_sync(self):
        #  loop 1000 times
        i = 0
        while i < 10:
            b = 1
            b_json = {'bB': b}
            b_rst = await requests.post('http://localhost:5001/BobBit', json=b_json)
            print(b_rst)
            b_rst = b_rst.json()
            print(b_rst)
            print(f"i={i}")
            i += 1
            self.assertEqual(int(b_rst['result']), b)

if __name__ == '__main__':
    unittest.main()








