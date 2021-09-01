import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np

def make_box_layout():
     return widgets.Layout(
        border='solid 1px black',
        margin='0px 10px 10px 0px',
        padding='5px 5px 5px 5px'
     )
 
class MakeMeshWidget(widgets.HBox):
     
    def __init__(self):
        super().__init__()
        self.output = widgets.Output()
        
        self.data = {
            "stream_slope": 0.05,
            "nx": 11,
            "ny": 21,
            "x_range": [0.0, 10.0],
            "y_range": [0.0, 20.0],
            "z_range": [0.0, 10.0],
            "z_v": 7.0,
        }
        
        self.mapping = {
            "Slope:": "stream_slope",
            "$N_x$:": "nx",
            "$N_y$:": "ny",
            "$N_z$:": "x_min",
            "$x_0, x_1$:": "x_range",
            "$y_0, y_1$:": "y_range",
            "$z_0, z_1$:": "z_range",
            "$z_V$:": "z_v",
        }
        
        inv_map = {self.mapping[key]: key for key in self.mapping}
 
        with self.output:
            self.fig = plt.figure(constrained_layout=True, figsize=(5, 3.5))
            self.ax = self.fig.add_subplot(projection='3d')
        
        self.compute_surface()
        self.plot_surface()
            
        self.fig.canvas.toolbar_position = 'bottom'
        self.ax.grid(True)
        
        # ===================== #
        
        label_discretization = widgets.Label(value="Discretization")
        
        slider_nx = widgets.IntSlider(
            value=self.data['nx'],
            min=1,
            max=30,
            step=1,
            description=inv_map['nx'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        
        slider_ny = widgets.IntSlider(
            value=self.data['ny'],
            min=1,
            max=30,
            step=1,
            description=inv_map['ny'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
              
        label_extent = widgets.Label(value="Extent")
        
        slider_xrange = widgets.FloatRangeSlider(
            value=self.data['x_range'],
            min=0,
            max=30,
            step=1,
            description=inv_map['x_range'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
        )
        
        slider_yrange = widgets.FloatRangeSlider(
            value=self.data['y_range'],
            min=0,
            max=30,
            step=1,
            description=inv_map['y_range'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
        )
        
        slider_zrange = widgets.FloatRangeSlider(
            value=self.data['z_range'],
            min=0,
            max=30,
            step=1,
            description=inv_map['z_range'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
        )
        
        label_params = widgets.Label(value="Parameters")
        slider_slope = widgets.FloatSlider(
            value=self.data['stream_slope'],
            min=0,
            max=1,
            step=0.01,
            description=inv_map['stream_slope'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.3f'
        )
        
        slider_zv = widgets.FloatSlider(
            value=self.data['z_v'],
            min=0.0,
            max=30,
            step=1,
            description=inv_map['z_v'],
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
    
        controls = widgets.VBox([
            label_discretization,
            slider_nx,
            slider_ny,
            
            label_extent,
            slider_xrange,
            slider_yrange,
            slider_zrange,
            
            label_params,
            slider_slope,
            slider_zv,
        ])
        controls.layout = make_box_layout()
         
        out_box = widgets.Box([self.output])
        self.output.layout = make_box_layout()
 
        for control in controls.children:
            control.observe(self.update, names=control.description)#'value')
        
        #link = [(c, 'value') for c in controls.children]
        #widgets.jslink(*link)
        
        self.children = [controls, self.output]
    
    def compute_surface(self):
        self.x, self.y, self.Z = make_mesh(
            stream_slope = self.data['stream_slope'],
            nx = self.data['nx'],
            ny = self.data['ny'],
            x_min = self.data['x_range'][0],
            x_max = self.data['x_range'][1],
            y_min = self.data['y_range'][0],
            y_max = self.data['y_range'][1],
            z_min = self.data['z_range'][0],
            z_max = self.data['z_range'][1],
            z_v = self.data['z_v'],
        )
    
    def widgets(self):
        return self.children
    
    def plot_surface(self):
        X, Y = np.meshgrid(self.x, self.y)
        self.ax.plot_surface(X, Y, self.Z)
        self.fig.canvas.draw()
    
    def xyZ(self):
        return self.x, self.y, self.Z
    
    def update(self, change):
        with self.output:
            self.data[self.mapping[change.name]] = change.new
        self.compute_surface()
        self.plot_surface()
         
