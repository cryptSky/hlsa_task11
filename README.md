### Setup

1. Install docker
2. Install siege

## Steps to run

1. `docker-compose up --build` 
2. Open redis-master docker container terminal
3. Run `redic-cli`
4. `config set maxmemory 3mb`
   

### Results

Set eviction strategy via redis-cli
`config set maxmemory-policy noeviction` 


You can check the implementation of probabilistic cache flushing [here](server/rest/user.py)

`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`
```console
Transactions:                   3382 hits
Availability:                  75.09 %
Elapsed time:                  23.76 secs
Data transferred:               0.20 MB
Response time:                  0.70 secs
Transaction rate:             142.34 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                   99.50
Successful transactions:        3382
Failed transactions:            1122
Longest transaction:            0.88
Shortest transaction:           0.04
```

Set eviction strategy via redis-cli
`config set maxmemory-policy allkeys-lru` 

`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`

```console
Transactions:                  12354 hits
Availability:                 100.00 %
Elapsed time:                  59.71 secs
Data transferred:               0.48 MB
Response time:                  0.48 secs
Transaction rate:             206.90 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                   99.59
Successful transactions:       12354
Failed transactions:               0
Longest transaction:            0.87
Shortest transaction:           0.05
```

Set eviction strategy via redis-cli
`config set maxmemory-policy volatile-lru` 

`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`

```console
Transactions:                  13651 hits
Availability:                 100.00 %
Elapsed time:                  59.40 secs
Data transferred:               0.53 MB
Response time:                  0.43 secs
Transaction rate:             229.81 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                   99.61
Successful transactions:       13651
Failed transactions:               0
Longest transaction:            0.72
Shortest transaction:           0.02
```


Set eviction strategy via redis-cli
`config set maxmemory-policy allkeys-random` 

`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`

```console
Transactions:                  12217 hits
Availability:                 100.00 %
Elapsed time:                  59.07 secs
Data transferred:               0.48 MB
Response time:                  0.48 secs
Transaction rate:             206.82 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                   99.45
Successful transactions:       12217
Failed transactions:               0
Longest transaction:            1.03
Shortest transaction:           0.02
```

Set eviction strategy via redis-cli
`config set maxmemory-policy volatile-random` 

`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`

```console
Transactions:                  14761 hits
Availability:                 100.00 %
Elapsed time:                  59.41 secs
Data transferred:               0.58 MB
Response time:                  0.40 secs
Transaction rate:             248.46 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                   99.47
Successful transactions:       14761
Failed transactions:               0
Longest transaction:            0.73
Shortest transaction:           0.02
```


Set eviction strategy via redis-cli
`config set maxmemory-policy volatile-ttl` 

`siege -c100 -t60S --content-type "application/json" 'http://localhost:8000/users POST {}'`

```console
Transactions:                  15882 hits
Availability:                 100.00 %
Elapsed time:                  59.13 secs
Data transferred:               0.62 MB
Response time:                  0.37 secs
Transaction rate:             268.59 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                   99.72
Successful transactions:       15882
Failed transactions:               0
Longest transaction:            0.95
Shortest transaction:           0.02
```


