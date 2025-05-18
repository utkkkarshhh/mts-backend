#!/bin/bash

# Prevents __pycache__ creation
export PYTHONDONTWRITEBYTECODE=1

# Start FastAPI server
uvicorn main:app --reload --port 9000 &
PID_UVICORN=$!

# Start Redis RQ workers for each queue
python ./app/redis/worker.py HIGH &
PID_WORKER_HIGH=$!

python ./app/redis/worker.py MEDIUM &
PID_WORKER_MEDIUM=$!

python ./app/redis/worker.py LOW &
PID_WORKER_LOW=$!

# Start rq-dashboard
rq-dashboard &
PID_DASHBOARD=$!

# Cleanup function
cleanup() {
    echo "🛑 Stopping all services..."
    kill $PID_UVICORN $PID_WORKER_HIGH $PID_WORKER_MEDIUM $PID_WORKER_LOW $PID_DASHBOARD
    exit 0
}

trap cleanup SIGINT

# Wait for all services
wait $PID_UVICORN $PID_WORKER_HIGH $PID_WORKER_MEDIUM $PID_WORKER_LOW $PID_DASHBOARD
