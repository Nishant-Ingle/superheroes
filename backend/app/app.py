import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import superheroes_controller, teams_controller
from backend.config.startup import perform_startup_tasks

if __name__ == "__main__":
    app = FastAPI(
        title="Superhero API",
        description="API for managing superheroes",
        docs_url="/docs")  # URL for interactive API documentation

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["GET", "POST", "PUT"]
    )
    app.include_router(superheroes_controller.router)
    app.include_router(teams_controller.router)

    perform_startup_tasks()
    uvicorn.run(app)
