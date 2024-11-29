import sys
import os

# Add tcg_simulator root to PYTHONPATH before importing local modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_state import GameState
from action_processor import ActionProcessor

def test_turn_phases():
    # Initialize players and game state
    players = [{"name": "Player 1"}, {"name": "Player 2"}]
    game_state = GameState(players)
    action_processor = ActionProcessor(game_state)

    # Test phase transitions
    assert game_state.turn_manager.current_phase == "START_PHASE", "Initial phase should be START_PHASE"
    game_state.turn_manager.next_phase()
    assert game_state.turn_manager.current_phase == "DRAW_PHASE", "Next phase should be DRAW_PHASE"
    game_state.turn_manager.next_phase()
    assert game_state.turn_manager.current_phase == "MAIN_PHASE", "Next phase should be MAIN_PHASE"

    # Test cycling back to the first phase after a full turn
    game_state.turn_manager.next_phase()  # COMBAT_PHASE
    game_state.turn_manager.next_phase()  # END_PHASE
    game_state.turn_manager.next_phase()  # Back to START_PHASE
    assert game_state.turn_manager.current_phase == "START_PHASE", "Phase should reset to START_PHASE after a full turn"
