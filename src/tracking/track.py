class Track:
    _id_counter = 0

    def __init__(self, bbox, score, class_id):
        self.track_id = Track._id_counter
        Track._id_counter += 1

        self.bbox = bbox
        self.score = score
        self.class_id = class_id

        self.age = 0
        self.time_since_update = 0
        self.active = True

    def update(self, bbox, score):
        self.bbox = bbox
        self.score = score
        self.time_since_update = 0

    def step(self):
        self.age += 1
        self.time_since_update += 1