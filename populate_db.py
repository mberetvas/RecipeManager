import asyncio
import httpx
from BackEnd.data_models import RecipeData
from BackEnd.orm_models import Base, CookbookEntry, Recipe, Ingredient, RecipeStep
from BackEnd.sqlite_db_connection import engine
from BackEnd.gram15_parser import FifteenGramParser
from BackEnd.sqlite_db_connection import async_session


async def create_all_tables() -> None:
    """
    Asynchronously create all tables in the database as defined in the ORM models.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully.")


async def get_html_content(url: str) -> str:
    """
    Asynchronously fetch HTML content from a URL.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def parse_recipe(html: str) -> RecipeData:
    """
    Parses a recipe from the provided HTML content.
    """
    parser = FifteenGramParser()
    return parser.parse(html)


async def save_recipe_to_db(recipe: RecipeData) -> None:
    """
    Saves the parsed recipe data to the database.
    """
    async with async_session() as session:
        async with session.begin():
            cookbookentry_orm = CookbookEntry(**recipe.cookbook_entry_data.__dict__)
            session.add(cookbookentry_orm)
            await session.commit()

            recipe_orm = Recipe(cookbook_entry=cookbookentry_orm)
            session.add(recipe_orm)
            await session.commit()

            # Save ingredients and instructions
            for ingredient in recipe.ingredients_data:
                ingredient_orm = Ingredient(**ingredient.__dict__)
                session.add(ingredient_orm)
            await session.commit()

            # Save recipe steps
            for step in recipe.instructions_data:
                step_orm = RecipeStep(**step.__dict__)
                session.add(step_orm)
            await session.commit()


async def main():
    # Example URL (replace with actual recipe URL)
    url = "https://15gram.be/artikelen/10-gerechten-die-het-waard-zijn-om-de-barbecue-aan-te-steken"

    # Create all tables in the database if they do not exist
    await create_all_tables()

    # Fetch HTML content
    html_content = await get_html_content(url)

    # Parse the recipe
    recipe = await parse_recipe(html_content)

    if recipe is None:
        print("No valid recipe found in the provided HTML content.")
        return

    # Save the recipe to the database
    await save_recipe_to_db(recipe)

    print("Recipe saved to the database successfully.")
    from pprint import pprint

    pprint(recipe)


if __name__ == "__main__":
    asyncio.run(main())
