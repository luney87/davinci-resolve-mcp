"""record_frame_mode handling in media_pool append/create clip_infos actions.

Observed live (Studio, timeline start_frame 90000): record_frame 90721 landed
at 180721 because the wrapper added the timeline start, and a top-level
record_frame_mode="absolute" in the params dict changed nothing — the mode key
was only read from inside each clip_infos entry, and everything else in the
entry or the params dict was silently dropped. These tests pin three things:

- entry-level record_frame_mode="absolute" bypasses the start-frame offset
  through the real dispatcher (the exact live scenario),
- a top-level record_frame_mode applies as the default for every entry,
- a typo'd clip_infos key is an error, not a silent no-op.
"""

import unittest
from unittest import mock

import src.server as s
from tests._error_envelope_helpers import err_message, is_err

TIMELINE_START = 90000


class ClipStub:
    def __init__(self, unique_id="clip-1", name="C6301.MP4"):
        self.unique_id = unique_id
        self.name = name

    def GetUniqueId(self):
        return self.unique_id

    def GetName(self):
        return self.name


class FolderStub:
    def __init__(self, clips):
        self.clips = clips

    def GetClipList(self):
        return list(self.clips)

    def GetSubFolderList(self):
        return []


class TimelineItemStub:
    def __init__(self, unique_id, name):
        self.unique_id = unique_id
        self.name = name

    def GetUniqueId(self):
        return self.unique_id

    def GetName(self):
        return self.name


class TimelineStub:
    def __init__(self, name="Timeline 1", start_frame=TIMELINE_START):
        self.name = name
        self.start_frame = start_frame
        self.items = []

    def GetName(self):
        return self.name

    def GetUniqueId(self):
        return f"timeline-{self.name}"

    def GetStartFrame(self):
        return self.start_frame

    def GetTrackCount(self, track_type):
        return 1 if track_type == "video" else 0

    def GetItemListInTrack(self, track_type, track_index):
        if track_type == "video" and track_index == 1:
            return list(self.items)
        return []


class ProjectStub:
    def __init__(self, timeline):
        self.timeline = timeline

    def GetCurrentTimeline(self):
        return self.timeline

    def SetCurrentTimeline(self, timeline):
        self.timeline = timeline
        return True

    def GetTimelineCount(self):
        return 0

    def GetTimelineByIndex(self, index):
        return None


class MediaPoolStub:
    def __init__(self, root, project):
        self.root = root
        self.project = project
        self.appended_rows = []

    def GetRootFolder(self):
        return self.root

    def CreateEmptyTimeline(self, name):
        timeline = TimelineStub(name=name)
        self.project.timeline = timeline
        return timeline

    def AppendToTimeline(self, rows):
        self.appended_rows.append(list(rows))
        appended = []
        for index, row in enumerate(rows, start=1):
            item = TimelineItemStub(f"timeline-item-{index}", f"item-{index}")
            self.project.timeline.items.append(item)
            appended.append(item)
        return appended


def _entry(**overrides):
    base = {
        "clip_id": "clip-1",
        "start_frame": 0,
        "end_frame": 100,
        "record_frame": 90721,
        "track_index": 1,
    }
    base.update(overrides)
    return base


class RecordFrameModeDispatchTest(unittest.TestCase):
    def setUp(self):
        timeline = TimelineStub()
        self.project = ProjectStub(timeline)
        self.media_pool = MediaPoolStub(FolderStub([ClipStub()]), self.project)
        patcher = mock.patch.object(
            s, "_get_mp", return_value=(None, self.project, self.media_pool, None)
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def _last_record_frame(self):
        self.assertTrue(self.media_pool.appended_rows, "AppendToTimeline was never called")
        return self.media_pool.appended_rows[-1][0]["recordFrame"]

    def test_entry_level_absolute_mode_bypasses_timeline_start(self):
        result = s.media_pool("append_to_timeline", {
            "clip_infos": [_entry(record_frame_mode="absolute")],
        })
        self.assertTrue(result.get("success"), result)
        self.assertEqual(self._last_record_frame(), 90721)

    def test_default_mode_is_timeline_relative(self):
        result = s.media_pool("append_to_timeline", {
            "clip_infos": [_entry(record_frame=721)],
        })
        self.assertTrue(result.get("success"), result)
        self.assertEqual(self._last_record_frame(), TIMELINE_START + 721)

    def test_top_level_absolute_mode_applies_to_entries(self):
        result = s.media_pool("append_to_timeline", {
            "clip_infos": [_entry()],
            "record_frame_mode": "absolute",
        })
        self.assertTrue(result.get("success"), result)
        self.assertEqual(self._last_record_frame(), 90721)

    def test_entry_mode_overrides_top_level_mode(self):
        result = s.media_pool("append_to_timeline", {
            "clip_infos": [_entry(record_frame=721, record_frame_mode="relative")],
            "record_frame_mode": "absolute",
        })
        self.assertTrue(result.get("success"), result)
        self.assertEqual(self._last_record_frame(), TIMELINE_START + 721)

    def test_invalid_top_level_mode_is_an_error(self):
        result = s.media_pool("append_to_timeline", {
            "clip_infos": [_entry()],
            "record_frame_mode": "absolutely",
        })
        self.assertTrue(is_err(result), result)
        self.assertIn("record_frame_mode", err_message(result))
        self.assertFalse(self.media_pool.appended_rows)

    def test_unknown_clip_info_key_is_an_error(self):
        result = s.media_pool("append_to_timeline", {
            "clip_infos": [_entry(recordframe_mode="absolute")],
        })
        self.assertTrue(is_err(result), result)
        self.assertIn("recordframe_mode", err_message(result))
        self.assertFalse(self.media_pool.appended_rows)

    def test_create_timeline_from_clips_honors_top_level_absolute(self):
        result = s.media_pool("create_timeline_from_clips", {
            "name": "Cut v1",
            "clip_infos": [_entry()],
            "record_frame_mode": "absolute",
        })
        self.assertTrue(result.get("success"), result)
        self.assertEqual(self._last_record_frame(), 90721)

    def test_create_timeline_from_clips_rejects_unknown_entry_key(self):
        result = s.media_pool("create_timeline_from_clips", {
            "name": "Cut v1",
            "clip_infos": [_entry(record_mode="absolute")],
        })
        self.assertTrue(is_err(result), result)
        self.assertIn("record_mode", err_message(result))
        self.assertFalse(self.media_pool.appended_rows)


if __name__ == "__main__":
    unittest.main()
