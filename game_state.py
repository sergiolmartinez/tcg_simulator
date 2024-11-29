from turn_manager import TurnManager
import random

# Example abilities


def heal_player(player, game_state):
    print(f"{player['name']} heals for 3 health!")
    player["health"] = player.get("health", 20) + 3  # Default health is 20
    print(f"{player['name']}'s health is now {player['health']}.")


def deal_damage(player, game_state):
    opponent = game_state.turn_manager.players[1 -
                                               game_state.turn_manager.current_player_index]
    print(f"{player['name']} deals 3 damage to {opponent['name']}!")
    opponent["health"] = opponent.get("health", 20) - 3
    print(f"{opponent['name']}'s health is now {opponent['health']}.")


def generate_mana(player, game_state):
    print(f"{player['name']} generates 1 extra mana!")
    player["mana"] += 1
    print(f"{player['name']}'s mana is now {
          player['mana']}/{player['max_mana']}.")

# Class definitions


class Card:
    def __init__(self, name, mana_cost=0, ability=None, attack=0, health=0):
        self.name = name
        self.mana_cost = mana_cost  # Fixed typo
        self.state = "active"  # Possible states: "active", "tapped", "exhausted"
        self.ability = ability
        self.attack = attack  # Damage this card deals
        self.health = health  # Health of the card

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {
              damage} damage. Remaining health: {self.health}")
        if self.health <= 0:
            print(f"{self.name} is destroyed!")
            return True  # Indicates the card is destroyed
        return False

    def activate_ability(self, player, game_state):
        if self.ability:
            print(f"Activating {self.name}'s ability!")
            self.ability(player, game_state)  # Execute the ability logic

    def tap(self):
        if self.state == "active":
            self.state = "tapped"
            print(f"{self.name} is now tapped.")
        else:
            raise Exception(f"Cannot tap {self.name}; it is {self.state}.")

    def untap(self):
        if self.state == "tapped":
            self.state = "active"
            print(f"{self.name} is now untapped.")
        else:
            raise Exception(f"Cannot untap {self.name}; it is {self.state}.")


class Deck:
    def __init__(self, card_definitions):
        # Create Card objects with name, mana_cost, ability, attack, and health
        self.cards = [Card(name, mana_cost, ability, attack, health)
                      for name, mana_cost, ability, attack, health in card_definitions]

    def draw_card(self):
        if not self.cards:
            raise Exception("Deck is empty!")
        return self.cards.pop()  # Remove and return the top card


class GameState:
    def __init__(self, players):
        self.players = players
        self.turn_manager = TurnManager(players)
        for player in players:
            # Independent deck for each player
            deck_definitions = [
                # Spell with attack (direct damage)
                ("Fireball", 3, deal_damage, 5, 0),
                ("Shield", 2, None, 0, 5),           # Defensive card
                ("Lightning Bolt", 4, deal_damage, 6, 0),  # High attack spell
                # Healing card with health
                ("Healing Potion", 1, heal_player, 0, 3)
            ]
            player["deck"] = Deck(deck_definitions)
            player["hand"] = []
            player["board"] = []
            player["graveyard"] = []
            player["mana"] = 0          # Current mana available
            player["max_mana"] = 0      # Maximum mana capacity
