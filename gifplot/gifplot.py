from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from IPython.display import Image

IMWriter = manimation.writers.avail['imagemagick']

def get_time_map(x, y, t):
    time_map = defaultdict(lambda: [[],[]])
    for i, t_i in enumerate(t):
        time_map[t_i][0].append(x[i])
        time_map[t_i][1].append(y[i])
    return time_map

class GifPlot:
    def __init__(self, filename, fps=10, metadata={}):
        self.filename = filename
        self.fps = fps
        self.metadata = metadata

    def make_gif(self, t, step, setup=None):
        writer = IMWriter(fps=self.fps, metadata=self.metadata)
        fig = plt.figure()
        prev_step = setup(fig) if setup else None
        with writer.saving(fig, self.filename, 100):
            for t_i in t:
                prev_step = step(t_i, prev_step)
                writer.grab_frame()
        plt.close(fig)
        try:
            return Image(filename=self.filename)
        except:
            return fig

    def scatter(self, x, y, t, *args, **kwargs):
        time_map = get_time_map(x, y, t)
        def step(t_i, prev_step):
            data = time_map[t_i]
            if prev_step: prev_step.remove()
            plt.title(f'{t_i}')
            return plt.scatter(data[0], data[1], *args, **kwargs)
        def setup(fig):
            plt.xlim(np.min(x), np.max(x))
            plt.ylim(np.min(y), np.max(y))
        return self.make_gif(sorted(list(time_map.keys())), step, setup)
