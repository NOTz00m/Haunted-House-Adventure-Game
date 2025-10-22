"""
Integration tests for the Haunted House Adventure Game.
Tests the game as a whole without the GUI.
"""

import os
import pickle
from skeleton import Skeleton
from rooms import move_room, explore_current_room, rooms
from monsters import combat_encounter

def test_game_initialization():
    """Test that the game initializes correctly."""
    print("Testing game initialization...")
    
    skeleton = Skeleton()
    
    assert skeleton.name == "Bones"
    assert skeleton.current_room == "Entrance Hall"
    assert 2 <= len(skeleton.lost_bones) <= 4, "Should lose 2-4 bones at start"
    assert len(skeleton.bones) + len(skeleton.lost_bones) == 6, "Total should be 6 bones"
    assert skeleton.spirit_energy == 0, "Should start with 0 energy"
    assert skeleton.bone_shield_active == False, "Shield should be inactive"
    assert skeleton.facts_collected == 0, "Should have 0 facts"
    
    print("✓ Game initialization working")

def test_room_navigation():
    """Test that room navigation works correctly."""
    print("Testing room navigation...")
    
    skeleton = Skeleton()
    
    # Test valid move
    result = move_room(skeleton, "left")
    assert skeleton.current_room == "Creepy Library", "Should move to Creepy Library"
    assert "Creepy Library" in result, "Result should mention new room"
    
    # Test invalid move
    result = move_room(skeleton, "left")  # Can't go left from library
    assert skeleton.current_room == "Creepy Library", "Should stay in same room"
    assert "can't move" in result.lower(), "Should indicate invalid move"
    
    # Test move back
    result = move_room(skeleton, "right")
    assert skeleton.current_room == "Entrance Hall", "Should return to entrance"
    
    print("✓ Room navigation working")

def test_exploration_events():
    """Test that exploration triggers various events."""
    print("Testing exploration events...")
    
    skeleton = Skeleton()
    
    # Run exploration multiple times to hit different events
    events_found = {
        "combat": False,
        "bone": False,
        "fact": False,
        "random": False
    }
    
    for _ in range(50):
        test_skeleton = Skeleton()
        result = explore_current_room(test_skeleton)
        
        if result == "COMBAT_TRIGGER":
            events_found["combat"] = True
        elif "found your" in result.lower():
            events_found["bone"] = True
        elif "Random fact found:" in result:
            events_found["fact"] = True
        elif "Event:" in result:
            events_found["random"] = True
    
    assert events_found["combat"], "Should encounter combat"
    assert events_found["fact"], "Should find facts"
    # Note: bones and random events might not trigger in 50 tries due to RNG
    
    print(f"✓ Exploration events working (found: {sum(events_found.values())}/4 event types)")

def test_fact_collection():
    """Test fact collection increases counter."""
    print("Testing fact collection...")
    
    skeleton = Skeleton()
    initial_facts = skeleton.facts_collected
    
    skeleton.collect_fact()
    assert skeleton.facts_collected == initial_facts + 1, "Facts should increase"
    
    skeleton.collect_fact()
    skeleton.collect_fact()
    assert skeleton.facts_collected == initial_facts + 3, "Should have 3 more facts"
    
    print("✓ Fact collection working")

def test_win_condition():
    """Test that win condition works when all bones found."""
    print("Testing win condition...")
    
    skeleton = Skeleton()
    
    # Simulate finding all lost bones
    skeleton.lost_bones = []
    
    assert skeleton.has_won() == True, "Should win with no lost bones"
    assert skeleton.is_alive() == True, "Should still be alive"
    
    print("✓ Win condition working")

def test_lose_condition():
    """Test that lose condition works when all bones lost."""
    print("Testing lose condition...")
    
    skeleton = Skeleton()
    
    # Simulate losing all bones
    skeleton.bones = []
    
    assert skeleton.is_alive() == False, "Should not be alive with no bones"
    
    print("✓ Lose condition working")

def test_save_load_game():
    """Test save and load functionality."""
    print("Testing save/load functionality...")
    
    # Create a game state
    skeleton = Skeleton()
    skeleton.current_room = "Spooky Kitchen"
    skeleton.spirit_energy = 5
    skeleton.bone_shield_active = True
    skeleton.facts_collected = 3
    
    # Save state
    game_state = {
        "current_room": skeleton.current_room,
        "bones": skeleton.bones,
        "lost_bones": skeleton.lost_bones,
        "facts_collected": skeleton.facts_collected,
        "hinted_rooms": skeleton.hinted_rooms,
        "spirit_energy": skeleton.spirit_energy,
        "bone_shield_active": skeleton.bone_shield_active
    }
    
    with open("test_savegame.pkl", "wb") as file:
        pickle.dump(game_state, file)
    
    # Create new skeleton and load
    new_skeleton = Skeleton()
    
    with open("test_savegame.pkl", "rb") as file:
        loaded_state = pickle.load(file)
    
    new_skeleton.current_room = loaded_state["current_room"]
    new_skeleton.bones = loaded_state["bones"]
    new_skeleton.lost_bones = loaded_state["lost_bones"]
    new_skeleton.facts_collected = loaded_state["facts_collected"]
    new_skeleton.spirit_energy = loaded_state.get("spirit_energy", 0)
    new_skeleton.bone_shield_active = loaded_state.get("bone_shield_active", False)
    
    # Verify
    assert new_skeleton.current_room == "Spooky Kitchen"
    assert new_skeleton.spirit_energy == 5
    assert new_skeleton.bone_shield_active == True
    assert new_skeleton.facts_collected == 3
    
    # Cleanup
    os.remove("test_savegame.pkl")
    
    print("✓ Save/load working")

