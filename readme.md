docker build -t pybox pybox

docker-compose up --remove-orphans

docker run  --network host -v `pwd`:/app/ -it pybox:latest sh
 -> /app/pybox/indexer.py
 -> /app/pybox/search.py
