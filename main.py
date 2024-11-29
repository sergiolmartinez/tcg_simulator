from game_state import GameState
from action_processor import ActionProcessor


def main():
    players = [
        {"name": "Player 1", "mana": 5, "health": 20},
        {"name": "Player 2", "mana": 5, "health": 20},
    ]

    game_state = GameState(players)
    action_processor = ActionProcessor(game_state)

    for _ in range(6):  # Simulate turns
        player = game_state.turn_manager.get_current_player()
        phase = game_state.turn_manager.current_phase

        print(f"\n{player['name']}'s turn - Phase: {phase}")
        print(f"Health: {player['health']}, Mana: {
              player['mana']}/{player['max_mana']}")
        print(f"Deck: {[card.name for card in player['deck'].cards]}")
        print(f"Hand: {[card.name for card in player['hand']]}")
        print(f"Board: {[card.name for card in player['board']]}")

        if phase == "START_PHASE":
            player["max_mana"] = min(player["max_mana"] + 1, 10)
            player["mana"] = player["max_mana"]
            print(f"{player['name']} regenerated mana: {
                  player['mana']}/{player['max_mana']}")
        elif phase == "DRAW_PHASE" and player["deck"].cards:
            action_processor.process_action(
                player, {"type": "DrawCard", "allowed_phases": ["DRAW_PHASE"]})
        elif phase == "MAIN_PHASE" and player["hand"]:
            action_processor.process_action(player, {
                                            "type": "PlayCard", "card": player["hand"][0], "allowed_phases": ["MAIN_PHASE"]})
        elif phase == "COMBAT_PHASE":
            if player["board"]:
                attacker = player["board"][0]
                opponent = game_state.turn_manager.players[1 -
                                                           game_state.turn_manager.current_player_index]
                if opponent["board"]:
                    # Attack the first card on the opponent's board
                    target = opponent["board"][0]
                    action_processor.process_action(player, {
                        "type": "Attack",
                        "attacker": attacker,
                        "target": target,
                        "opponent": opponent
                    })
                else:
                    # Attack the opponent directly
                    print(f"{player['name']}'s {attacker.name} attacks {
                          opponent['name']} directly!")
                    opponent["health"] -= attacker.attack
                    print(f"{opponent['name']}'s health is now {
                          opponent['health']}.")
        elif phase == "END_PHASE" and player["board"]:
            action_processor.process_action(
                player, {"type": "EndTurn", "allowed_phases": ["END_PHASE"]})

        game_state.turn_manager.next_phase()


if __name__ == "__main__":
    main()
