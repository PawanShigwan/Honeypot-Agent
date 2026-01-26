from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .routes import router

app = FastAPI(title="Agentic Honeypot API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal Server Error"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": "Invalid Request", "details": str(exc)},
    )

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
