from pipeline.draw import Drawer

class DrawProcessor:
    def __init__(self, drawer: Drawer):
        self.drawer = drawer

    def process(self, ctx, camera_id= None):
        
        ctx.frame = self.drawer.draw(ctx.frame, ctx.objects, camera_id=camera_id)
        return ctx