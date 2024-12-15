zoom_options = {
    'Input_interface': {
        'android': {
            'width': [0.6, 0.95]
        },
        'windows': {
            'width': [0.6, 0.95]
        }
    },
    'ListCards_interface': {
        'android': {
            'width': [0.6, 0.95],
            'height': [0.81, 0.81]
        },
        'windows': {
            'width': [0.6, 0.95],
            'height': [0.81, 0.81]
        }
    },
    'Search_interface': {
        'android': {
            'width': [0.6, 0.95],
            'height': [0.8, 0.8]
        },
        'windows': {
            'width': [0.6, 0.95],
            'height': [0.8, 0.8]
        }
    },
    'Edit_interface': {
        'android': {
            'width': [0.6, 0.95]
        },
        'windows': {
            'width': [0.6, 0.95]
        }
    },
}


def get_option(*args):
    r_data = ''
    buffer = zoom_options

    for item in args:
        buffer = buffer[item]

    r_data = buffer

    return r_data


