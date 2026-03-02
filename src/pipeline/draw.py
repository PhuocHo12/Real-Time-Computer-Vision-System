import cv2

class Drawer:
    def __init__(
        self,
        class_names=None,
        show_score=True,
        show_track_id=True,
        box_thickness=2,
        font_scale=0.5,
    ):
        self.class_names = class_names or {}
        self.show_score = show_score
        self.show_track_id = show_track_id
        self.box_thickness = box_thickness
        self.font_scale = font_scale

    def draw(self, frame, objects,  camera_id=None):
        """
        Draw bounding boxes and labels on frame.

        Args:
            frame (np.ndarray): OpenCV image
            objects (list): detection / tracking results

        Returns:
            np.ndarray: annotated frame
        """
        for obj in objects:
            self._draw_one(frame, obj)

        return frame

    def _draw_one(self, frame, obj):
        x1, y1, x2, y2 = map(int, obj[:4])
        score = obj[4]
        class_id = int(obj[5])
        track_id = obj[6] if len(obj) > 6 else None

        color = self._color_for_id(track_id or class_id)

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            self.box_thickness,
        )

        # Build label
        label_parts = []

        if class_id in self.class_names:
            label_parts.append(self.class_names[class_id])
        else:
            label_parts.append(f"id:{class_id}")

        if self.show_score:
            label_parts.append(f"{score:.2f}")

        if track_id is not None and self.show_track_id:
            label_parts.append(f"T{track_id}")

        label = " ".join(label_parts)

        self._draw_label(frame, label, x1, y1, color)

    def _draw_label(self, frame, text, x, y, color):
        (w, h), _ = cv2.getTextSize(
            text,
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            1,
        )

        cv2.rectangle(
            frame,
            (x, y - h - 6),
            (x + w + 4, y),
            color,
            -1,
        )

        cv2.putText(
            frame,
            text,
            (x + 2, y - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    def _color_for_id(self, idx):
        """
        Generate a consistent color for a given id.
        """
        idx = int(idx)
        return (
            (37 * idx) % 255,
            (17 * idx) % 255,
            (29 * idx) % 255,
        )