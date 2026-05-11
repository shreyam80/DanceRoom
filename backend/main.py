from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, organizations, teams, subgroups, routines, videos, comments, dashboards
from app.core.config import settings

app = FastAPI(title="DanceRoom API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(subgroups.router, prefix="/subgroups", tags=["subgroups"])
app.include_router(routines.router, prefix="/routines", tags=["routines"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(dashboards.router, prefix="/dashboard", tags=["dashboard"])
