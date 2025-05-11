#!/bin/bash

#Prevents __pycache__ creation
export PYTHONDONTWRITEBYTECODE=1

#Start the FastAPI server
uvicorn main:app --reload --port 9000
