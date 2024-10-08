from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router import router
from src.model.model import Recipe
from src.schema.recipe import RecipePost, RecipeResponse
from src.storage.db import get_db



@router.get('/receipts')
async def get_receipts(session: AsyncSession = Depends(get_db)):
    receipts = await session.execute(select(Recipe))
    res = []
    for recipe in receipts.all():
        res.append(recipe[0].__dict__)

    return {'receipts': res}

@router.post('/receipts', response_model=RecipeResponse)
async def create_recipe(body: RecipePost, session: AsyncSession = Depends(get_db)) -> ORJSONResponse:
    recipe = Recipe(**body.model_dump())
    session.add(recipe)
    await session.commit()
    return ORJSONResponse({'id': recipe.id})


@router.get('/receipts/{user_id}')
async def get_recipe_by_user_id(user_id: int, session: AsyncSession = Depends(get_db)):
    receipts = await session.execute(select(Recipe).where(Recipe.user_id==user_id))
    res = []
    for recipe in receipts.all():
        res.append(recipe[0].__dict__)
    return {'receipts': res}
