import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":

    # defining the entry point for our server
    uvicorn.run(
        "server.app:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        reload=True,
    )
