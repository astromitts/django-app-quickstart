from namer import words
import random


class RandomName(object):
    def __init__(self, use_dash=True, animals_only=False, edited_adjectives=True):
        if animals_only:
            self.noun_source = words.animals
        else:
            self.noun_source = words.animals + words.nouns

        if not edited_adjectives:
            self.adjective_source = words.adjectives
        else:
            self.adjective_source = words.edited_adjectives
        self.use_dash = use_dash
        self.name = self.get_name()

    def get_name(self):
        if self.use_dash:
            self.name = '{}-{}'.format(self.adjective(), self.noun())
        else:
            self.name = '{}{}'.format(self.adjective(), self.noun())
        return self.name

    def adjective(self):
        return random.choice(self.adjective_source)

    def noun(self):
        return random.choice(self.noun_source)
