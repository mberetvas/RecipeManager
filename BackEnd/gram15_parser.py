"""15gram_parser.py

Parses recipes from 15gram.be HTML pages into structured Python objects.
Uses BeautifulSoup for HTML parsing and regular expressions for ingredient extraction.

Classes:
    Ingredient: Represents a single ingredient with optional amount, unit, and name.
    CookbookEntry: Metadata for a recipe (title, description, servings, prep time).
    Instructions: Represents a single instruction step.
    Recipe: Aggregates cookbook entry, ingredients, and instructions.
    FifteenGramParser: Main parser class for extracting recipe data from HTML.

Example:
    parser = FifteenGramParser()
    recipe = parser.parse(html)
"""

from typing import List, Optional
from bs4 import BeautifulSoup
from back_end.custom_logger import logger
from back_end.data_models import (
    Ingredient,
    CookbookEntry,
    RecipeStep,
    Recipe,
)
import re


class FifteenGramParser:
    """Parser for extracting recipe data from 15gram.be HTML pages."""

    def parse(self, html: str) -> Recipe:
        """Parses the entire HTML page and returns a Recipe object.

        Args:
            html (str): The HTML content of the recipe page.

        Returns:
            Recipe: Parsed recipe data including metadata, ingredients, and instructions.
        """
        logger.debug("Starting HTML parsing for recipe.")
        soup = BeautifulSoup(html, "html.parser")
        cookbook_entry = self._parse_entry(soup)
        ingredients = self._parse_ingredients(html)
        instructions = self._parse_instructions(soup)
        recipe = Recipe(
            cookbook_entry=cookbook_entry,
            ingredients=ingredients,
            instructions=instructions,
        )
        logger.debug("Finished HTML parsing for recipe.")
        return recipe

    def _parse_entry(self, soup: BeautifulSoup) -> CookbookEntry:
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
        yield_tag = soup.select_one(".yield-container .yield") or soup.find(
            "span", class_="yield"
        )
        servings = yield_tag.get_text(strip=True) if yield_tag else ""
        logger.debug(f"Extracted servings: {servings}")

        duration_tag = soup.select_one(".duration-container .duration") or soup.find(
            "span", class_="duration"
        )
        prep_time = duration_tag.get_text(strip=True) if duration_tag else ""
        logger.debug(f"Extracted prep time: {prep_time}")

        return CookbookEntry(
            title=title, description=description, servings=servings, prep_time=prep_time
        )

    def _parse_ingredients(self, html: str) -> List[Ingredient]:
        """Parses ingredients from HTML using the internal parsing logic.

        Args:
            html (str): The HTML content of the recipe page.

        Returns:
            List[Ingredient]: List of parsed ingredients.
        """
        return self._parse_ingredients_from_html(html)

    def _parse_ingredients_from_html(
        self, html: str, parser: str = "html.parser"
    ) -> List[Ingredient]:
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
        logger.debug(
            f"Finished ingredient parsing. Found {len(ingredients)} ingredients."
        )
        return ingredients

    def _parse_ingredient_line(self, line: str) -> Ingredient:
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
            logger.debug(
                f"Regex matched: amount='{amount}', unit='{unit}', name='{name}'"
            )
            if amount in fraction_map:
                logger.debug(f"Converting fraction '{amount}' to decimal.")
                amount = fraction_map[amount]
            if unit is None and amount is not None and name:
                parts = name.split(None, 1)
                if len(parts) > 1 and self._normalize_unit(parts[0]) is not None:
                    logger.debug(
                        f"Attempting to infer unit from name part: '{parts[0]}'"
                    )
                    unit = self._normalize_unit(parts[0])
                    name = parts[1]
        else:
            name = line
            logger.debug(f"No regex match, setting full line as name: '{name}'")
        parsed_ingredient = Ingredient(
            raw_text=line, amount=amount, unit=unit, name=name
        )
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

    def _parse_instructions(self, soup: BeautifulSoup) -> List[RecipeStep]:
        """Extracts instruction steps from the HTML soup.

        Args:
            soup (BeautifulSoup): Parsed HTML soup.

        Returns:
            List[Instructions]: List of instruction steps.
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
                    instructions.append(RecipeStep(step_number=idx, instruction=step))
        logger.debug(
            f"Finished instruction parsing. Found {len(instructions)} instructions."
        )
        return instructions


if __name__ == "__main__":
    import requests
    import pprint

    # Example usage: fetch and parse a recipe from 15gram.be
    url = "https://15gram.be/recepten/gekruide-kip-met-aardappelblokjes-selder-radijs-en-appelsalade"
    response = requests.get(url)
    html = response.text

    parser = FifteenGramParser()
    recipe = parser.parse(html)

    pprint.pprint(recipe)
