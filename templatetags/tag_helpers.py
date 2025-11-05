# templatetags/tag_helpers.py

import hashlib


# 🎨 You can customize this list with your own accessible hex color codes.
# I've chosen a set of 12 distinct, modern colors.
TAG_COLOR_PALETTE = [
    '#FF6B6B',  # Coral Red
    '#FFD166',  # Golden Yellow
    '#06D6A0',  # Mint Green
    '#118AB2',  # Ocean Blue
    '#073B4C',  # Deep Navy
    '#E07A5F',  # Peach
    '#3D405B',  # Slate Gray
    '#81B29A',  # Sage Green
    '#F2CC8F',  # Cream
    '#F4A261',  # Orange
    '#E76F51',  # Terracotta
    '#2A9D8F',  # Teal
]

def hash_to_color(tag_name):
    """
    Takes a string (tag_name) and deterministically picks a color 
    from the TAG_COLOR_PALETTE based on its hash.
    """
    if not tag_name:
        return '#DDDDDD'  # Default color for empty tags
    
    # Hash the tag name to get a consistent integer
    hash_obj = hashlib.md5(tag_name.encode('utf-8'))
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # Use modulo to pick a color from the palette
    color_index = hash_int % len(TAG_COLOR_PALETTE)
    
    return TAG_COLOR_PALETTE[color_index]

def get_text_color(bg_hex):
    """
    Takes a background hex color and returns either '#000000' (black) 
    or '#FFFFFF' (white) for the best text contrast.
    """
    if not bg_hex:
        return '#000000'
    
    # Remove '#' if present
    hex_color = bg_hex.lstrip('#')
    
    # Convert hex to RGB
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        return '#000000'  # Default to black on error
    
    # Calculate luminance (W3C recommended formula)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # Return black or white depending on luminance
    if luminance > 0.5:
        return '#000000'  # Use black text on light backgrounds
    else:
        return '#FFFFFF'  # Use white text on dark backgrounds
