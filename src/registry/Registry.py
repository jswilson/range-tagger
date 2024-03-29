import os.path
import ntpath
import sys
from appdirs import AppDirs

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def resource_location(dev_location):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path_leaf(dev_location))
    return dev_location

class Registry:
    SEGMENT_MENU_QSS = resource_location("./src/components/segments/segment-menu.qss")
    TAG_MENU_QSS = resource_location("./src/components/tags/tag-menu.qss")
    VIDEO_AREA_QSS = resource_location("./src/components/video/video-area.qss")
    CONTROLS_QSS = resource_location("./src/components/video/controls.qss")
    TAG_LIST_ITEM_QSS = resource_location("./src/components/tags/tag-list-item.qss")
    SEGMENT_LIST_ITEM_QSS = resource_location("./src/components/segments/segment-list-item.qss")
    OPEN_IMAGE = resource_location("./src/registry/open.png")

    CONFIG_FILE_LOCATION = os.path.join(AppDirs("range-tagger", "").user_data_dir, 'range-tagger.seg')

    OPEN_VIDEO_DIALOG_TITLE = "Open Video"
    OPEN_VIDEO_DIALOG_FILE_TYPES = "Video Files (*.mp4 *.mkv *.avi *.ts)"
    SEGMENT_MENU_HEADER_STR = "Segments"
    TAG_MENU_HEADER_STR = "Tags"
    NEW_TAG_PLACEHOLDER_STR = "Add Tag..."
    OPEN_VIDEO_STR = "Open Video for Tagging"
    CREATE_SEGMENT_BUTTON = "Create Segment"
    EXPORT_SEGMENTS_TITLE = "Export Segments as CSV"
    EXPORT_SEGMENTS_TYPES = "CSV (*.csv)"
    CONTROLS_DEFAULT_FRAMES_JUMP = 10

    MENU_EXPORT_CSV = "Export to CSV"
    MENU_EXPORT_CSV_KEYS = "Ctrl+Shift+x"
    MENU_UNDO = "Undo"
    MENU_UNDO_KEYS = "Ctrl+z"
    MENU_REDO = "Redo"
    MENU_REDO_KEYS = "Ctrl+Shift+z"
    MENU_CREATE_SEGMENT = "Create Segment at Current Frame"
    MENU_CREATE_SEGMENT_KEYS = "Ctrl+Shift+c"
    MENU_END_SEGMENT = "End Segment at Current Frame"
    MENU_END_SEGMENT_KEYS = "Ctrl+Shift+e"
    MENU_TAG_ONE = "Tag Segment with First Tag"
    MENU_TAG_ONE_KEYS = "Ctrl+1"
    MENU_TAG_TWO = "Tag Segment with Second Tag"
    MENU_TAG_TWO_KEYS = "Ctrl+2"
    MENU_TAG_THREE = "Tag Segment with Third Tag"
    MENU_TAG_THREE_KEYS = "Ctrl+3"
    MENU_TAG_FOUR = "Tag Segment with Fourth Tag"
    MENU_TAG_FOUR_KEYS = "Ctrl+4"
    MENU_BACK_100X = "Back 100x"
    MENU_BACK_100X_KEYS = "a"
    MENU_BACK_10X = "Back 10x"
    MENU_BACK_10X_KEYS = "s"
    MENU_BACK_1X = "Back 1x"
    MENU_BACK_1X_KEYS = "d"
    MENU_BACK_1FRAME = "Back 1 frame"
    MENU_BACK_1FRAME_KEYS = "f"
    MENU_FORWARD_1FRAME = "Forward 1 frame"
    MENU_FORWARD_1FRAME_KEYS = "j"
    MENU_FORWARD_1X = "Forward 1x"
    MENU_FORWARD_1X_KEYS = "k"
    MENU_FORWARD_10X = "Forward 10x"
    MENU_FORWARD_10X_KEYS = "l"
    MENU_FORWARD_100X = "Forward 100x"
    MENU_FORWARD_100X_KEYS = ";"
