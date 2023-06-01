# bit-or-privacy-preserving

# How to run

```bash
    git clone https://github.com/yakov103/bit-or-privacy-preserving/tree/mix_the_code_with_union
```

```
    cd bit-or-privacy-preserving
```
open env

```
    virtualenv .venv
    source .venv/bin/activate
```

make sure you have python installed on your sysmte, based on your OS python / python3 , pip / pip3 will be used in the termianl

```
    pip3 install -r requirements.txt
```

## Run Alice

Open terminal in project directory

```
    cd ServerA
    python3 ServerA.p
```

## Run Bob

Open terminal in projet directory

```
    cd ServerB
    python3 ServerB.py
```


# Run Clients

# Run Alice Client

opne terminal for alice
```
    python3 testA.py
```

open terminal for bob

```
    python3 testB.py
```









```mermaid
sequenceDiagram
actor Alice
actor Bob
    par send request
    ServerA ->> Alice : 1 or 0 
    activate Alice
    ServerB ->> Bob : 1 or 0
    end
    
    Alice ->> Alice: k
    Alice ->> Bob: Ca , q , g , g^k
    deactivate Alice
    activate Bob
    Bob ->> Alice : Cb
    deactivate Bob
    activate Alice
    par Return the same result
    Alice ->> ServerA : Algo result is 1 or 0 
    Alice ->> Bob: Algo result
    Bob ->> ServerB : Algo result
    end
    deactivate Alice
 ```
