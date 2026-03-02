from .base import BaseTracker
from .track import Track
from .iou import iou

class ByteTrackTracker(BaseTracker):
    def __init__(
        self,
        high_thresh=0.6,
        low_thresh=0.1,
        match_thresh=0.5,
        max_lost=30
    ):
        self.high_thresh = high_thresh
        self.low_thresh = low_thresh
        self.match_thresh = match_thresh
        self.max_lost = max_lost

        self.tracks = []

    def update(self, detections):
        """
        detections: [x1, y1, x2, y2, score, class_id]
        """
        high_dets = [d for d in detections if d[4] >= self.high_thresh]
        low_dets = [d for d in detections if self.low_thresh <= d[4] < self.high_thresh]

        updated_tracks = []
        used_dets = set()

        # Step all tracks
        for track in self.tracks:
            track.step()

        # 1️⃣ Match high-confidence detections
        for track in self.tracks:
            best_iou = 0
            best_det_idx = -1

            for i, det in enumerate(high_dets):
                if i in used_dets or det[5] != track.class_id:
                    continue

                score = iou(track.bbox, det[:4])
                if score > best_iou:
                    best_iou = score
                    best_det_idx = i

            if best_iou >= self.match_thresh:
                det = high_dets[best_det_idx]
                track.update(det[:4], det[4])
                used_dets.add(best_det_idx)
                updated_tracks.append(track)

        # 2️⃣ Match low-confidence detections (recovery)
        for track in self.tracks:
            if track.time_since_update == 0:
                continue

            for det in low_dets:
                if det[5] != track.class_id:
                    continue

                if iou(track.bbox, det[:4]) >= self.match_thresh:
                    track.update(det[:4], det[4])
                    updated_tracks.append(track)
                    break

        # 3️⃣ Create new tracks
        for i, det in enumerate(high_dets):
            if i not in used_dets:
                updated_tracks.append(
                    Track(det[:4], det[4], det[5])
                )

        # 4️⃣ Remove dead tracks
        self.tracks = [
            t for t in updated_tracks
            if t.time_since_update <= self.max_lost
        ]

        # Output
        return [
            {
                "track_id": t.track_id,
                "bbox": t.bbox,
                "score": t.score,
                "class_id": t.class_id
            }
            for t in self.tracks
        ]