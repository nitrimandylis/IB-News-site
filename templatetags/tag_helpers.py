TAG_CLASS_MAP = {
    '#AD': 'tag-ad',
    'BUSINESS': 'tag-business',
    'FOR THE STUDENT': 'tag-for-student',
    'ARTS': 'tag-arts',
    'OPINION': 'tag-opinion',
    'SPORTS': 'tag-sports',
    'STUDENT LIFE': 'tag-student-life',
    'STUDENT PROJECTS': 'tag-student-projects',
    'VOLUNTEERING-CAS': 'tag-volunteering-cas',
}

def get_tag_class(tag_name):
    """
    Takes a string (tag_name) and returns the corresponding CSS class from the map.
    """
    return TAG_CLASS_MAP.get(tag_name.upper(), 'tag-gray')
