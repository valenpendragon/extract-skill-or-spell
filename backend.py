from pathlib import Path

TEST_DATA = "./test_data/test_file.txt"
NAME_ENDS = ["(1)", "(2)", "(3)", "(T)", "(M)", "(C)", "(S)"]
EXTRAS = ["Improvised Weapons", "Punch", "Dirty Fighting", "Kick",
          "Bonus to Damage", "Bonus to Defend", "Two Weapons", "Two Weapons",
          "Shrewd thrust", "Shrewd blow", "Throw", "Evade", "Prerequisites",
          "Disarming", "Note", "Show", "Combat", "Believe", "Do Not", "Come",
          "Fire", "Go That Way", "Kill", "Obey", "Quit", "Stop", "Surrender"]
TEST_OUTPUT_DIR = "./output"
TEST_OUTPUT_FILE = "output_test.txt"


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


def remove_linefeeds(raw_spells: list) -> list:
    """
    This function takes a list of spells and removes linefeeds from every
    line forming the spell.
    :param lines: list of lists of strings
    :return: list of lists of strings
    """
    spells_sans_linefeed = []
    for spell in raw_spells:
        spell = [line.replace("\n", "") for line in spell]
        spells_sans_linefeed.append(spell)
    print(spells_sans_linefeed)
    return spells_sans_linefeed


def find_paragraphs(remaining_txt: list,
                    extras=EXTRAS,
                    has_extras=True) -> list:
    """
    This functions receives the remaining text, which will be in the form of
    a list of lines. This text will be returned as assembled paragraphs.
    :param remaining_txt: list of str
    :param extras: list of str
    :param has_extras: bool
    :return: list
    """
    ending_punctuation = [".", "!", "?", ":"]
    current_paragraph = ""
    paragraphs = []
    for line in remaining_txt:
        print(f"current_paragraph: {current_paragraph}")
        # The copying process can leave spaces at the start of a paragraph.
        while line[0] == " ":
            line = line[1:]

        # If a line starts with an extra, the paragraph starts.
        # We also have to add strong emphasis to the extra part.
        extra = identify_extras(line, extras)
        bullet = check_for_bullet(line)
        print(f"extra: {extra}")
        print(f"bullet: {bullet}")
        if has_extras and extra is not None:
            if current_paragraph != "":
                paragraphs.append(current_paragraph)
                current_paragraph = ""
            current_paragraph = line.replace(extra, f"__{extra}__")
            if current_paragraph[-1] in ending_punctuation:
                paragraphs.append(current_paragraph)
        elif bullet:
            if current_paragraph != "":
                paragraphs.append(current_paragraph)
                current_paragraph = ""
            current_paragraph = line.replace("•", "*")
            if current_paragraph[-1] in ending_punctuation:
                paragraphs.append(current_paragraph)
                current_paragraph = ""
        else:
            if current_paragraph != "" and current_paragraph[-1] in ending_punctuation:
                paragraphs.append(current_paragraph)
                current_paragraph = ""
            current_paragraph = current_paragraph + " " + line
            # Paragraphs typically end with the end of a sentence.
            if line[-1] in ending_punctuation:
                paragraphs.append(current_paragraph)
                current_paragraph = ""
        # print(f"current_paragraph: {current_paragraph}")
        # print(f"extra: {extra}")
        print(f"paragraphs: {paragraphs}")

    # Once the initial pass of paragraph generation is done, we need to remove
    # any duplicate first lines. This will correct a bug in which the first line
    # ends with a period or other indicator of the potential end of a paragraph.
    # We can remove these duplicates quite easily.
    # Due to the amount of text involved here, it is possible that an empty
    # paragraph can be generated. This fixes one aspect of this bug.
    if len(paragraphs) >= 2:
        paragraphs = check_for_duplication(paragraphs)
    return paragraphs


def check_for_duplication(paragraphs: list) -> list:
    """
    This functions takes a list of text paragraphs and removes duplication of
    all or portions of a paragraph at the beginning of the next paragraph.
    :param paragraphs: list of str
    :return: list of str
    """
    # Duplication produced by the first line ending with a potential paragraph end
    # can be easily fixed by checking lines against the next line.
    no_paragraphs = len(paragraphs)
    checked_paragraphs = []
    index = 0
    while index < no_paragraphs - 1:
        current_paragraph = paragraphs[index]
        next_paragraph = paragraphs[index + 1]
        if current_paragraph not in next_paragraph:
            checked_paragraphs.append(current_paragraph)
        index += 1
        print(f"checked_paragraphs: {checked_paragraphs}")
    checked_paragraphs.append(paragraphs[-1])
    print(f"checked_paragraphs: {checked_paragraphs}")
    return checked_paragraphs


def identify_extras(line: str,
                    extras: list):
    """
    This function checks to see if a line begins with a string in extras. The
    extras are items that start emphasized paragraphs or bullet items in the
    spell description.
    :param line: str
    :param extras: list of str
    :return: str or None
    """
    for extra in extras:
        if line.startswith(extra):
            return extra
    return None


def check_for_bullet(s: str) -> bool:
    """
    This function checks for a bullet character at the beginning of a string and returns
    True or False depending on the starting character.
    :param s: str
    :return: bool
    """
    return s[0] == "•"


def write_new_file(spells, dest_folder, new_filename) -> None:
    """
    This function writes a list of lists of strings to disk, adding break
    lines for each string.
    :param spells: list of lists of str
    :param dest_folder: str
    :param new_filename: str
    :return: None
    """
    new_filepath = f"{dest_folder}/{new_filename}"
    for idx, spell in enumerate(spells):
        print(f"idx: {idx}. spell: {spell}")
        if spell == []:
            continue
        output = [line + "\n" for line in spell]
        print(f"output: {output}")
        # Separate each spell by an extra line.
        output[-1] = output[-1] + "\n"
        with open(new_filepath, 'a') as file:
            file.writelines(output)


def finalize_spells(spells):
    """
    This function takes a list of lists of string with linefeeds removed
    from all lines. It returns the spells as paragraph descriptions.
    :param spells: list of lists of string
    :return: list of lists of string
    """
    finalized_spells = []
    for spell in spells:
        updated_spell = find_paragraphs(spell)
        finalized_spells.append(updated_spell)
    return finalized_spells


if __name__ == "__main__":
    filepath = TEST_DATA
    test_data = load_file(filepath)
    print(test_data)
    raw_spells = find_spells_in_content(test_data)
    print(raw_spells)
    spells_sans_linefeed = remove_linefeeds(raw_spells)
    finalized_spells = finalize_spells(spells_sans_linefeed)
    print(finalized_spells)
    write_new_file(finalized_spells, TEST_OUTPUT_DIR, TEST_OUTPUT_FILE)
