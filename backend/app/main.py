from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.videos import router as videos_router

app = FastAPI(title="Content Factory API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(videos_router)


@app.get("/api/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
