from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.routes import health, summary, analytics, prediction

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="NYC Taxi Public Transportation Demand Analysis and Passenger Prediction System (Phase 1)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for clean JSON error responses
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred", "error": str(exc)}
    )

# Register routes with /api prefix
app.include_router(health.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(prediction.router, prefix="/api")

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "api_root": "/api/health"
    }
