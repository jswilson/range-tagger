from PyQt5.QtWidgets import (QMenuBar, QAction)

from .commands import AddTagToSegmentCommand
from .commands import AddSegmentCommand
from .commands import AddEndFrameToSegmentCommand
from .components.serialize import Serializer
from .registry import Registry

class MenuBar(QMenuBar):

    def __init__(self, store, invoker):
        QMenuBar.__init__(self)

        self.store = store
        self.invoker = invoker

        self._create_file_menu()
        self._create_edit_menu()
        self._create_playback_menu()

    def _on_export(self):
        filename, _ = QFileDialog.getSaveFileName(self,
            Registry.EXPORT_SEGMENTS_TITLE,
            '.',
            Registry.EXPORT_SEGMENTS_TYPES
        )

        if not filename:
            return

        Serializer.segments_to_csv(filename, self.store)

    def _on_tag1(self):
        if len(self.store.tags) < 1:
            return
        self._toggle_tag(0)

    def _on_tag2(self):
        if len(self.store.tags) < 2:
            return
        self._toggle_tag(1)

    def _on_tag3(self):
        if len(self.store.tags) < 3:
            return
        self._toggle_tag(2)

    def _on_tag4(self):
        if len(self.store.tags) < 4:
            return
        self._toggle_tag(3)

    def _toggle_tag(self, index):
        if (self.store.does_segment_have_tag(self.store.selected_segment_id, self.store.tags[index].id)):
            self.store.remove_tag_from_segment(self.store.tags[index].id, self.store.selected_segment_id)
        else:
            self.store.add_tag_to_segment(self.store.tags[index].id, self.store.selected_segment_id)

    def _on_video_load(self):
        if not self.store.video_filename:
            self.create_segment.setEnabled(False)
        self.create_segment.setEnabled(True)


    def _on_tags_changed(self):
        if self.store.selected_segment_id is None or len(self.store.tags) == 0:
            self.add_tag1.setEnabled(False)
            self.add_tag2.setEnabled(False)
            self.add_tag3.setEnabled(False)
            self.add_tag4.setEnabled(False)

        elif (len(self.store.tags) == 1):
            self.add_tag1.setEnabled(True)
            self.add_tag2.setEnabled(False)
            self.add_tag3.setEnabled(False)
            self.add_tag4.setEnabled(False)

        elif (len(self.store.tags) == 2):
            self.add_tag1.setEnabled(True)
            self.add_tag2.setEnabled(True)
            self.add_tag3.setEnabled(False)
            self.add_tag4.setEnabled(False)

        elif (len(self.store.tags) == 3):
            self.add_tag1.setEnabled(True)
            self.add_tag2.setEnabled(True)
            self.add_tag3.setEnabled(True)
            self.add_tag4.setEnabled(False)

        elif (len(self.store.tags) == 4):
            self.add_tag1.setEnabled(True)
            self.add_tag2.setEnabled(True)
            self.add_tag3.setEnabled(True)
            self.add_tag4.setEnabled(True)

    def _on_segment_selected(self):
        if (self.store.selected_segment_id is None):
            self.end_segment.setEnabled(False)
            self._on_tags_changed()
        else:
            self.end_segment.setEnabled(True)
            self._on_tags_changed()

    def _on_create_segment(self):
        command = AddSegmentCommand(self.store, self.store.video_current_frame)
        self.invoker.execute(command)

    def _on_undo(self):
        self.invoker.undo()

    def _on_redo(self):
        self.invoker.redo()

    def _on_endseg(self):
        command = AddEndFrameToSegmentCommand(self.store, self.store.selected_segment_id, self.store.video_current_frame, self)
        self.invoker.execute(command)

    def _on_back100x(self):
        self.store.set_video_frame(self.store.video_current_frame - 100 * self.store.frames_to_jump)

    def _on_back10x(self):
        self.store.set_video_frame(self.store.video_current_frame - 10 * self.store.frames_to_jump)

    def _on_back1x(self):
        self.store.set_video_frame(self.store.video_current_frame - self.store.frames_to_jump)

    def _on_fwd100x(self):
        self.store.set_video_frame(self.store.video_current_frame + 100 * self.store.frames_to_jump)

    def _on_fwd10x(self):
        self.store.set_video_frame(self.store.video_current_frame + 10 * self.store.frames_to_jump)

    def _on_fwd1x(self):
        self.store.set_video_frame(self.store.video_current_frame + self.store.frames_to_jump)

    def _on_back1frame(self):
        self.store.set_video_frame(self.store.video_current_frame - 1)

    def _on_fwd1frame(self):
        self.store.set_video_frame(self.store.video_current_frame + 1)

    def _create_file_menu(self):
        file_menu = self.addMenu(' &File')

        export = QAction(Registry.MENU_EXPORT_CSV,self)
        export.setShortcut(Registry.MENU_EXPORT_CSV_KEYS)
        file_menu.addAction(export)
        export.triggered.connect(self._on_export)

    def _create_edit_menu(self):
        edit_menu = self.addMenu(' &Edit')

        # undo
        undo = QAction(Registry.MENU_UNDO, self)
        undo.setShortcut(Registry.MENU_UNDO_KEYS)
        edit_menu.addAction(undo)
        undo.triggered.connect(self._on_undo)

        # redo
        redo = QAction(Registry.MENU_REDO, self)
        redo.setShortcut(Registry.MENU_REDO_KEYS)
        edit_menu.addAction(redo)
        redo.triggered.connect(self._on_redo)

        edit_menu.addSeparator()

        # create segment command
        self.create_segment = QAction(Registry.MENU_CREATE_SEGMENT, self)
        self.create_segment.setShortcut(Registry.MENU_CREATE_SEGMENT_KEYS)
        edit_menu.addAction(self.create_segment)
        self.create_segment.triggered.connect(self._on_create_segment)
        if (not self.store.video_filename):
            self.create_segment.setEnabled(False)
        self.store.video_filename_changed.connect(self._on_video_load)

        # end segment command
        self.end_segment = QAction(Registry.MENU_END_SEGMENT, self)
        self.end_segment.setShortcut(Registry.MENU_END_SEGMENT_KEYS)
        edit_menu.addAction(self.end_segment)
        self.end_segment.triggered.connect(self._on_endseg)

        if (self.store.selected_segment_id is None):
            self.end_segment.setEnabled(False)
        self.store.selected_segment_changed.connect(self._on_segment_selected)

        edit_menu.addSeparator()

        # shortcuts to tag the current segment
        self._create_tagging_shortcuts(edit_menu)

        self.store.tag_added.connect(self._on_tags_changed)
        self.store.tag_added.connect(self._on_tags_changed)

    def _create_playback_menu(self):
        playback_menu = self.addMenu(' &Playback')

        self.back100 = QAction(Registry.MENU_BACK_100X, self)
        self.back100.setShortcut(Registry.MENU_BACK_100X_KEYS)
        playback_menu.addAction(self.back100)
        self.back100.triggered.connect(self._on_back100x)

        self.back10 = QAction(Registry.MENU_BACK_10X, self)
        self.back10.setShortcut(Registry.MENU_BACK_10X_KEYS)
        playback_menu.addAction(self.back10)
        self.back10.triggered.connect(self._on_back10x)

        self.back1 = QAction(Registry.MENU_BACK_1X, self)
        self.back1.setShortcut(Registry.MENU_BACK_1X_KEYS)
        playback_menu.addAction(self.back1)
        self.back1.triggered.connect(self._on_back1x)

        self.back1frame = QAction(Registry.MENU_BACK_1FRAME, self)
        self.back1frame.setShortcut(Registry.MENU_BACK_1FRAME_KEYS)
        playback_menu.addAction(self.back1frame)
        self.back1frame.triggered.connect(self._on_back1frame)

        self.fwd1frame = QAction(Registry.MENU_FORWARD_1FRAME, self)
        self.fwd1frame.setShortcut(Registry.MENU_FORWARD_1FRAME_KEYS)
        playback_menu.addAction(self.fwd1frame)
        self.fwd1frame.triggered.connect(self._on_fwd1frame)

        self.fwd1 = QAction(Registry.MENU_FORWARD_1X, self)
        self.fwd1.setShortcut(Registry.MENU_FORWARD_1X_KEYS)
        playback_menu.addAction(self.fwd1)
        self.fwd1.triggered.connect(self._on_fwd1x)

        self.fwd10 = QAction(Registry.MENU_FORWARD_10X, self)
        self.fwd10.setShortcut(Registry.MENU_FORWARD_10X_KEYS)
        playback_menu.addAction(self.fwd10)
        self.fwd10.triggered.connect(self._on_fwd10x)

        self.fwd100 = QAction(Registry.MENU_FORWARD_100X, self)
        self.fwd100.setShortcut(Registry.MENU_FORWARD_100X_KEYS)
        playback_menu.addAction(self.fwd100)
        self.fwd100.triggered.connect(self._on_fwd100x)

    def _create_tagging_shortcuts(self, menu):
        self.add_tag1 = QAction(Registry.MENU_TAG_ONE, self)
        self.add_tag1.setShortcut(Registry.MENU_TAG_ONE_KEYS)
        menu.addAction(self.add_tag1)
        self.add_tag1.triggered.connect(self._on_tag1)

        self.add_tag2 = QAction(Registry.MENU_TAG_TWO, self)
        self.add_tag2.setShortcut(Registry.MENU_TAG_TWO_KEYS)
        menu.addAction(self.add_tag2)
        self.add_tag2.triggered.connect(self._on_tag2)

        self.add_tag3 = QAction(Registry.MENU_TAG_THREE, self)
        self.add_tag3.setShortcut(Registry.MENU_TAG_THREE_KEYS)
        menu.addAction(self.add_tag3)
        self.add_tag3.triggered.connect(self._on_tag3)

        self.add_tag4 = QAction(Registry.MENU_TAG_FOUR, self)
        self.add_tag4.setShortcut(Registry.MENU_TAG_FOUR_KEYS)
        menu.addAction(self.add_tag4)
        self.add_tag4.triggered.connect(self._on_tag4)

        self._on_tags_changed()