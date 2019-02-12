# Trade ledger

The aim of this project is to keep track on orders and have all requests ledger saved.

## Setup introduction
### From battling-knights
*NOTE: X rates provider needs have base api key and abse url (missing in docker-compose.yml) 
* Step to setup:
Run in separate windows:
`docker-compose up db`
`docker-compose up redis`
`make build`
* Step to run:  
`make run`
* Step to run tests:    
`make test`


Current state of app:
* /last/ returns filtered results for Redis and isoformat of last created result from MySQL
* Missing:
* errors handling
* OpenApi doc
* Some responses validation
* circle-ci
