import base64
import json

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import (QPixmap, QImage)
import openshot
from openshot import FFmpegReader

class VideoHandler:
    def __init__(self, filename):
        self.filename = filename

        try:
            self.capture = FFmpegReader(self.filename)
        except:
            raise CouldNotOpenVideoException

        self.capture.Open()
        self.current_frame_number = 0
        self._frame_call_count = 0

    def get_total_frames(self):
        return int(json.loads(self.capture.Json())['video_length'])

    def get_current_frame_number(self):
        return self.current_frame_number

    def get_frame(self, frame_number):
        # libopenshot's cache isn't particularly useful for us, so we clear it
        # out every 100 calls (otherwise, it just uses up way too much memory)
        self._frame_call_count += 1
        if self._frame_call_count % 100 == 0:
            self.capture.GetCache().Clear()

        frame = self.capture.GetFrame(frame_number + 1) # openshot is 1-indexed...yay.

        # in order to retrieve the image from libopen shot, we actually have
        # to base64 decode it
        dat = base64.b64decode(frame.GetImageAsString())
        frame.DeleteImageAsStringMemory()
        newqimg = QImage(dat, frame.GetWidth(), frame.GetHeight(), frame.GetWidth()*4, QImage.Format_RGBA8888)

        self.current_frame_number = frame_number
        return self._image_to_pixmap(newqimg)

    def _image_to_pixmap(self, qimg):
        pixmap = QGraphicsPixmapItem()
        pixmap.setPixmap( QPixmap.fromImage(qimg) );
        return pixmap

class CouldNotOpenVideoException(Exception):
    pass
