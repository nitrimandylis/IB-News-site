TAG_COLOR_PALETTE = {
    '#AD': ('#51E87D', '#0F5B2D'),
    'BUSINESS': ('#33D9E8', '#0A4F5C'),
    'FOR THE STUDENT': ('#8B5CF6', '#FFFFFF'),
    'ARTS': ('#D4FF66', '#3D5C0F'),
    'OPINION': ('#FF33E8', '#FFFFFF'),
    'SPORTS': ('#D4FF33', '#5C6B0F'),
    'STUDENT LIFE': ('#66FF99', '#0F5C2D'),
    'STUDENT PROJECTS': ('#FF9933', '#5C2D0F'),
    'VOLUNTEERING-CAS': ('#66FF99', '#0F5C2D'),
}

DEFAULT_COLOR = ('#E0E0E0', '#000000') # Grey background, black text

TAG_CLASS_MAP = {
    '#AD': 'tag-ad',
    'BUSINESS': 'tag-business',
    'FOR THE STUDENT': 'tag-for-the-student',
    'ARTS': 'tag-arts',
    'OPINION': 'tag-opinion',
    'SPORTS': 'tag-sports',
    'STUDENT LIFE': 'tag-student-life',
    'STUDENT PROJECTS': 'tag-student-projects',
    'VOLUNTEERING-CAS': 'tag-volunteering-cas',
}

def get_background_color(tag_name):
    """
    Returns the background color for a given tag.
    """
    return TAG_COLOR_PALETTE.get(tag_name.upper(), DEFAULT_COLOR)[0]

def get_text_color(tag_name):
    """
    Returns the text color for a given tag.
    """
    return TAG_COLOR_PALETTE.get(tag_name.upper(), DEFAULT_COLOR)[1]

def get_tag_class(tag_name):
    """
    Takes a string (tag_name) and returns the corresponding CSS class from the map.
    """
    return TAG_CLASS_MAP.get(tag_name.upper(), 'tag-gray')