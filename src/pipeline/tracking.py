class ByteTrackProcessor:
    def __init__(self, tracker):
        self.tracker = tracker

    def process(self, ctx):
        ctx.objects = self.tracker.update(ctx.objects)
        return ctx