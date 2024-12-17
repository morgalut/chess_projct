### chess 



## install Requirements.txt
- pip install Requirements.txt

## run
- cd backend
- py main.py

## test 
# Check White move
- curl -X POST http://localhost:5000/move -H "Content-Type: application/json" -d "{\"color\": \"white\", \"start_pos\": \"e2\", \"end_pos\": \"e4\"}"

# Check black move
- curl -X POST http://localhost:5000/move -H "Content-Type: application/json" -d "{\"start_pos\": \"e7\", \"end_pos\": \"e5\"}"
