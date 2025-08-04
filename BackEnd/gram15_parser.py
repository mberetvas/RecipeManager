"""15gram_parser.py

Parses recipes from 15gram.be HTML pages into structured Python objects.
Uses BeautifulSoup for HTML parsing and regular expressions for ingredient extraction.

Classes:
    Ingredient: Represents a single ingredient with optional amount, unit, and name.
    CookbookEntry: Metadata for a recipe (title, description, servings, prep time).
    RecipeStep: Represents a single instruction step.
    Recipe: Aggregates cookbook entry, ingredients, and instructions.
    FifteenGramParser: Main parser class for extracting recipe data from HTML.

Example:
    parser = FifteenGramParser()
    recipe = parser.parse(html)
"""

from typing import List, Optional
from bs4 import BeautifulSoup
from Utils.custom_logger import logger
from BackEnd.data_models import (
    IngredientData,
    CookbookEntryData,
    RecipeStepData,
    RecipeData,
)
import re


class FifteenGramParser:
    """Parser for extracting recipe data from 15gram.be HTML pages."""

    def parse(self, html: str, url: str) -> Optional[RecipeData]:
        """Parses the entire HTML page and returns a Recipe object or None if not a valid recipe.

        Args:
            html (str): The HTML content of the recipe page.

        Returns:
            Optional[Recipe]: Parsed recipe data including metadata, ingredients, and instructions, or None if not a valid recipe page.
        """
        logger.debug("Starting HTML parsing for recipe.")
        soup = BeautifulSoup(html, "html.parser")
        cookbook_entry = self._parse_entry(soup, url)
        ingredients = self._parse_ingredients(html)
        instructions = self._parse_instructions(soup)
        recipe = RecipeData(
            cookbook_entry_data=cookbook_entry,
            ingredients_data=ingredients,
            instructions_data=instructions,
        )
        if not self._is_valid_recipe(recipe):
            logger.info("HTML does not represent a valid recipe page. Returning None.")
            return None
        logger.debug("Finished HTML parsing for recipe.")
        return recipe

    def _is_valid_recipe(self, recipe: RecipeData) -> bool:
        """Checks if the parsed Recipe object contains the minimal required fields to be considered valid.

        Args:
            recipe (Recipe): The parsed Recipe object.

        Returns:
            bool: True if the recipe is valid, False otherwise.
        """
        entry = recipe.cookbook_entry_data
        if not entry or not entry.title or not entry.title.strip():
            logger.debug("Recipe invalid: missing or empty title.")
            return False
        if not recipe.ingredients_data or len(recipe.ingredients_data) == 0:
            logger.debug("Recipe invalid: no ingredients found.")
            return False
        if not recipe.instructions_data or len(recipe.instructions_data) == 0:
            logger.debug("Recipe invalid: no instructions found.")
            return False
        return True

    def _parse_entry(self, soup: BeautifulSoup, url: str) -> CookbookEntryData:
        """Extracts recipe metadata from the HTML soup.

        Args:
            soup (BeautifulSoup): Parsed HTML soup.

        Returns:
            CookbookEntry: Metadata for the recipe.
        """
        logger.debug("Parsing cookbook entry.")
        title_tag = soup.select_one("h1.text-center") or soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""
        logger.debug(f"Extracted title: {title}")

        descr_tag = soup.select_one(".recipe-description p") or soup.find(
            "meta", attrs={"name": "description"}
        )
        description = ""
        if descr_tag:
            if hasattr(descr_tag, "get_text"):
                description = descr_tag.get_text(strip=True)
            elif descr_tag.has_attr("content"):
                description = descr_tag["content"]
        logger.debug(f"Extracted description: {description}")

        servings = ""
        prep_time = ""
        yield_tag = soup.select_one(".yield-container .yield") or soup.find("span", class_="yield")
        servings = yield_tag.get_text(strip=True) if yield_tag else ""
        logger.debug(f"Extracted servings: {servings}")

        duration_tag = soup.select_one(".duration-container .duration") or soup.find(
            "span", class_="duration"
        )
        prep_time = duration_tag.get_text(strip=True) if duration_tag else ""
        logger.debug(f"Extracted prep time: {prep_time}")

        return CookbookEntryData(
            title=title,
            description=description,
            servings=servings,
            prep_time=prep_time,
            src_url=url,
        )

    def _parse_ingredients(self, html: str) -> List[IngredientData]:
        """Parses ingredients from HTML using the internal parsing logic.

        Args:
            html (str): The HTML content of the recipe page.

        Returns:
            List[Ingredient]: List of parsed ingredients.
        """
        return self._parse_ingredients_from_html(html)

    def _parse_ingredients_from_html(
        self, html: str, parser: str = "html.parser"
    ) -> List[IngredientData]:
        """Extracts ingredient lines from the HTML and parses them into Ingredient objects.

        Args:
            html (str): The HTML content of the recipe page.
            parser (str): The parser to use for BeautifulSoup (default: 'html.parser').

        Returns:
            List[Ingredient]: List of parsed ingredients.
        """
        logger.debug("Starting ingredient parsing from HTML.")
        soup = BeautifulSoup(html, parser)
        ingredients = []
        u = soup.find("div", id="ingredients")
        if u:
            logger.debug("Found 'ingredients' div.")
            ul = u.find("ul")
            if ul:
                for li in ul.find_all("li"):
                    txt = li.get_text(strip=True)
                    if txt:
                        ingredients.append(self._parse_ingredient_line(txt))
        logger.debug(f"Finished ingredient parsing. Found {len(ingredients)} ingredients.")
        return ingredients

    def _parse_ingredient_line(self, line: str) -> IngredientData:
        """Parses a single ingredient line into an Ingredient object.

        Args:
            line (str): The raw ingredient line.

        Returns:
            Ingredient: Parsed ingredient data.
        """
        logger.debug(f"Parsing ingredient line: '{line}'")
        fraction_map = {
            "¼": "0.25",
            "½": "0.5",
            "¾": "0.75",
            "⅐": "0.142857",
            "⅑": "0.111111",
            "⅒": "0.1",
            "⅓": "0.333333",
            "⅔": "0.666667",
            "⅕": "0.2",
            "⅖": "0.4",
            "⅗": "0.6",
            "⅘": "0.8",
            "⅙": "0.166667",
            "⅚": "0.833333",
            "⅛": "0.125",
            "⅜": "0.375",
            "⅝": "0.625",
            "⅞": "0.875",
        }
        pat = r"""
        ^\s*
        (
            \d+[\.,]?\d*         # e.g., 50, 1.5
            |¼|½|¾|⅐|⅑|⅒|⅓|⅔|⅕|⅖|⅗|⅘|⅙|⅚|⅛|⅜|⅝|⅞
            |een|hele|halve|half|snuifje
        )?
        \s*
        (teentje|teentjes|gr|g|kg|ml|cl|l|el|tl|kl|stuk|stuks|stukken|snuifje)?\b   # unit (optional)
        [\.\s]*
        (.*)                        # rest is the ingredient name
        $
        """
        regex = re.compile(pat, flags=re.I | re.X)
        match = regex.match(line)
        amount = None
        unit = None
        name = None
        if match:
            amount = match.group(1)
            unit = self._normalize_unit(match.group(2))
            name = match.group(3).strip() if match.group(3) else None
            logger.debug(f"Regex matched: amount='{amount}', unit='{unit}', name='{name}'")
            if amount in fraction_map:
                logger.debug(f"Converting fraction '{amount}' to decimal.")
                amount = fraction_map[amount]
            if unit is None and amount is not None and name:
                parts = name.split(None, 1)
                if len(parts) > 1 and self._normalize_unit(parts[0]) is not None:
                    logger.debug(f"Attempting to infer unit from name part: '{parts[0]}'")
                    unit = self._normalize_unit(parts[0])
                    name = parts[1]
        else:
            name = line
            logger.debug(f"No regex match, setting full line as name: '{name}'")
        parsed_ingredient = IngredientData(raw_text=line, amount=amount, unit=unit, name=name)
        logger.debug(f"Parsed ingredient: {parsed_ingredient}")
        return parsed_ingredient

    def _normalize_unit(self, unit: Optional[str]) -> Optional[str]:
        """Converts unit variants to canonical form.

        Args:
            unit (Optional[str]): The unit string to normalize.

        Returns:
            Optional[str]: Canonical unit string or None if not recognized.
        """
        if not unit:
            logger.debug("Unit is None, returning None.")
            return None
        logger.debug(f"Normalizing unit: '{unit}'")
        unit_map = {
            "gr": "g",
            "g": "g",
            "kg": "kg",
            "ml": "ml",
            "cl": "cl",
            "l": "l",
            "el": "el",
            "tl": "tl",
            "kl": "kl",
            "stuk": "stuks",
            "stuks": "stuks",
            "stukken": "stuks",
            "teentje": "teentje",
            "teentjes": "teentje",
            "snuifje": "snuifje",
        }
        key = unit.strip().lower()
        normalized_unit = unit_map.get(key, key)
        logger.debug(f"Normalized '{unit}' to '{normalized_unit}'")
        return normalized_unit

    def _parse_instructions(self, soup: BeautifulSoup) -> List[RecipeStepData]:
        """Extracts instruction steps from the HTML soup.

        Args:
            soup (BeautifulSoup): Parsed HTML soup.

        Returns:
            List[RecipeStep]: List of instruction steps.
        """
        logger.debug("Starting instruction parsing.")
        instructions = []
        instructions_ol = soup.find("div", id="preparation")
        if instructions_ol:
            logger.debug("Found 'preparation' div.")
            ol = instructions_ol.find("ol")
            if ol:
                for idx, li in enumerate(ol.find_all("li"), 1):
                    step = li.get_text(strip=True)
                    instructions.append(RecipeStepData(step_number=idx, instruction=step))
        logger.debug(f"Finished instruction parsing. Found {len(instructions)} instructions.")
        return instructions
