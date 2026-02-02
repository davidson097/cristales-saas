#!/usr/bin/env python3
"""
Launcher script for the Cristales SaaS API.
This script runs the FastAPI application from the backend directory.
"""

import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)