class TurnManager:
    PHASE_ORDER = ["START_PHASE", "DRAW_PHASE",
                   "MAIN_PHASE", "COMBAT_PHASE", "END_PHASE"]

    def __init__(self, players):
        if not players:
            raise ValueError(
                "TurnManager must be initialized with at least one player.")
        self.players = players
        self.current_player_index = 0
        # Initialize to the first phase
        self.current_phase = self.PHASE_ORDER[0]

    def next_phase(self):
        current_index = self.PHASE_ORDER.index(self.current_phase)
        if current_index == len(self.PHASE_ORDER) - 1:
            self.end_turn()  # If at END_PHASE, end the turn
        else:
            # Move to next phase
            self.current_phase = self.PHASE_ORDER[current_index + 1]

    def end_turn(self):
        self.current_phase = self.PHASE_ORDER[0]  # Reset to START_PHASE
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)  # Next player

    def get_current_player(self):
        return self.players[self.current_player_index]

    def reset_phase(self):
        """Reset the phase to START_PHASE without ending the turn."""
        self.current_phase = self.PHASE_ORDER[0]

    def skip_to_phase(self, phase):
        """Skip directly to a specific phase, if valid."""
        if phase not in self.PHASE_ORDER:
            raise ValueError(f"Invalid phase: {phase}. Must be one of {
                             self.PHASE_ORDER}.")
        self.current_phase = phase
