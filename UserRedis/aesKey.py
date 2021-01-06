import base64


if __name__ == "__main__":
    test_str=  'hello'
    key_str = base64.b64encode(test_str.encode())
    print(key_str)
    a = base64.b64decode(key_str)
    print(a.decode())