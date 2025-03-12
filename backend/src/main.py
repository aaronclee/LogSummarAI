from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router as api_router

app = FastAPI(title="LogSummarAI API", description="API for summarizing logs from a noisy file.")

# Allow CORS from the frontend (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)