import json
import os
import re
from pprint import pprint

import untangle

from wolcen.encoder import ComplexEncoder
from wolcen.models.ring import Ring
from wolcen.models.skill import Skill


def translate_ui_string(source: dict, key: str) -> str:
    """
    For a given source, obtain the translation value for the given key
    :param source: dictionary to obtain translation from
    :param key: key, starting with `@...`, this will be stripped internally for the lookup
    :return: value if exists else None
    """
    return source.get(key[1:], None)


def parse_effect(effect: untangle.Element):
    """
    Parse "effects" of nodes, replace placeholders with values
    :param effect: xml untangle element
    :return: combined string describing the node
    """
    text = translate_ui_string(effect_translator, effect['HUDDesc'])
    # find another way to just get any attributes from untangle...
    kv = effect.Semantics._attributes

    if text is None:
        return

    for i in range(len(kv)):
        attr_name = list(kv)[i]
        value_str = list(kv.values())[i]
        if 'percent' in attr_name.lower():
            value_str += '%'
        text = text.replace(f'%{i + 1}', value_str)
    return text


def parse_skill(skill: untangle.Element, tree_nodes_data: untangle.Element):
    """
    Parse a node (skill) in the passive tree
    :param skill: raw xml of the element
    :param tree_nodes_data: all specific node data
    :return: data object holding combined info of available data
    """
    data = next(node for node in tree_nodes_data.MetaData.Spell if node['Name'] == skill['Name'])
    effects = [parse_effect(effect) for effect in data.MagicEffects.EIM]
    name = translate_ui_string(skill_translator, data['UIName'])
    return Skill(skill['Name'], name, skill['Rarity'], skill['Category'], skill['MaxLevel'], skill['Angle'],
                 skill['Pos'],
                 skill['Unlock'], effects)


def parse_ring(tree_name: str, number: int):
    """
    Parse a ring tree by obtaining the correct xml for the layout, then the correct XML for the node data
    :param tree_name: internal name of the tree
    :param number: of the tree
    :return: Ring representation including skills
    """
    xml_ring_tree = untangle.parse(f'../input/Umbra/Skills/Trees/PassiveSkills/{tree_name}_tree.xml')
    tree = xml_ring_tree.MetaData.Tree

    paths = get_passive_tree_xml_paths()
    tree_path = next(path for path in paths if tree_name.lower() in path.lower())
    if not tree_path:
        return None

    tree_node_data = untangle.parse(f'../input/Umbra/Skills/Passive/PST/{tree_path}')
    nodes = [parse_skill(node, tree_node_data) for node in tree.Skill]

    return Ring(tree_name, translate_ui_string(skill_translator, tree['UIName']), number, nodes)


def parse_sections(ring: untangle.Element):
    xml_sections = ring.Section
    return {section['Number']: parse_ring(section['Name'], section['Number']) for section in xml_sections}


def get_passive_tree_xml_paths():
    """
    Fetch all specific tree xml paths
    :return: list of all tree xml paths
    """
    return os.listdir('../input/Umbra/Skills/Passive/PST')


def fetch_translations(path):
    """
    Fetch translation pairs via regex, feed them into a dictionary
    :param path: to the translation file
    :return: dictionary with the key:translation format
    """
    with open(path, 'r', encoding='utf8') as f:
        content = f.read()

    regex = re.compile(r"<Data.*?>(?P<id>.*?)<\/Data><\/Cell>\n\s*<Cell.*?><Data.*?>(?P<value>.*?)<")
    return {m['id']: m['value'] for m in regex.finditer(content)}


skill_translation_en_path = '../input/localization/english_xml/text_ui_passiveskills.xml'
skill_translator = fetch_translations(skill_translation_en_path)
effect_translation_default_path = '../input/localization/text_ui_EIM.xml'
effect_translator = fetch_translations(effect_translation_default_path)
effect_translation_en_path = '../input/localization/english_xml/text_ui_EIM.xml'
effect_translator.update(fetch_translations(effect_translation_en_path))

if __name__ == '__main__':
    base_tree_path = '../input/Umbra/Skills/Trees/PSTConfig/Global_tree.xml'

    root = untangle.parse(base_tree_path)
    rings = root.Tree.Ring

    sections = {ring['Number']: parse_sections(ring) for ring in rings}

    pprint(sections)

    with open('tree.json', 'w') as f:
        f.write(json.dumps(sections, indent=2, cls=ComplexEncoder))
    print("-- fin")
