import re
from typing import Dict, List

from model import Pizza

FAKE_USERS = {
    "vegan@ppizzahh.de": "nocheese",
    "basic@ppizzahh.de": "somecheese",
    "admin@ppizzahh.de": "muchoqueso",
    "a@b.c": "d",
}

_menu = [
    (
        "The Classic Margherita",
        "Tomato, Mozzarella, Basil",
        "A timeless delight with ripe tomatoes, creamy mozzarella, and fresh basil on a crispy crust.",
    ),
    (
        "Salami Simplicity",
        "Salami, Mozzarella",
        "Classic and straightforward, this pizza offers a generous helping of salami paired with melted mozzarella.",
    ),
    (
        "Mushroom Melt",
        "Mushrooms, Mozzarella",
        "A minimalist's dream, featuring earthy mushrooms and stretchy mozzarella cheese.",
    ),
    (
        "Cheesy Ham Haven",
        "Ham, Mozzarella",
        "Simple yet satisfying with chunks of ham nestled under a blanket of bubbling mozzarella.",
    ),
    (
        "Ham and Mushroom Harmony",
        "Ham, Mushrooms, Mozzarella",
        "A delightful blend of ham and mushrooms, topped with gooey mozzarella.",
    ),
    (
        "Onion Overture",
        "Onions, Mozzarella",
        "A melody of caramelized onions on a canvas of melted mozzarella.",
    ),
    (
        "Spinach and Ham Delight",
        "Spinach, Ham, Mozzarella",
        "A tasty trio of fresh spinach, savory ham, and creamy mozzarella.",
    ),
    (
        "Garlic Gusto",
        "Garlic, Mozzarella",
        "A bold garlic punch accompanied by smooth mozzarella for garlic lovers.",
    ),
    (
        "Pepperoni Pleasure",
        "Pepperoni, Mozzarella",
        "Nothing but the classics: pepperoni paired with our signature mozzarella.",
    ),
    (
        "Tomato Basil Bliss",
        "Tomato Slices, Basil, Mozzarella",
        "A fresh take with ripe tomato slices, aromatic basil, and stretchy mozzarella.",
    ),
    (
        "Cheese Corn Carnival",
        "Sweet Corn, Mozzarella",
        "A playful mix of sweet corn and mozzarella for a light and tasty experience.",
    ),
    (
        "Olives and Herb Oasis",
        "Black Olives, Oregano, Mozzarella",
        "Sliced olives and oregano sprinkled over mozzarella for a Mediterranean touch.",
    ),
    (
        "Cheddar Chunk Charm",
        "Cheddar, Mozzarella",
        "A cheese lover's fantasy, featuring hearty cheddar chunks and mozzarella.",
    ),
    (
        "Pineapple Paradise",
        "Pineapple, Mozzarella",
        "Sweet pineapple chunks on a cheesy bed, for a tropical twist.",
    ),
    (
        "Fiery Chili Fever",
        "Chili Peppers, Mozzarella",
        "Fiery chili peppers atop melting mozzarella for those who dare.",
    ),
    (
        "Sweet Pepper Panache",
        "Bell Peppers, Mozzarella",
        "Colorful bell peppers over gooey mozzarella for a sweet crunch.",
    ),
    (
        "Ricotta and Rosemary",
        "Ricotta, Rosemary, Mozzarella",
        "Creamy ricotta and fragrant rosemary, a simple gourmet treat.",
    ),
    (
        "BBQ Bonanza",
        "BBQ Sauce, Mozzarella",
        "A smoky BBQ base topped with a generous layer of mozzarella.",
    ),
    (
        "Garlic Chicken Charm",
        "Chicken, Garlic, Mozzarella",
        "Roasted garlic and tender chicken pieces, a white pizza with flair.",
    ),
    (
        "Sausage Serenade",
        "Sausage Slices, Mozzarella",
        "Hearty sausage slices atop our classic mozzarella for a fulfilling bite.",
    ),
    (
        "Bacon Crisp Craze",
        "Bacon, Mozzarella",
        "Crispy bacon pieces over melted mozzarella, simple and indulgent.",
    ),
    (
        "Pepperoni Feast",
        "Pepperoni, Tomato Sauce, Mozzarella",
        "Slices of spicy pepperoni atop a gooey mozzarella and rich tomato base.",
    ),
    (
        "Meat Lover's Dream",
        "Sausage, Pepperoni, Bacon, Ham",
        "A carnivorous mix of meats on a thick, golden crust that's sure to satisfy.",
    ),
    (
        "Veggie Supreme",
        "Bell Peppers, Onions, Mushrooms, Olives",
        "A garden of colorful veggies nestled on a bed of melting cheese.",
    ),
    (
        "BBQ Chicken Sensation",
        "BBQ Sauce, Chicken, Red Onions, Cilantro",
        "Tangy BBQ sauce drizzled over succulent chicken pieces, topped with sweet onions.",
    ),
    (
        "Hawaiian Luau",
        "Ham, Pineapple, Mozzarella",
        "A tropical twist with juicy pineapple chunks and savory ham pieces.",
    ),
    (
        "Fiery Buffalo",
        "Buffalo Sauce, Chicken, Blue Cheese",
        "Spicy buffalo sauce and chicken, cooled by creamy blue cheese crumbles.",
    ),
    (
        "Garlic Spinach Delight",
        "Spinach, Garlic, Ricotta, Mozzarella",
        "Leafy spinach and roasted garlic mingling with rich ricotta and mozzarella.",
    ),
    (
        "Four Cheese Harmony",
        "Mozzarella, Parmesan, Gouda, Goat Cheese",
        "A quartet of cheeses melting together in perfect harmony.",
    ),
    (
        "Truffle Treasure",
        "Mushrooms, Truffle Oil, Mozzarella",
        "Earthy mushrooms enhanced by aromatic truffle oil on a cheesy base.",
    ),
    (
        "Seafood Special",
        "Shrimp, Calamari, Garlic, Tomato",
        "Fresh seafood with a garlic kick, evoking the spirit of the ocean.",
    ),
    (
        "Bacon Double Cheeseburger",
        "Ground Beef, Bacon, Cheddar, Pickles",
        "All the flavors of a hearty cheeseburger translated into pizza form.",
    ),
    (
        "Sweet & Spicy Delicacy",
        "Italian Sausage, Honey, Chili Flakes",
        "A daring combo of sweet honey and spicy chili to excite your palate.",
    ),
    (
        "Tandoori Twist",
        "Tandoori Chicken, Red Onion, Cilantro",
        "An Indian-inspired creation with spiced tandoori chicken and fresh herbs.",
    ),
    (
        "Mediterranean Medley",
        "Feta, Sun-dried Tomatoes, Olives, Spinach",
        "A vibrant mix of Mediterranean flavors that transport you to sunny shores.",
    ),
    (
        "Alfredo Dream",
        "Chicken, Alfredo Sauce, Spinach, Mozzarella",
        "Creamy Alfredo sauce with tender chicken and spinach over a chewy crust.",
    ),
    (
        "Tuscan Sun",
        "Roasted Red Peppers, Sausage, Mozzarella, Basil",
        "The warmth of the Tuscan sun captured with roasted peppers and Italian sausage.",
    ),
    (
        "Spicy Italian",
        "Spicy Salami, Jalapeños, Tomato Sauce, Mozzarella",
        "Fiery salami and jalapeños ignite this pizza with bold Italian heat.",
    ),
    (
        "Pesto Perfection",
        "Pesto, Chicken, Sun-dried Tomatoes, Pine Nuts",
        "A green pesto base with savory chicken, tangy tomatoes, and crunchy pine nuts.",
    ),
    (
        "Garden Ranch",
        "Ranch Dressing, Cucumbers, Tomatoes, Bell Peppers",
        "A refreshing ranch base with a crisp garden veggie topping.",
    ),
    (
        "Triple Pig",
        "Ham, Sausage, Bacon, BBQ Swirl",
        "Three kinds of pork with a sweet BBQ swirl for an indulgent feast.",
    ),
    (
        "Sweet Fig Fantasy",
        "Figs, Ricotta, Arugula, Balsamic Glaze",
        "Sweet figs with creamy ricotta and balsamic glaze for a sophisticated bite.",
    ),
    (
        "Buffalo Mozzarella Magic",
        "Buffalo Mozzarella, Tomato, Basil, Olive Oil",
        "Creamy buffalo mozzarella with fresh tomatoes and basil, drizzled with olive oil.",
    ),
    (
        "Wild Mushroom Wonder",
        "Assorted Wild Mushrooms, Thyme, Mozzarella",
        "A mix of wild mushrooms with aromatic thyme on a cheesy backdrop.",
    ),
    (
        "Chipotle Chicken Craze",
        "Chipotle Chicken, Red Onions, Cilantro, Avocado",
        "Smoky chipotle chicken topped with fresh avocado and cilantro.",
    ),
    (
        "Carbonara Comfort",
        "Pancetta, Egg, Parmesan, Black Pepper",
        "A pizza twist on the classic pasta, with crisp pancetta and a soft egg center.",
    ),
    (
        "Greek Odyssey",
        "Feta, Kalamata Olives, Cucumber, Tomato",
        "A Greek salad-inspired pizza with feta cheese and kalamata olives.",
    ),
    (
        "Tex-Mex BBQ",
        "BBQ Sauce, Corn, Black Beans, Cheddar",
        "A fusion of BBQ and Tex-Mex, with sweet corn and black beans.",
    ),
    (
        "Roasted Beet Bliss",
        "Roasted Beets, Goat Cheese, Arugula, Walnuts",
        "Earthy roasted beets with tangy goat cheese and crunchy walnuts.",
    ),
    (
        "Apple Pie Surprise",
        "Sliced Apples, Cinnamon, Streusel Topping, Caramel Drizzle",
        "Dessert pizza with the classic flavors of apple pie, finished with caramel drizzle.",
    ),
]

