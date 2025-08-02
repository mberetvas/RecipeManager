import asyncio
import httpx
from BackEnd.data_models import Recipe
from BackEnd.orm_models import Base
from BackEnd.sqlite_db_connection import engine
from BackEnd.gram15_parser import FifteenGramParser


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


async def parse_recipe(html: str) -> Recipe:
    """
    Parses a recipe from the provided HTML content.
    """
    parser = FifteenGramParser()
    return parser.parse(html)


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
    print(f"Recipe Title: {recipe.cookbook_entry.title}")
    print(f"Description: {recipe.cookbook_entry.description}")
    print(f"Servings: {recipe.cookbook_entry.servings}")
    print(f"Ingredients: {[ingredient.name for ingredient in recipe.ingredients]}")
    print(f"Instructions: {recipe.instructions}")


if __name__ == "__main__":
    asyncio.run(main())
