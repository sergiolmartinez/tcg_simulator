class ActionProcessor:
    def __init__(self, game_state):
        self.game_state = game_state

    def process_action(self, player, action):
        if not self.validate_action(player, action):
            raise Exception(f"Invalid action: {action}")

        self.resolve_action(player, action)

    def validate_action(self, player, action):
        phase = self.game_state.turn_manager.current_phase

        if phase not in action["allowed_phases"]:
            print(f"Action not allowed in phase: {phase}")
            return False

        if action["type"] == "PlayCard":
            card = action["card"]
            if card not in player["hand"]:
                print(f"{card.name} is not in {player['name']}'s hand.")
                return False
            if player["mana"] < card.mana_cost:
                print(
                    f"{player['name']} does not have enough mana to play {
                        card.name} "
                    f"(Cost: {card.mana_cost}, Available: {player['mana']})."
                )
                return False

        return True

    def resolve_action(self, player, action):
        action_type = action["type"]

        if action_type == "Attack":
            self._resolve_attack(player, action)
        elif action_type == "Defend":
            self._resolve_defend(player, action)
        elif action_type == "DrawCard":
            self._resolve_draw_card(player)
        elif action_type == "PlayCard":
            self._resolve_play_card(player, action["card"])
        elif action_type == "TapCard":
            action["card"].tap()
        elif action_type == "UntapCard":
            action["card"].untap()
        elif action_type == "DiscardCard":
            self._resolve_discard_card(player, action["card"])
        elif action_type == "EndTurn":
            self.game_state.turn_manager.end_turn()

    def _resolve_attack(self, player, action):
        attacker = action["attacker"]
        target = action["target"]
        print(f"{player['name']}'s {attacker.name} attacks {target.name}!")
        destroyed = target.take_damage(attacker.attack)
        if destroyed:
            opponent = action["opponent"]
            if target in opponent["board"]:
                opponent["board"].remove(target)
            elif target in player["board"]:  # Self-damaging effects
                player["board"].remove(target)

    def _resolve_defend(self, player, action):
        defender = action["defender"]
        attacker = action["attacker"]
        print(f"{player['name']}'s {
              defender.name} defends against {attacker.name}!")
        # Swap damage between cards
        defender_destroyed = defender.take_damage(attacker.attack)
        attacker_destroyed = attacker.take_damage(defender.attack)
        if defender_destroyed:
            player["board"].remove(defender)
        if attacker_destroyed:
            action["opponent"]["board"].remove(attacker)

    def _resolve_draw_card(self, player):
        card = player["deck"].draw_card()
        player["hand"].append(card)
        print(f"{player['name']} drew {card.name}")

    def _resolve_play_card(self, player, card):
        player["mana"] -= card.mana_cost
        player["hand"].remove(card)
        player["board"].append(card)
        print(
            f"{player['name']} played {card.name} "
            f"(Cost: {card.mana_cost}, Remaining Mana: {player['mana']})"
        )
        if card.ability:
            card.activate_ability(player, self.game_state)

    def _resolve_discard_card(self, player, card):
        if card in player["board"]:
            player["board"].remove(card)
        elif card in player["hand"]:
            player["hand"].remove(card)
        else:
            raise Exception(
                f"Card {card.name} not found in {
                    player['name']}'s hand or board!"
            )
        player["graveyard"].append(card)
        print(f"{player['name']} discarded {card.name}")
