import csv
import json
import uuid

from ..store import Store
from ..store.models import *

class Serializer:

    @classmethod
    def store_to_json(self, store):
        h = {}
        h['video_filename'] = store.video_filename
        h['video_total_frames'] = store.video_total_frames
        h['video_current_frame'] = store.video_current_frame
        h['frames_to_jump'] = store.frames_to_jump
        h['selected_segment_id'] = str(store.selected_segment_id)
        h['segments'] = []
        h['tags'] = []

        for tag in store.tags:
            h['tags'].append(self._tag_to_json(tag))

        for segment in store.segments:
            h['segments'].append(self._segment_to_json(segment))

        return json.dumps(h)

    @classmethod
    def json_to_store(self, j):
        h = json.loads(j)
        store = Store.Store()

        store.video_filename = h['video_filename']
        store.video_total_frames = h['video_total_frames']
        store.video_current_frame = h['video_current_frame']
        store.frames_to_jump = h['frames_to_jump']

        try:
            store.selected_segment_id = uuid.UUID(h['selected_segment_id'])
        except:
            store.selected_segment_id = None

        for tag in h['tags']:
            store.tags.append(self._json_to_tag(tag))

        for segment in h['segments']:
            store.segments.append(self._json_to_segment(segment))

        return store

    @classmethod
    def segments_to_csv(self, filename, store):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Start Frame', 'End Frame'] + list(map(lambda x: x.name, store.tags)))

            for segment in store.segments:
                tag_values = list(map(lambda x: 1 if segment.is_tagged_with(x) else 0, store.tags))
                writer.writerow([segment.start_frame, segment.end_frame] + tag_values)

    @classmethod
    def _json_to_tag(self, tag):
        t = Tag(tag['name'])
        t.id = uuid.UUID(tag['id'])
        return t

    @classmethod
    def _json_to_segment(self, segment):
        s = Segment(segment['start_frame'])
        s.end_frame = segment['end_frame']
        s.id = uuid.UUID(segment['id'])

        for tag in segment['tags']:
            s.add_tag(self._json_to_tag(tag))

        return s

    @classmethod
    def _segment_to_json(self, segment):
        h = {}
        h['id'] = str(segment.id)
        h['start_frame'] = segment.start_frame
        h['end_frame'] = segment.end_frame
        h['tags'] = []

        for tag in segment.tags:
            h['tags'].append(self._tag_to_json(tag))

        return h

    @classmethod
    def _tag_to_json(self, tag):
        h = {}
        h['id'] = str(tag.id)
        h['name'] = tag.name
        return h
