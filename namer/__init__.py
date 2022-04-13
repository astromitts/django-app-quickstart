from namer.models import RandomName


def get_random_name(use_dash=True):
    rn = RandomName(use_dash)
    return rn.name
