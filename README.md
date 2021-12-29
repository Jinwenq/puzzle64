# Bitcoin Puzzle 64 Random

Private keys are generated randomly in keyspace 8000000000000000:ffffffffffffffff the private keys are converted into their respective public keys to address and checks their balance in real-time.

# Donation

I really apreciate any small donation. 
BTC: 1DZR3pdrJkBcF3D6hMmFYcrVJ4oHrqepG2

LTC: LdspvbLuKeRCiD3MxheFm4hFfAq8RxqhrJ

XMR: 46ig2xy6NHLSs1dcXiGUnjFhHf9UYVEywAhvU9U6jEgLXRW3ADjoQLZAZnqdr22PGq3A5Q4UzAV6i54JQJTyCscYPn5Dmh8

ETH: 0x481f70Fd18a7a4C5642680B7441FCF36a4A28eAD

# Dependencies

<a href="https://www.python.org/downloads/">Python 3.6</a> or higher

btc-hack.py will try to automatically install the required modules if they are not present. Should that fail, you can find the required modules listed in the <a href="/requirements.txt">requirements.txt<a/>
  
Minimum <a href="#memory-consumption">RAM requirements</a>

# Installation

```
$ git clone https://github.com/Xh0st/puzzle64
```

# Quick Start
  
  

```
import base58
import ecdsa
import requests
import sys
import json
```
```
$ python3 puzzle64.py
```
# Expected Output

Every time this program checks the balance of a generated address, it will print the result to the user. If an empty wallet is found, then the wallet address will be printed to the terminal. An example is:

>1HBL9rXLrF1BoPwmLZHxuYV1wx4g6K32N6 : 0.0

However, if a wallet with a balance is found, then all necessary information about the wallet will be saved to the text file `found.txt`. An example is:

>address: 1B1Enw49ovsH3bReGbBnAfkfaGhaRJj3ku<br/>
>private key: 00000000000000000000000000000000000000000000000090e15e21125e3806<br/>
>WIF private key: 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip7WoQYQFx7wjw8RaHL<br/>
>public key: 037D5B40E63C41A0B70D499A41C8F256569BD4BF169B5E02D668BB0498C7178CEA<br/>
>balance: 0.64<br/>

# Memory Consumption

This program uses approximately 2GB of RAM per CPU. Because this program can use multi-processing, some data gets shared between threads making it difficult to accurately measure RAM usage.

The memory consumption stack trace was made by using <a href="https://pypi.org/project/memory-profiler/">mprof</a> to monitor this program brute force 10,000 addresses on a 4 logical processor machine with 8GB of RAM. As a result, 4 child processes were created, each consuming 2100MiB of RAM (~2GB).

