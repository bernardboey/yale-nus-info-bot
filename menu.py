import datetime
import textwrap

SG_TZ = datetime.timezone(offset=datetime.timedelta(hours=8))


class MealCategory:
    def __init__(self, items: str):
        """

        Args:
            items: String representing the food items for the meal (e.g. "Pulled Beef Sandwich, Fries, Coleslaw")
        """
        self.items = items

    def __repr__(self):
        return f"MealCategory(items='{self.items}')"

    @classmethod
    def parse_from_dict(cls, d):
        return MealCategory(d["items"])

    def to_dict(self):
        return {"items": self.items}


class MealType:
    def __init__(self, name: str):
        """

        Args:
            name: String representing the type name (e.g. "Bento" / "Buffet" / "Set Meal" / "Grab & Go")
        """
        self.name = name
        self.categories: list[MealCategory] = []

    def __repr__(self):
        return (f"MealType(name='{self.name}', categories=[\n" +
                ",\n".join(textwrap.indent(repr(category), "  ") for category in self.categories) +
                "\n])")

    def add_category(self, category: MealCategory):
        self.categories.append(category)

    @classmethod
    def parse_from_dict(cls, d):
        meal_type = MealType(d["name"])
        for category in d["categories"]:
            meal_type.add_category(MealCategory.parse_from_dict(category))
        return meal_type

    def to_dict(self):
        return {"name": self.name, "categories": [category.to_dict() for category in self.categories]}


class Meal:
    def __init__(self, name: str):
        """

        Args:
            name: String representing the meal name (e.g. "Brunch" / "Breakfast" / "Lunch" / "Dinner")
        """
        self.name = name
        self.types: list[MealType] = []

    def __repr__(self):
        return (f"Meal(name='{self.name}', types=[\n" +
                ",\n".join(textwrap.indent(repr(meal_type), "  ") for meal_type in self.types) +
                "\n])")

    def add_type(self, meal_type: MealType):
        self.types.append(meal_type)

    @classmethod
    def parse_from_dict(cls, d):
        meal = Meal(d["name"])
        for meal_type in d["types"]:
            meal.add_type(MealType.parse_from_dict(meal_type))
        return meal

    def to_dict(self):
        return {"name": self.name, "types": [meal_type.to_dict() for meal_type in self.types]}


class Menu:
    def __init__(self, datetime_: datetime.datetime = None):
        self.datetime = datetime_
        self.day = self.calculate_day()
        self.meals: list[Meal] = []

    def __str__(self):
        return f"Menu() {self.day, self.datetime.date() if self.datetime else '(No date)'}"

    def __repr__(self):
        return (f"Menu(day={self.day}, date={self.datetime.date() if self.datetime else None}, meals=[\n" +
                ",\n".join(textwrap.indent(repr(meal), "  ") for meal in self.meals) +
                "\n])")

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def set_date(self, date: datetime.date):
        self.datetime = datetime.datetime.combine(date, datetime.time.min, tzinfo=SG_TZ)
        self.day = self.calculate_day()

    def calculate_day(self):
        return self.datetime.strftime('%A') if self.datetime else None

    def add_meal(self, meal: Meal):
        self.meals.append(meal)

    @classmethod
    def parse_from_dict(cls, d: dict):
        menu = cls(datetime_=d["date"])
        for meal in d["meals"]:
            menu.add_meal(Meal.parse_from_dict(meal))
        return menu

    def to_dict(self):
        return {"date": self.datetime, "day": self.day, "meals": [meal.to_dict() for meal in self.meals]}
