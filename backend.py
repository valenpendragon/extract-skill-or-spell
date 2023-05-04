from pathlib import Path

TEST_DATA = "./test_data/test_file.txt"
NAME_ENDS = ["(1)", "(2)", "(3)", "(T)", "(M)", "(C)", "(S)"]
EXTRAS = ["Improvised Weapons", "Punch", "Dirty Fighting", "Kick",
          "Bonus to Damage", "Bonus to Defend", "Two Weapons", "Two Weapons",
          "Shrewd thrust", "Shrewd blow", "Throw", "Evade", "Prerequisites",
          "Disarming", "Note", "Show", "Combat", "Believe", "Do Not", "Come",
          "Fire", "Go That Way", "Kill", "Obey", "Quit", "Stop", "Surrender"]


def load_file(filepath):
    """
    This function takes a filepath to a text file and returns a list of lines of
    text contained in the file. It should not be used on any file type other than
    text. It will return an error message if so.
    :param filepath: str
    :return: content: list of str (text lines) or str (error message)
    """
    extension = Path(filepath).suffix
    match extension:
        case ".txt":
            with open(filepath, 'r', encoding="utf-8") as file:
                content = file.readlines()
            return content
        case _:
            return f"{extension} is an invalid format for this program."


def find_spells_in_content(content, name_ends=NAME_ENDS) -> list:
    """
    This functions receives a list of lines of text. It returns a list of lists
    of text which are the spells, talents, or skills broken into individual lists
    of the text descriptions. It also adds markdown emphasis to the name appearing
    in the first line of each sublist.
    :param name_ends: list of str
    :return: list of tuples of indices
    """
    content = content
    name_ends = name_ends
    indices = []
    for j, line in enumerate(content):
        for item in name_ends:
            if item in line:
                indices.append((j, item))
    # We need to the final index which is the end of the text.
    # It will contain a None item.
    indices.append((len(content), None))
    print(indices)
    spells = []
    start_spell = None
    end_spell = None
    start_item = None
    # This loop uses the tuples to bracket the spells, et al
    # contained in the content.
    for idx, item in indices:
        print(f"idx: {idx}. item: {item}. start_item: {start_item}")
        print(f"start_spell: {start_spell}. end_spell: {end_spell}")
        if start_spell is None:
            start_spell = idx
            start_item = item
            continue
        else:
            end_spell = idx
            print(f"start_spell: {start_spell}. end_spell: {end_spell}")
            spell = content[start_spell:end_spell]
            print(f"spell: {spell}")
            first_line = content[start_spell]
            print(f"first_line: {first_line}")
            # start_pos is the starting position of a name_end item.
            # All of them are 3 characters long. So, the end position
            # will start_pos + 3. This tells us the position where the
            # name of the spell, et al ends. We can apply emphasis to it.
            start_pos = first_line.index(start_item)
            end_pos = start_pos + 3
            # print(f"start_pos: {start_pos}. end_pos: {end_pos}.")
            spell[0] = f"__{first_line[0:end_pos]}__{first_line[end_pos:]}"
            spells.append(spell)
            print(f"finished spell: {spell}")

            # Reset the start of spell and starting item for the next round.
            # Reset the end_spell to None.
            end_spell = None
            start_spell = idx
            start_item = item

    return spells


if __name__ == "__main__":
    filepath = TEST_DATA
    test_data = load_file(filepath)
    print(test_data)
    spells = find_spells_in_content(test_data)
    print(spells)
