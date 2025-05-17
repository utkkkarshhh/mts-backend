#!/bin/bash

# Prevents __pycache__ creation
export PYTHONDONTWRITEBYTECODE=1

# Start FastAPI server
uvicorn main:app --reload --port 9000 &
PID_UVICORN=$!

# Start Redis RQ worker
python ./redis_queue/worker.py &
PID_WORKER=$!

# Start rq-dashboard
rq-dashboard &
PID_DASHBOARD=$!

cleanup() {
    echo "🛑 Stopping all services..."
    kill $PID_UVICORN $PID_WORKER $PID_DASHBOARD
    exit 0
}
trap cleanup SIGINT
wait $PID_UVICORN $PID_WORKER $PID_DASHBOARD
