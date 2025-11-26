import hashlib

def get_hsl_color(tag_name):
    """
    Generates a unique, somewhat pleasant HSL color from a string.
    """
    hash_obj = hashlib.md5(tag_name.encode())
    hash_hex = hash_obj.hexdigest()
    hue = int(hash_hex[:8], 16) % 360
    saturation = int(hash_hex[8:16], 16) % 30 + 70  # 70-100% for vibrant colors
    lightness = int(hash_hex[16:24], 16) % 30 + 50 # 50-80% for good readability
    return (hue, saturation, lightness)

def get_background_color(tag_name):
    """
    Returns the HSL background color string for a tag.
    """
    hue, saturation, lightness = get_hsl_color(tag_name)
    return f'hsl({hue}, {saturation}%, {lightness}%)'

def get_text_color(tag_name):
    """
    Determines if the text on a given tag's color should be black or white.
    """
    hue, saturation, lightness = get_hsl_color(tag_name)
    # If lightness is high, use black text, otherwise use white.
    return '#000000' if lightness > 70 else '#FFFFFF'

TAG_COLOR_PALETTE = {
    'ad': ('#FFB300', '#000000'),
    'Arts': ('#0FD3FF', '#000000'),
    'Business': ('#80FF72', '#000000'),
    'For The Student': ('#FF6B6B', '#FFFFFF'),
    'Opinion': ('#00FFA3', '#000000'),
    'Sports': ('#FF5E00', '#FFFFFF'),
    'Student Life': ('#7A5CFF', '#FFFFFF'),
    'Student Projects': ('#00C2FF', '#000000'),
    'Volunteering-CAS': ('#FFA552', '#000000'),
    # Alternates
    'Science': ('#39FF14', '#000000'),
    'Editorial': ('#FF00A8', '#FFFFFF'),
    'Events': ('#FFD300', '#000000'),
    'Tech': ('#00F0FF', '#000000'),
    'Wellness': ('#FF3D7F', '#FFFFFF'),
}

TAG_CLASS_MAP = {
    '#ad': 'category-ad',
    'Arts': 'category-arts',
    'Business': 'category-business',
    'For The Student': 'category-student',
    'Opinion': 'category-opinion',
    'Sports': 'category-sports',
    'Student Life': 'category-life',
    'Student Projects': 'category-projects',
    'Volunteering-CAS': 'category-cas',
    'Science': 'category-science',
    'Editorial': 'category-editorial',
    'Events': 'category-events',
    'Tech': 'category-tech',
    'Wellness': 'category-wellness',
}

def get_tag_color(tag_name):
    """
    Takes a string (tag_name) and returns the corresponding color from the palette.
    """
    return TAG_COLOR_PALETTE.get(tag_name, ('#DDDDDD', '#000000'))[0]

def get_text_color_for_tag(tag_name):
    """
    Takes a string (tag_name) and returns the corresponding text color from the palette.
    """
    return TAG_COLOR_PALETTE.get(tag_name, ('#DDDDDD', '#000000'))[1]

def get_tag_class(tag_name):
    """
    Takes a string (tag_name) and returns the corresponding CSS class from the map.
    """
    return TAG_CLASS_MAP.get(tag_name, 'tag-gray')