import time
import random
from typing import List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventArgs:
    """Base class for event arguments"""
    pass


class Event:
    """Class equivalent to C#'s event"""
    
    def __init__(self):
        self._handlers: List[Callable] = []
    
    def add_handler(self, handler: Callable):
        """Add event handler"""
        if handler not in self._handlers:
            self._handlers.append(handler)
    
    def remove_handler(self, handler: Callable):
        """Remove event handler"""
        if handler in self._handlers:
            self._handlers.remove(handler)
    
    def invoke(self, sender, args: EventArgs = None):
        """Fire event"""
        for handler in self._handlers:
            handler(sender, args or EventArgs())


@dataclass
class KitchenObjectSO:
    """Kitchen object data class"""
    name: str
    object_id: int


@dataclass
class RecipeSO:
    """Recipe data class"""
    name: str
    kitchen_object_so_list: List[KitchenObjectSO] = field(default_factory=list)


@dataclass
class RecipeListSO:
    """Recipe list data class"""
    recipe_so_list: List[RecipeSO] = field(default_factory=list)


class PlateKitchenObject:
    """Plate kitchen object"""
    
    def __init__(self):
        self._kitchen_object_so_list: List[KitchenObjectSO] = []
    
    def add_kitchen_object(self, kitchen_object: KitchenObjectSO):
        """Add kitchen object"""
        self._kitchen_object_so_list.append(kitchen_object)
    
    def get_kitchen_object_so_list(self) -> List[KitchenObjectSO]:
        """Get kitchen object list"""
        return self._kitchen_object_so_list.copy()