PIZZAS: Dict[str, Pizza]
PIZZAS = {f"PZ{i}": Pizza(f"PZ{i}", *pz) for i, pz in enumerate(_menu, start=1)}

CHEESES = [
    "Blue",
    "Buffalo",
    "Cheddar",
    "Feta",
    "Gouda",
    "Mozzarella",
    "Parmesan",
    "Ricotta",
]

MEATS = ["BBQ", "Bacon", "Beef", "Ham", "Chicken", "Pepperoni", "Salami", "Tandoori"]


def user_login_possible(email: str, password: str) -> bool:
    """fake user login"""
    if email not in FAKE_USERS:
        return False
    if FAKE_USERS[email] != password:
        return False
    return True


def find_pizzas(search_text: str, max_results=10) -> List[Pizza]:
    """Search for pizzas by toppings.
       Also accept general search terms 'Meat' and 'Cheese' """
    def match_toppings(search_text: str, pizza_toppings: str) -> bool:
        """Hacky matching of pizzas"""
        pizza_toppings = pizza_toppings.lower()
        # adding cheese and meat for general search in a hacky way
        if any([c.lower() in pizza_toppings for c in CHEESES]):
            pizza_toppings += ", cheese"
        if any([m.lower() in pizza_toppings for m in MEATS]):
            pizza_toppings += ", meat"
        result = re.split(r"[^a-zA-Z]+", search_text.lower())
        return all([word in pizza_toppings for word in result if word])

    matched_pizzas = []

    if search_text:
        pizza: Pizza
        for pizza in PIZZAS.values():
            if match_toppings(search_text=search_text, pizza_toppings=pizza.toppings):
                matched_pizzas.append(pizza)
                if len(matched_pizzas) > max_results:
                    break
    return matched_pizzas
