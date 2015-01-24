# -*- coding: utf-8 -*-
import unittest
from UIUtility.CharacterSelector import *


class CharacterSelectorTest(unittest.TestCase):
    def test_getter_and_setter(self):
        character_selector = CharacterSelectorCanvas(None)
        assert character_selector.get() is None

        character = DBAccessor.select_character_by_specific_column('ID', 5002)
        self.assertRaises(TypeError, character_selector.set, character.info_list)

        character_selector.set(character)
        assert character_selector.get().nickname == u'聖女'
