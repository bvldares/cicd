#!/usr/bin/env python3
"""
Entry point per avviare l'applicazione FastAPI
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
