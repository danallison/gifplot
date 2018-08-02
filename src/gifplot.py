from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from IPython.display import Image

IMWriter = manimation.writers.avail['imagemagick']

class GifPlot:
    def __init__(self, filename, fps=10, metadata={}):
        self.filename = filename
        self.fps = fps
        self.metadata = metadata

    def animate(self, t, data_fn, viz_step_fn, viz_setup_fn=None):
        writer = IMWriter(fps=self.fps, metadata=self.metadata)

        fig = plt.figure()
        viz_step = viz_setup_fn(fig) if viz_setup_fn else None

        with writer.saving(fig, self.filename, 100):
            for t_i in t:
                data = data_fn(t_i)
                viz_step = viz_step_fn(t_i, data, viz_step)
                writer.grab_frame()
        plt.close(fig)
        try:
            return Image(filename=self.filename)
        except:
            return fig

    def _get_time_map(self, x, y, t):
        time_map = defaultdict(lambda: [[],[]])
        for i, t_i in enumerate(t):
            time_map[t_i][0].append(x[i])
            time_map[t_i][1].append(y[i])
        return time_map

    def scatter(self, x, y, t, *args, **kwargs):
        time_map = self._get_time_map(x, y, t)
        def data_fn(t_i):
            return time_map[t_i]
        def viz_step_fn(t_i, data, viz_step):
            if viz_step: viz_step.remove()
            plt.title(f'{t_i}')
            return plt.scatter(data[0], data[1], *args, **kwargs)
        def viz_setup_fn(fig):
            plt.xlim(np.min(x), np.max(x))
            plt.ylim(np.min(y), np.max(y))
        return self.animate(sorted(list(time_map.keys())), data_fn, viz_step_fn, viz_setup_fn)
