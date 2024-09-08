from backend.service.team_service import generate_team
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/teams", summary="Retrieve a team of superheroes")
async def get_team_suggestion(criteria: str = "random"):
    """
    Retrieves a team of superheroes based on criteria.

    Returns:
        A list of Superheroes based on selection criteria given by user.
    """
    return JSONResponse(jsonable_encoder(generate_team(criteria)))
