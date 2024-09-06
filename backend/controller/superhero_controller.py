from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from backend.config.startup import perform_startup_tasks
from backend.models.Superhero import Superhero
from backend.service.SuperheroService import SuperheroService

app = FastAPI(
    title="Superhero API",
    description="API for managing superheroes",
    docs_url="/docs"  # URL for interactive API documentation
)


@app.get("/superheroes", summary="Retrieve all superheroes")
async def get_all_superheroes(name: Optional[str] = ""):
    """
    Retrieves a list of all superheroes.

    Returns:
        A list of dictionaries, each containing the superhero's ID and name.
    """
    return JSONResponse(SuperheroService.get_instance().get_superheroes(name.lower()))


@app.get("/superheroes/{superhero_id}", summary="Retrieve a superhero by ID")
async def get_superhero_by_id(superhero_id: int):
    """
    Retrieves a specific superhero object based on its ID.

    Args:
        superhero_id (int): The ID of the superhero to retrieve.

    Returns:
        The superhero object if found.

    Raises:
        HTTPException: If the superhero with ID is not found.
    """
    superhero_service = SuperheroService.get_instance()
    superhero = superhero_service.get_superhero(superhero_id)

    if not superhero:
        raise HTTPException(detail={"error": f"Superhero with ID {superhero_id} not found"}, status_code=404)

    return JSONResponse(jsonable_encoder(superhero))


@app.post("/superheroes", summary="Add a new superhero")
async def add_superhero(superhero: Superhero):
    """
    Adds a new superhero to the database.

    Args:
        superhero (Superhero): The superhero data to add.

    Returns:
        A message indicating success.

    Raises:
        HTTPException: If there's an error adding the superhero or if superhero ID already exists.
    """
    service = SuperheroService.get_instance()

    try:
        if service.add_superhero(superhero):
            return JSONResponse(content={"message": "Superhero added successfully"}, status_code=201,
                                headers={
                                    "Location": f"/superheroes/{superhero.id}"
                                })
    except Exception as e:
        raise HTTPException(detail=f"Superhero addition failed: {str(e)}", status_code=500)

    raise HTTPException(detail=f"Superhero update failed, make sure ID is not already present.", status_code=400)


@app.put("/superheroes/{superhero_id}", summary="Update a superhero")
async def update_superhero(superhero: Superhero):
    """
    Updates an existing superhero.

    Args:
        superhero_id (int): The ID of the superhero to update.
        superhero (Superhero): The updated superhero data.

    Returns:
        A message indicating success.

    Raises:
        HTTPException: If there's an error updating the superhero or if the superhero is not found.
    """
    service = SuperheroService.get_instance()

    try:
        if service.update_superhero(superhero):
            return JSONResponse(content={"message": "Superhero updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(detail=f"Superhero update failed: {str(e)}", status_code=500)

    raise HTTPException(detail=f"Superhero update failed, please check if ID already present.", status_code=400)


if __name__ == "__main__":
    perform_startup_tasks()
    uvicorn.run(app)
