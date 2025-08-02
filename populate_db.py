import asyncio
import httpx
from Utils.custom_logger import logger
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
    Handles foreign key relationships and errors.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                # Create and add CookbookEntry
                cookbookentry_orm = CookbookEntry(**recipe.cookbook_entry_data.__dict__)
                session.add(cookbookentry_orm)
                await session.flush()  # Get cookbookentry_orm.id

                # Create and add Recipe, link to CookbookEntry
                recipe_orm = Recipe(cookbook_entry_id=cookbookentry_orm.id)
                session.add(recipe_orm)
                await session.flush()  # Get recipe_orm.id

                # Add Ingredients
                for ingredient in recipe.ingredients_data:
                    ingredient_orm = Ingredient(**ingredient.__dict__, recipe_id=recipe_orm.id)
                    session.add(ingredient_orm)

                # Add Recipe Steps
                for step in recipe.instructions_data:
                    step_orm = RecipeStep(**step.__dict__, recipe_id=recipe_orm.id)
                    session.add(step_orm)

            # Commit once at the end
            await session.commit()
    except Exception as e:
        logger.error(f"Failed to save recipe: {e}")
        await session.rollback()
        raise


async def recipe_exists(url: str, title: str) -> bool:
    """
    Check if a recipe with the given URL or title already exists in the database.

    Parameters:
    url (str): The source URL of the recipe to check.
    title (str): The title of the recipe to check.

    Returns:
    bool: True if a recipe with the given URL or title exists, False otherwise.
    """
    async with async_session() as session:
        result = await session.execute(
            # CookbookEntry.src_url or CookbookEntry.title
            # Use ilike for case-insensitive title match
            CookbookEntry.__table__.select().where(
                (CookbookEntry.src_url == url) | (CookbookEntry.title.ilike(title))
            )
        )
        row = result.first()
        return row is not None


async def main():
    # Example URL (replace with actual recipe URL)
    url = "https://15gram.be/recepten/mignonette-met-dragon-champignonsaus-venkel-en-zoete-aardappelfrietjes"

    # Create all tables in the database if they do not exist
    await create_all_tables()

    # Check if recipe already exists
    title = "Mignonette met dragon, champignonsaus, venkel en zoete aardappelfrietjes"
    exists = await recipe_exists(url, title)
    if exists:
        print("Recipe already exists in the database.")
        return

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
