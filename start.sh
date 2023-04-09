#!/bin/bash
uvicorn main:app --reload --reload-dir . --host 0.0.0.0 --port 8000