from fastapi import FastAPI
from routes.index_route import router as index_router

app = FastAPI(title="To-Do-List", version="1.0.0", openapi_url="/openapi.json")

app.include_router(index_router)



if __name__== "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8000)
    