class KitchenGameManager:
    """Kitchen game manager (Singleton)"""
    
    _instance: Optional['KitchenGameManager'] = None
    
    def __init__(self):
        self._is_game_playing = False
    
    @classmethod
    def get_instance(cls) -> 'KitchenGameManager':
        """Get Singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def is_game_playing(self) -> bool:
        """Check if game is in progress"""
        return self._is_game_playing
    
    def start_game(self):
        """Start game"""
        self._is_game_playing = True
    
    def stop_game(self):
        """Stop game"""
        self._is_game_playing = False


class DeliveryManager:
    """
    Delivery management class (Python version)
    Handles recipe delivery logic, event management, and game state.
    Thread-safe singleton, configurable, and testable.
    """

    # Configurable constants
    DEFAULT_SPAWN_RECIPE_INTERVAL = 4.0
    DEFAULT_MAX_WAITING_RECIPES = 4

    _instance: Optional['DeliveryManager'] = None
    _lock = __import__('threading').Lock()

    def __init__(self, recipe_list_so: RecipeListSO, spawn_recipe_interval=None, max_waiting_recipes=None):
        """
        Initialize DeliveryManager.
        Args:
            recipe_list_so (RecipeListSO): List of available recipes.
            spawn_recipe_interval (float, optional): Interval for spawning recipes.
            max_waiting_recipes (int, optional): Max number of waiting recipes.
        """
        if not isinstance(recipe_list_so, RecipeListSO):
            raise ValueError("recipe_list_so must be a RecipeListSO instance")
        self._recipe_list_so = recipe_list_so
        self._spawn_recipe_interval = spawn_recipe_interval or self.DEFAULT_SPAWN_RECIPE_INTERVAL
        self._max_waiting_recipes = max_waiting_recipes or self.DEFAULT_MAX_WAITING_RECIPES
        self._waiting_recipe_so_list: List[RecipeSO] = []
        self._spawn_recipe_timer = self._spawn_recipe_interval
        self._successful_recipes_amount = 0
        self._last_update_time = time.time()
        # Events
        self.on_recipe_spawned = Event()
        self.on_recipe_completed = Event()
        self.on_recipe_success = Event()
        self.on_recipe_failed = Event()

    @classmethod
    def get_instance(cls, recipe_list_so=None, spawn_recipe_interval=None, max_waiting_recipes=None, reset=False):
        """
        Thread-safe singleton getter. Allows reset for testing.
        """
        with cls._lock:
            if reset or cls._instance is None:
                if recipe_list_so is None:
                    raise ValueError("recipe_list_so must be provided for first initialization or reset")
                cls._instance = cls(recipe_list_so, spawn_recipe_interval, max_waiting_recipes)
            return cls._instance

    def reset_instance(self):
        """Reset singleton instance (for testing)."""
        type(self)._instance = None

    def _ingredients_match(self, plate_ingredients, recipe_ingredients):
        """
        Helper to check if plate ingredients match recipe ingredients.
        Uses collections.Counter for order-insensitive comparison.
        """
        from collections import Counter
        return Counter(plate_ingredients) == Counter(recipe_ingredients)

    def update(self):
        """
        Update the delivery manager state, spawn recipes if needed.
        """
        import time
        now = time.time()
        elapsed = now - self._last_update_time
        self._last_update_time = now
        if not KitchenGameManager.get_instance().is_game_playing():
            return
        self._spawn_recipe_timer -= elapsed
        if self._spawn_recipe_timer <= 0:
            self._spawn_recipe_timer = self._spawn_recipe_interval
            if len(self._waiting_recipe_so_list) < self._max_waiting_recipes:
                import random
                if not self._recipe_list_so.recipe_so_list:
                    # Error: No recipes available
                    self.on_recipe_failed.invoke(self, EventArgs())
                    return
                recipe_so = random.choice(self._recipe_list_so.recipe_so_list)
                self._waiting_recipe_so_list.append(recipe_so)
                self.on_recipe_spawned.invoke(self, EventArgs())

    def deliver_recipe(self, plate_kitchen_object: PlateKitchenObject):
        """
        Check if plate matches any waiting recipe by ingredients.
        Args:
            plate_kitchen_object (PlateKitchenObject): Plate to check.
        """
        # Input validation
        if not isinstance(plate_kitchen_object, PlateKitchenObject):
            raise ValueError("plate_kitchen_object must be a PlateKitchenObject instance")
        plate_ingredients = plate_kitchen_object.get_kitchen_object_so_list()
        if not isinstance(plate_ingredients, list) or not plate_ingredients:
            # Error handling: empty or invalid plate
            self.on_recipe_failed.invoke(self, EventArgs())
            return

        for i, waiting_recipe_so in enumerate(self._waiting_recipe_so_list):
            recipe_ingredients = getattr(waiting_recipe_so, 'kitchen_object_so_list', None)
            if not isinstance(recipe_ingredients, list) or not recipe_ingredients:
                continue  # Skip invalid or empty recipes

            if self._ingredients_match(plate_ingredients, recipe_ingredients):
                self._successful_recipes_amount += 1
                self._waiting_recipe_so_list.pop(i)
                self.on_recipe_completed.invoke(self, EventArgs())
                self.on_recipe_success.invoke(self, EventArgs())
                return  # Early return on success

        # No matching recipe found
        self.on_recipe_failed.invoke(self, EventArgs())

    def get_waiting_recipe_so_list(self) -> List['RecipeSO']:
        """Return current waiting recipes."""
        return self._waiting_recipe_so_list.copy()

    def get_successful_recipes_amount(self) -> int:
        """Return the count of successful deliveries."""
        return self._successful_recipes_amount


# Usage example
if __name__ == "__main__":
    # Create sample data
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    
    # Sample recipes
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad", [lettuce, tomato])
    
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])
    
    # Initialize game manager and delivery manager
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    
    # Set up event handlers
    def on_recipe_spawned(sender, args):
        print("New recipe has been generated!")
    
    def on_recipe_success(sender, args):
        print("Recipe delivery successful!")
    
    def on_recipe_failed(sender, args):
        print("Recipe delivery failed...")
    
    delivery_manager.on_recipe_spawned.add_handler(on_recipe_spawned)
    delivery_manager.on_recipe_success.add_handler(on_recipe_success)
    delivery_manager.on_recipe_failed.add_handler(on_recipe_failed)
    
    # Sample execution
    print("Game starting...")
    
    # Run update process for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        delivery_manager.update()
        time.sleep(0.1)  # Update every 100ms
    
    print(f"Number of waiting recipes: {len(delivery_manager.get_waiting_recipe_so_list())}")
    
    # Sample delivery test
    plate = PlateKitchenObject()
    plate.add_kitchen_object(bread)
    plate.add_kitchen_object(lettuce)
    plate.add_kitchen_object(tomato)
    
    print("Delivering sandwich...")
    delivery_manager.deliver_recipe(plate)
    
    print(f"Number of successful recipes: {delivery_manager.get_successful_recipes_amount()}")