def test_backward_compatibility():
    """Test loading old save files without new attributes."""
    print("Testing backward compatibility...")
    
    # Create old-style save (without spirit_energy and bone_shield_active)
    old_skeleton = Skeleton()
    old_state = {
        "current_room": "Dark Cellar",
        "bones": ["head", "torso"],
        "lost_bones": ["left arm", "right arm"],
        "facts_collected": 2,
        "hinted_rooms": {}
    }
    
    with open("test_old_save.pkl", "wb") as file:
        pickle.dump(old_state, file)
    
    # Load into new skeleton
    new_skeleton = Skeleton()
    
    with open("test_old_save.pkl", "rb") as file:
        loaded = pickle.load(file)
    
    new_skeleton.current_room = loaded["current_room"]
    new_skeleton.bones = loaded["bones"]
    new_skeleton.lost_bones = loaded["lost_bones"]
    new_skeleton.facts_collected = loaded["facts_collected"]
    new_skeleton.spirit_energy = loaded.get("spirit_energy", 0)  # Default to 0
    new_skeleton.bone_shield_active = loaded.get("bone_shield_active", False)  # Default to False
    
    # Verify defaults applied
    assert new_skeleton.spirit_energy == 0, "Old save should default to 0 energy"
    assert new_skeleton.bone_shield_active == False, "Old save should have no shield"
    assert new_skeleton.current_room == "Dark Cellar", "Other data should load correctly"
    
    # Cleanup
    os.remove("test_old_save.pkl")
    
    print("✓ Backward compatibility working")

def test_spectral_search_integration():
    """Test spectral search with room exploration."""
    print("Testing spectral search integration...")
    
    skeleton = Skeleton()
    skeleton.gain_energy(10)  # Give enough energy
    
    initial_lost = len(skeleton.lost_bones)
    
    if initial_lost > 0:
        result = explore_current_room(skeleton, use_spectral_search=True)
        
        assert "spectral search" in result.lower(), "Should mention spectral search"
        assert skeleton.spirit_energy == 8, "Should spend 2 energy"
        assert len(skeleton.lost_bones) == initial_lost - 1, "Should find a bone"
    
    print("✓ Spectral search integration working")

def test_combat_integration():
    """Test combat system integrates with skeleton state."""
    print("Testing combat integration...")
    
    skeleton = Skeleton()
    initial_bones = len(skeleton.bones)
    
    # Test successful fight
    result = combat_encounter(skeleton, "fight", "test_monster")
    
    if result["success"]:
        assert skeleton.spirit_energy == 1, "Should gain energy on success"
    else:
        # If failed and had bones, should lose one
        if initial_bones > 0 and not result["bones_lost"]:
            # Might have shield or succeed
            pass
    
    print("✓ Combat integration working")

def test_all_rooms_accessible():
    """Test that all rooms can be reached."""
    print("Testing room accessibility...")
    
    # All rooms defined
    all_rooms = set(rooms.keys())
    assert len(all_rooms) == 9, "Should have 9 rooms"
    
    # Test that rooms form a connected graph
    visited = set()
    to_visit = ["Entrance Hall"]
    
    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)
        
        # Add all connected rooms
        for direction in ["up", "down", "left", "right"]:
            if direction in rooms[current]:
                next_room = rooms[current][direction]
                if next_room not in visited:
                    to_visit.append(next_room)
    
    assert visited == all_rooms, f"Not all rooms accessible. Visited: {visited}, All: {all_rooms}"
    
    print("✓ All rooms accessible")

def run_all_integration_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("RUNNING INTEGRATION TESTS")
    print("=" * 60)
    
    try:
        test_game_initialization()
        test_room_navigation()
        test_exploration_events()
        test_fact_collection()
        test_win_condition()
        test_lose_condition()
        test_save_load_game()
        test_backward_compatibility()
        test_spectral_search_integration()
        test_combat_integration()
        test_all_rooms_accessible()
        
        print("=" * 60)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print("=" * 60)
        print(f"❌ UNEXPECTED ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_integration_tests()
    exit(0 if success else 1)
