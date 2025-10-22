"""
UI Constants and Configuration
Centralizes colors, fonts, spacing, and other UI parameters.
"""

# Color Palette (Halloween theme with consistency)
COLORS = {
    # Primary colors
    "bg_dark": "#1a1a2e",
    "bg_medium": "#2d2d44",
    "bg_light": "#3d3d5c",
    
    # Text colors
    "text_primary": "#ffffff",
    "text_secondary": "#b8b8d0",
    "text_muted": "#808080",
    
    # Status colors
    "success": "#4CAF50",      # Green
    "warning": "#FF9800",      # Orange
    "error": "#f44336",        # Red
    "info": "#2196F3",         # Blue
    "energy": "#9C27B0",       # Purple
    "shield": "#00BCD4",       # Cyan
    
    # Combat colors
    "fight_bg": "#ffcccc",
    "flee_bg": "#ccffcc",
    "outwit_bg": "#ffffcc",
    
    # Ability colors
    "spectral_bg": "#e6ccff",
    "shield_bg": "#cce6ff",
    "hint_bg": "#ffffcc",
    
    # UI element colors
    "button_bg": "#e0e0e0",
    "button_active": "#c0c0c0",
    "disabled": "#cccccc",
}

# Typography
FONTS = {
    "title": ("Arial", 16, "bold"),
    "heading": ("Arial", 14, "bold"),
    "body": ("Arial", 11),
    "body_bold": ("Arial", 11, "bold"),
    "small": ("Arial", 9),
    "monospace": ("Courier New", 10),
}

# Spacing (consistent padding/margins)
SPACING = {
    "xs": 2,
    "sm": 5,
    "md": 10,
    "lg": 15,
    "xl": 20,
}

# Window dimensions
WINDOW = {
    "min_width": 600,
    "min_height": 700,
    "title": "Haunted House Adventure",
}

# Button sizes
BUTTON = {
    "standard_width": 12,
    "wide_width": 20,
    "combat_width": 45,
    "combat_height": 4,
}

# Icons (emoji with proper spacing)
ICONS = {
    "bone": "🦴",
    "energy": "⚡",
    "shield": "🛡️",
    "heart": "❤️",
    "skull": "💀",
    
    # Combat
    "fight": "⚔️",
    "flee": "🏃",
    "outwit": "🧠",
    "monster": "👻",
    
    # Abilities
    "spectral": "🔍",
    "mystic": "🔮",
    
    # Status
    "success": "✅",
    "failure": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    
    # Progress
    "star": "⭐",
    "trophy": "🏆",
    "fire": "🔥",
}

# Difficulty settings
DIFFICULTY = {
    "easy": {
        "name": "Easy",
        "fight_chance": 0.70,
        "flee_chance": 0.90,
        "bone_find_base": 0.50,
        "bone_find_boosted": 0.60,
        "description": "More forgiving combat and exploration",
    },
    "normal": {
        "name": "Normal",
        "fight_chance": 0.60,
        "flee_chance": 0.80,
        "bone_find_base": 0.40,
        "bone_find_boosted": 0.50,
        "description": "Balanced gameplay experience",
    },
    "hard": {
        "name": "Hard",
        "fight_chance": 0.50,
        "flee_chance": 0.70,
        "bone_find_base": 0.30,
        "bone_find_boosted": 0.40,
        "description": "Challenging encounters and scarce bones",
    }
}

# Default difficulty
DEFAULT_DIFFICULTY = "normal"
