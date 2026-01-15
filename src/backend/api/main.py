from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.model.inference import load_model
from src.backend.api.core.config import settings, MODEL_DIR
from src.backend.api.v1.routers.predict import router as predict_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    model, config = load_model(MODEL_DIR, settings.DEVICE)
    app.state.model = model
    app.state.config_model = config
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(predict_router, prefix=settings.API_V1_STR)

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])