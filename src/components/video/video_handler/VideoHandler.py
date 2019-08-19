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
        # out every 100 calls (otherwise, it just uses up way too mucm memory)
        self._frame_call_count += 1
        if self._frame_call_count % 100 == 0:
            self.capture.GetCache().Clear()

        openshot_frame_number = frame_number + 1 # openshot is 1-indexed...yay.
        framee = self.capture.GetFrame(openshot_frame_number)

        newqimg = framee.GetImage()

        # f = openshot.UCharVector()
        # f = framee.GetImageAsVec()
        # width = framee.GetWidth()
        # height = framee.GetHeight()
        # newqimg = QImage(f, width, height, width*4, QImage.Format_RGBA8888)

        dat = base64.b64decode(framee.GetImageAsString())
        width = framee.GetWidth()
        height = framee.GetHeight()
        newqimg = QImage(dat, width, height, width*4, QImage.Format_RGBA8888)
        
        self.current_frame_number = frame_number
        return self._image_to_pixmap(newqimg)

    def get_frame_as_image(self, frame_number):
        framee = self.capture.GetFrame(frame_number+1) # openshot is 1-indexed
        dat = base64.b64decode(framee.GetImageAsString())
        width = framee.GetWidth()
        height = framee.GetHeight()
        newqimg = QImage(dat, width, height, width*4, QImage.Format_RGBA8888)
        return newqimg

    def _image_to_pixmap(self, qimg):
        pixmap = QGraphicsPixmapItem()
        pixmap.setPixmap( QPixmap.fromImage(qimg) );
        return pixmap

class CouldNotOpenVideoException(Exception):
    pass
