import PySimpleGUI as sg
import backend

# This constant covers the way names of most skill, talents, or spells end and
# the descriptive text begins.

sg.theme("Black")


def make_main_window() -> sg.Window:
    """
    This function creates and returns a main_window.
    :return: sg.Window
    """
    # Here is the main window.
    file_choice_label = sg.Text("Select the file to extract spell, skills or talents from:")
    file_choice_input = sg.Input(key="file_choice",
                                 enable_events=True,
                                 visible=True)
    file_choice_button = sg.FileBrowse("Choose",
                                       key="filepath",
                                       target="file_choice")
    layout_col1 = [[file_choice_label],
                   [file_choice_input],
                   [file_choice_button]]

    output_dir_label = sg.Text("Select the destination directory:")
    output_dir_input = sg.Input(key="folder_choice",
                                enable_events=True,
                                visible=True)
    output_dir_button = sg.FolderBrowse("Choose",
                                        key="dest_folder",
                                        target="folder_choice")
    filename_label = sg.Text("Enter the name of the output file:")
    filename_tooltip = "Avoid overwriting the original file if possible."
    filename_input = sg.Input(key="filename",
                              enable_events=True,
                              visible=True,
                              tooltip=filename_tooltip)
    layout_col2 = [[output_dir_label],
                   [output_dir_input],
                   [output_dir_button],
                   [filename_label],
                   [filename_input]]

    col1 = sg.Column(layout=layout_col1)
    col2 = sg.Column(layout=layout_col2)

    convert_file_button = sg.Button("Convert File", key="convert")
    exit_button = sg.Button("Exit", key="exit")
    result_label = sg.Text(key="results", visible=False, text_color="white")
    bottom_row_layout = [[convert_file_button, exit_button, result_label]]

    return sg.Window("Spell, Talent, and Skill Extractor",
                     layout=[[col1],
                             [col2],
                             [bottom_row_layout]],
                     finalize=True)


def main():
    """
    This is the event loop for this application.
    :return:
    """
    main_window = make_main_window()
    while True:
        window, event, values = sg.read_all_windows()
        print(window, event, values)

        if event == sg.WIN_CLOSED and window == main_window:
            break

        match event:
            case "convert":
                filepath = values["file_choice"]
                content = backend.load_file(filepath)


            case "exit":
                break

    main_window.close()


if __name__ == "__main__":
    main()