import tornado.web
import pylibmc


try:
    mc = pylibmc.Client()       # on sae
except:
    mc = pylibmc.Client(["127.0.0.1"], binary=True)

if not 'grid' in mc:
    mc['grid'] = 25 * 16 * [0]

def get_grid_str():
    grid_str = ""
    for g in mc['grid']:
        grid_str = grid_str + str(g)
    return grid_str
   

class GridHandler(tornado.web.RequestHandler):
    def get(self):
        grid = mc['grid']
        pos = self.get_argument("pos", None)
        if pos is None:         # common request
            self.render('pocket/grid.html')
        else:                   # ajax
            pos = int(pos)
            if pos < 0 or pos >= 400:       # get current grid str
                pass
            else:               # change state
                grid[pos] ^= 1
                mc.set('grid', grid)
            self.write(get_grid_str())
