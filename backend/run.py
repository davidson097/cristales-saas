#!/usr/bin/env python
import uvicorn
try:
    from app.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Error importing app: {e}")
    exit(1)

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error running server: {e}")