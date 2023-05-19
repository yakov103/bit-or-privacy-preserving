# bit-or-privacy-preserving

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
