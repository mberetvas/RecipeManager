"""
SQLAlchemy ORM models for CuisineCraft recipe management.
Defines Ingredient, CookbookEntry, RecipeStep, and Recipe models with relationships.
"""

from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class CookbookEntry(Base):
    """
    Metadata for a recipe, including title, description, servings, and prep time.
    """

    __tablename__ = "cookbook_entries"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(255), nullable=False)
    description: str = Column(Text, nullable=False)
    servings: str = Column(String(50), nullable=False)
    prep_time: str = Column(String(50), nullable=False)
    cuisine_origin: Optional[str] = Column(String(100), nullable=True)
    file_location: Optional[str] = Column(String(255), nullable=True)
    src_url: Optional[str] = Column(String(255), nullable=True)
    price: Optional[float] = Column(Float, nullable=True)

    recipe = relationship("Recipe", back_populates="cookbook_entry", uselist=False)

    def __repr__(self):
        return f"<CookbookEntry(title={self.title}, cuisine_origin={self.cuisine_origin})>"


class Recipe(Base):
    """
    Aggregates all parsed data for a recipe.
    """

    __tablename__ = "recipes"

    id: int = Column(Integer, primary_key=True)
    cookbook_entry_id: int = Column(
        Integer, ForeignKey("cookbook_entries.id"), nullable=False, unique=True
    )

    cookbook_entry = relationship("CookbookEntry", back_populates="recipe")
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("RecipeStep", back_populates="recipe", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """
        Return a string representation of the Recipe instance.
        """
        return f"<Recipe(id={self.id}, cookbook_entry_id={self.cookbook_entry_id})>"


class Ingredient(Base):
    """
    Represents a single ingredient parsed from a recipe.
    """

    __tablename__ = "ingredients"

    id: int = Column(Integer, primary_key=True)
    recipe_id: int = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    raw_text: str = Column(Text, nullable=False)
    amount: Optional[str] = Column(String(50), nullable=True)
    unit: Optional[str] = Column(String(50), nullable=True)
    name: Optional[str] = Column(String(255), nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")

    def __repr__(self) -> str:
        """
        Return a string representation of the Ingredient instance.
        """
        return (
            f"<Ingredient(id={self.id}, name={self.name}, amount={self.amount}, unit={self.unit})>"
        )


class RecipeStep(Base):
    """
    Represents a single step in the recipe instructions.
    """

    __tablename__ = "recipe_steps"
    __table_args__ = (UniqueConstraint("recipe_id", "step_number", name="_recipe_step_uc"),)

    id: int = Column(Integer, primary_key=True)
    recipe_id: int = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    step_number: int = Column(Integer, nullable=False)
    instruction: str = Column(Text, nullable=False)

    recipe = relationship("Recipe", back_populates="instructions")

    def __repr__(self) -> str:
        """
        Return a string representation of the RecipeStep instance.
        """
        return f"<RecipeStep(id={self.id}, recipe_id={self.recipe_id}, step_number={self.step_number})>"


class IngredientPrice(Base):
    """
    Stores price information for ingredients, enabling cost calculations for recipes and weekplanning.
    """

    __tablename__ = "ingredient_prices"

    id: int = Column(Integer, primary_key=True)
    ingredient_name: str = Column(String(255), nullable=False, index=True)
    unit: str = Column(String(50), nullable=False)
    price_per_unit: float = Column(Float, nullable=False)
    store: Optional[str] = Column(String(100), nullable=True)
    date: Optional[str] = Column(String(50), nullable=True)  # ISO date string or similar

    def __repr__(self) -> str:
        """
        Return a string representation of the IngredientPrice instance.
        """
        return f"<IngredientPrice(id={self.id}, ingredient_name={self.ingredient_name}, unit={self.unit}, price_per_unit={self.price_per_unit})>"


class WeekPlanning(Base):
    """
    Stores a weekplanning, which can contain up to 7 days (Monday to Sunday) and references recipes for each day.
    """

    __tablename__ = "weekplannings"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)
    created_at: str = Column(String(50), nullable=False)  # ISO date string
    days: int = Column(Integer, nullable=False)  # Number of days in planning (max 7)

    recipes = relationship(
        "WeekPlanningRecipe",
        back_populates="weekplanning",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """
        Return a string representation of the WeekPlanning instance.
        """
        return f"<WeekPlanning(id={self.id}, name={self.name}, days={self.days})>"


class WeekPlanningRecipe(Base):
    """
    Association table linking a weekplanning to recipes for specific days.
    """

    __tablename__ = "weekplanning_recipes"
    __table_args__ = (UniqueConstraint("weekplanning_id", "day", name="_weekplanning_day_uc"),)

    id: int = Column(Integer, primary_key=True)
    weekplanning_id: int = Column(Integer, ForeignKey("weekplannings.id"), nullable=False)
    recipe_id: int = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    day: int = Column(Integer, nullable=False)  # 1=Monday, 7=Sunday

    weekplanning = relationship("WeekPlanning", back_populates="recipes")
    recipe = relationship("Recipe")

    def __repr__(self) -> str:
        """
        Return a string representation of the WeekPlanningRecipe instance.
        """
        return f"<WeekPlanningRecipe(id={self.id}, weekplanning_id={self.weekplanning_id}, recipe_id={self.recipe_id}, day={self.day})>"
