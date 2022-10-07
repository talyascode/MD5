import hashlib

result = hashlib.md5(b'9')
# printing the equivalent byte value.
print("The byte equivalent of hash is : ", end="")
print(result.digest())
result = result.digest()

digit = 0
for i in range(1000000000, 10000000000):
    digit = f'{i:03}'
    num = hashlib.md5(digit.encode())
    print(digit)
    # printing the equivalent byte value.
    print("The byte equivalent of hash is : ", end="")
    print(num.digest())
    print(num.digest() == result)
    if num.digest() == result:
        print('found the string:')
        print(digit)
        break
