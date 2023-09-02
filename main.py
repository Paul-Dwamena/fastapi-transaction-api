from fastapi import FastAPI
from server.router import router as server_router
from server.schema import SessionLocal, Base,engine



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fido Backend Service",
    description="Webservice For Project Fido Backend Server",
    version="0.0.1",
)


app.include_router(server_router)


@app.get("/")
async def root():
    return {"message": "Server connected successfully"}