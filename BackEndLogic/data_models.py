from dataclasses import dataclass
from typing import List, Optional


@dataclass
class IngredientData:
    """Represents a single ingredient parsed from a recipe.

    Attributes:
        raw_text (str): The original ingredient line.
        amount (Optional[str]): The quantity of the ingredient.
        unit (Optional[str]): The unit of measurement.
        name (Optional[str]): The name of the ingredient.
    """

    raw_text: str
    amount: Optional[str] = None
    unit: Optional[str] = None
    name: Optional[str] = None


@dataclass
class CookbookEntryData:
    """Metadata for a recipe, including title, description, servings, and prep time.

    Attributes:
        title (str): The recipe title.
        description (str): Short description of the recipe.
        servings (str): Number of servings.
        prep_time (str): Preparation time.
    """

    title: str
    description: str
    servings: str
    prep_time: str
    cuisine_origin: Optional[str] = None  # Default to Belgian cuisine
    file_location: Optional[str] = None  # File location for saved recipes
    src_url: Optional[str] = None  # URL of the recipe page
    price: Optional[float] = (
        None  # Placeholder for total recipe price, Will be used in future features
    )


@dataclass
class RecipeStepData:
    """Represents a single step in the recipe instructions.

    Attributes:
        step_number (int): The step number.
        instruction (str): The instruction text.
    """

    step_number: int
    instruction: str


@dataclass
class RecipeData:
    """Aggregates all parsed data for a recipe.

    Attributes:
        cookbook_entry (CookbookEntry): Metadata for the recipe.
        ingredients (List[Ingredient]): List of parsed ingredients.
        instructions (List[Instructions]): List of instruction steps.
    """

    cookbook_entry_data: CookbookEntryData
    ingredients_data: List[IngredientData]
    instructions_data: List[RecipeStepData]
