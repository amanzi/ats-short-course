"""Module containing functions for visualizing and processing mesh data from ATS"""

import numpy as np
import geopandas as gpd
import h5py
from pyproj.crs import CRS
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize, LogNorm
from matplotlib.patches import Polygon  # Use this instead of PolygonPatch
from matplotlib.ticker import MultipleLocator
import xml.etree.ElementTree as ET

import shapely
import colorcet as cc
import pyvista as pv
import vtk
vtk.vtkObject.GlobalWarningDisplayOff()


def daymet_crs():
    """Returns the CRS used by DayMet files, but in m, not km.

    Returns
    -------
    out : crs-type
        The DayMet CRS.  The user should not care what this is.

    """
    # old proj: return from_string('+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs ')
    # new proj...
    return CRS.from_string(
        '+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs'
    )


def GetMeshPolygons(mfile=None):
    """This functions read mesh from h5 files
    
    Returns
    -------
    polygons:
        List of element in polygon format

    """
    # Read mesh file to extract the coordinates of the nodes
    fn = h5py.File(mfile, 'r')

    # Get group info
    group = fn["/0"]
    node_coor = group['Mesh']['Nodes'][:]
    group['Mesh'].keys()
    elems_mixed = group['Mesh']['MixedElements'][:]
    num_elems = group['Mesh']['ElementMap'].shape[0]

    # Loop to extract the index of the nodes that form each element
    elem_type = np.zeros(num_elems)
    mesh_topology = np.zeros((num_elems, 5))
    for i in range(num_elems):
        elem_type[i] = elems_mixed[0]
        if elem_type[i] == 4:
            mesh_topology[i, 0:3] = elems_mixed[1:4].flatten()
            # Remove elements from elems_mixed
            elems_mixed = elems_mixed[4:]
        elif elem_type[i] == 5:
            mesh_topology[i, 0:4] = elems_mixed[1:5].flatten()
            # Remove elements from elems_mixed
            elems_mixed = elems_mixed[5:]
        elif elem_type[i] == 3:
            mesh_topology[i, 0:5] = elems_mixed[2:7].flatten()
            # Remove elements from elems_mixed
            elems_mixed = elems_mixed[7:]

    # Extract the unique nodes
    noodes_unique = np.unique(mesh_topology.flatten())

    # convert to integer
    noodes_unique = noodes_unique.astype(int)

    # Get node coordinates
    node_coors = node_coor[noodes_unique, :]

    polygons = []
    for i in range(mesh_topology.shape[0]):
        # Extract the coordinates of the nodes that form the element
        nodes = mesh_topology[i, :]

        # Replace by -1 the zeros in column 4 and 5. This is done since there are some elements with node id equal to zero
        nodes[-2:][nodes[-2:] == 0] = -1

        # Remove the -1
        nodes = nodes[nodes != -1]
        nodes_elem_coors = node_coor[nodes.astype(int), :]

        # Create a polygon
        polygon = shapely.geometry.Polygon(nodes_elem_coors)
        polygons.append(polygon)

    return polygons


def PlotPolygonsFields(polygons, field, cmap='jet', alpha=1, lw=1, edgecolor='k',
                       vmin=None, vmax=None, label=None, colorbar=False, logscale=False,
                       showbox=True, ax=None):
    """
    Plots Shapely polygons with colors based on the provided field values.
    """
    if len(polygons) != len(field):
        raise ValueError("Each polygon must correspond to a field value.")

    if vmin is None:
        vmin = min(field)
    if vmax is None:
        vmax = max(field)
    if vmax < vmin:
        vmax = vmin*2

    if ax is None:
        _, ax = plt.subplots()

    ax.set_aspect('equal')
    norm = LogNorm(vmin=vmin, vmax=vmax) if logscale else Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.get_cmap(cmap)

    patches = []

    for polygon, fieldval in zip(polygons, field):
        nodes = np.array(polygon.exterior.xy).T  # Get the exterior coordinates
        patch = Polygon(nodes, closed=True, alpha=alpha, linewidth=lw, edgecolor=edgecolor)
        patches.append(patch)
        patch.set_facecolor(cmap(norm(fieldval)))

    for patch in patches:
        ax.add_patch(patch)

    if colorbar:
        # Add colorbar if needed
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        if showbox:
            cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1)
        else:
            cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.01)

        if logscale:
            # For logscale, show all values from vmin to vmax
            range_size = int(np.log10(vmax)) - int(np.log10(vmin)) + 1
            step = 2 if range_size > 5 and range_size % 2 == 1 else 1
            ticks = [pow(10, i) for i in range(
                int(np.log10(vmin)),
                int(np.log10(vmax))+1,
                step
            )]
            cbar.set_ticks(ticks)
        else:
            # Make colorbar ticks smarter for linear scale
            cbar.set_ticks(np.linspace(vmin, vmax, 5))
            cbar.update_ticks()

        if label is not None:
            cbar.set_label(label)
    plt.tight_layout()


def get_skip_number(filename):
    """ Count the number of lines starting with '#' in a file """
    with open(filename, 'r') as site:
        return sum(1 for line in site if line.startswith('#'))


def get_cmap(name):
    """
    Returns a colormap based on the given variable name.

    Args:
        name (str): The name of the variable for which to get a colormap.

    Returns:
        matplotlib.colors.Colormap: The colormap object corresponding to the input name.
        If the name is not found in the predefined dictionary, it returns the 'jet' colormap as default.
    """
    if isinstance(name, list):
        return 'jet'

    cmap_dict = {
        'elevation': 'terrain',
        'ponded_depth': cc.cm.CET_L17,
        'surface_subsurface_flux': 'seismic',
        'pressure': cc.cm.CET_R4,
        'pres_elev': cc.cm.CET_R4,
    }
    return cmap_dict.get(name, 'jet')


def get_boundary_polygons(surface_polys):
    """Get the outer boundary of a collection of surface polygons.

    Args:
        surface_polys (list): List of surface polygons

    Returns:
        GeoDataFrame: Single polygon representing the outer boundary
    """
    gdf = gpd.GeoDataFrame(geometry=surface_polys)
    gdf.crs = daymet_crs()
    gdf_union = gdf.union_all()
    return gpd.GeoDataFrame(crs=gdf.crs, geometry=[gdf_union])


def format_box(ax, gdf_clip, showbox, colorbox):
    """Format plot axes with consistent styling.

    Args:
        ax: Matplotlib axis object
        gdf_clip: GeoDataFrame with boundary information
        showbox (bool): Whether to show the axis box and labels
        colorbox (str): Color for the axis box
    """
    ax.set_aspect('equal')
    if showbox:
        ax.spines['top'].set_color(colorbox)
        ax.spines['bottom'].set_color(colorbox)
        ax.spines['left'].set_color(colorbox)
        ax.spines['right'].set_color(colorbox)
        ax.tick_params(axis='both', which='major', labelsize=7)            
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        xmin, ymin, xmax, ymax = gdf_clip.total_bounds
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
    else:
        ax.set_axis_off()


def plot_surface(variables, poly_surface, vis_surface, step, time, domain='surface',
                 vmin=None, vmax=None, cmap=None, units=None, logscales=None, figsize=None,
                 colorbox='whitesmoke', showbox=True):
    """
    Plot surface variables on a mesh.

    Args:
        variables (list): List of variable names to plot.
        poly_surface (list): List of polygon geometries.
        vis_surface: Visualization data object.
        step (int): Time step index for data.
        vmin (list, optional): List of minimum values for color scaling.
        vmax (list, optional): List of maximum values for color scaling.
        cmap (list, optional): List of colormaps for each variable.
    """
    
    num_plots = len(variables)
    if figsize is None:
        figsize = (4*num_plots, 6)

    _, ax = plt.subplots(1, num_plots, figsize=figsize)
    plt.suptitle(f'Time: {time[step]/vis_surface.time_factor} {vis_surface.time_unit}', fontsize=16)

    if num_plots == 1:
        ax = [ax]

    # Plot each variable
    gdf_clip = get_boundary_polygons(poly_surface)
    for k, var in enumerate(variables):
        if isinstance(var, list):
            data1 = vis_surface.getArray(domain+'-'+var[0])[step, :]
            data2 = vis_surface.getArray(domain+'-'+var[1])[step, :]
            data = data1 * data2
            ax[k].set_title(f'{var[0]} * {var[1]}', y=1.0, fontsize=14)
        else:
            data = vis_surface.getArray(domain+'-'+var)[step, :]
            ax[k].set_title(var, y=1.0, fontsize=12)

        colormap = cmap[k] if cmap and cmap[k] else get_cmap(var)
        cmin = vmin[k] if vmin and vmin[k] is not None else np.floor(np.nanmin(data))
        cmax = vmax[k] if vmax and vmax[k] is not None else np.ceil(np.nanmax(data))
        unit = units[k] if units is not None else None
        logscale = logscales[k] if logscales is not None else False
        if logscale:
            cmin = 1e-8 if cmin == 0 else cmin
            cmax = cmin*10 if cmax == 0 else cmax
        PlotPolygonsFields(poly_surface, data, cmap=colormap, vmin=cmin, vmax=cmax, lw=0.2,
                           ax=ax[k], label=unit, colorbar=True, logscale=logscale, showbox=showbox)
        format_box(ax[k], gdf_clip, showbox, colorbox)
        gdf_clip.plot(ax=ax[k], color="None", edgecolor='k', lw=1)


def plot_domain(variables, poly_surface, vis_domain, num_surface_elements, step, time, layer,
                vmin=None, vmax=None, cmap=None, units=None, logscale=False, figsize=None,
                colorbox='whitesmoke', showbox=True):
    """
    Plot domain variables on a mesh.

    Args:
        variables (list): List of variable names to plot.
        poly_surface (list): List of polygon geometries.
        vis_domain: Visualization data object.
        step (int): Time step index for data.
        vmin (list, optional): List of minimum values for color scaling.
        vmax (list, optional): List of maximum values for color scaling.
        cmap (list, optional): List of colormaps for each variable.
    """

    num_plots = len(variables)
    num_steps = len(vis_domain.cycles)
    num_layers = int(np.shape(vis_domain.centroids)[0] / num_surface_elements)

    if figsize is None:
        figsize = (4*num_plots, 6)

    _, ax = plt.subplots(1, num_plots, sharex=True, sharey=True, figsize=figsize)
    plt.suptitle(f'Time: {time[step]/vis_domain.time_factor} {vis_domain.time_unit}', fontsize=16)

    if num_plots == 1:
        ax = [ax]

    gdf_clip = get_boundary_polygons(poly_surface)
    for k, var in enumerate(variables):
        data = vis_domain.getArray(var).reshape(
            num_steps, num_surface_elements, num_layers)[step, :, layer]

        colormap = cmap[k] if cmap and cmap[k] else get_cmap(var)
        cmin = vmin[k] if vmin and vmin[k] is not None else np.floor(np.nanmin(data))
        cmax = vmax[k] if vmax and vmax[k] is not None else np.ceil(np.nanmax(data))
        unit = units[k] if units is not None else None

        PlotPolygonsFields(poly_surface, data, cmap=colormap, vmin=cmin, vmax=cmax, lw=0.2,
                           ax=ax[k], label=unit, colorbar=True, logscale=logscale, showbox=showbox)
        ax[k].set_title(var, y=1, fontsize=12)
        format_box(ax[k], gdf_clip, showbox, colorbox)
        gdf_clip.plot(ax=ax[k], color="None", edgecolor='k', lw=1)


def plot_sources(time, data, label=None, sfactor=1, color='dimgray', fontsize=12, xlabel=None,
                 ylabel=None, title=None, legend=False, yscale=0.2, ax=None):
    """Plot source data (like rainfall and tracer injection) on a secondary y-axis.

    Parameters
    ----------
    time : array-like
        Time values for x-axis
    data : array-like
        Source data to plot
    label : str
        Label for the data series
    sfactor : float, optional
        Scale factor for data values, default=1
    color : str, optional
        Color for the plot, default='dimgray'
    fontsize : int, optional
        Font size for labels, default=12
    xlabel, ylabel : str, optional
        Axis labels
    title : str, optional
        Plot title
    legend : bool, optional
        Whether to show legend, default=False
    yscale : float, optional
        Y-axis scale factor, default=0.2
    ax : matplotlib.axes.Axes, optional
        Primary axis to attach secondary axis to

    Returns
    -------
    matplotlib.axes.Axes
        The secondary axis containing the plot
    """
    # Add second y-axis
    axs = ax.twinx()
    axs.fill_between(time, data * sfactor, color=color, label=label, step='mid')
    if xlabel is not None:
        axs.set_xlabel(xlabel, fontsize=fontsize)
    if ylabel is not None:
        axs.set_ylabel(ylabel, fontsize=fontsize)    
    if title is not None:
        axs.set_title(title, fontsize=fontsize)

    axs.invert_yaxis()
    max_val = np.max(data)
    magnitude = 10 ** np.floor(np.log10(max_val))
    max_val = np.ceil(max_val / magnitude) * magnitude
    axs.set_ylim(max_val/yscale, 0)  # Reversed since axis is inverted    
    yticks = np.arange(0, 2*max_val + max_val/2, max_val/2)
    axs.set_yticks(yticks)
    axs.set_yticklabels([f'{int(y)}' for y in yticks])
    if max_val >= 1000:  # Only use scientific notation for large numbers
        axs.yaxis.set_major_formatter(plt.ScalarFormatter())
        axs.yaxis.get_major_formatter().set_scientific(True)
        axs.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    if legend:
        axs.legend(fontsize=fontsize, frameon=True)

    return axs


def plot_field_timeseries(time, data, labels, sfactor=1, fontsize=12, xlabel='Time (hr)',
                          ylabel=None, title=None, legend=True, ylim=None, logscale=False, ax=None):
    """Plot time series data for multiple fields on a single axis.

    Parameters
    ----------
    time : array-like
        Time values for x-axis
    data : list of array-like
        List of data arrays to plot
    labels : list of str
        Labels for each data series
    sfactor : float, optional
        Scale factor to apply to data values, default=1
    fontsize : int, optional
        Base font size for plot text, default=12
    xlabel : str, optional
        Label for x-axis, default='Time (hr)'
    ylabel : str, optional 
        Label for y-axis, default=None
    title : str, optional
        Plot title, default=None
    legend : bool, optional
        Whether to show legend, default=True
    ylim : tuple, optional
        Y-axis limits (min, max), default=None
    ax : matplotlib.axes.Axes, optional
        Axes to plot on, creates new axes if None

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the plot
    """
    # Create a new axis if none is provided
    if ax is None:
        ax = plt.gca()
    for label, field in zip(labels, data):
        ax.plot(time, field * sfactor, label=label, linewidth=2)

    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize+2)

    ax.tick_params(axis='both', labelsize=fontsize)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    if ylim is not None:
        ax.set_ylim(ylim)

    max_val = np.max(data)
    if max_val >= 1000 or max_val < 0.01:  # Use scientific notation for large and very small numbers
        ax.yaxis.set_major_formatter(plt.ScalarFormatter())
        ax.yaxis.get_major_formatter().set_scientific(True)
        ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    if logscale:
        ax.set_yscale('log')
    ax.grid(True, linestyle='--', alpha=0.5)

    if legend:
        ax.legend(loc='center left', fontsize=fontsize, frameon=True)
    
    return ax


def load_mesh_exodus(mesh_file, z_scale=1.0):
    """
    Load and process an Exodus mesh file, applying optional z-axis scaling.

    Args:
        mesh_file (str): Path to the Exodus mesh file to load
        z_scale (float, optional): Scaling factor to apply to z-coordinates. Defaults to 1.0.

    Returns:
        pyvista.UnstructuredGrid: The processed mesh with scaled z-coordinates
    """
    mesh = pv.read(mesh_file)
    combined_mesh = mesh.combine()
    z_values = combined_mesh.points[:, 2]  # Z values are in the 3rd column
    combined_mesh["Elevation"] = z_values
    domain_mesh = combined_mesh.warp_by_scalar(scalars="Elevation", factor=z_scale)
    return domain_mesh


def toggle_pick_callback(point, plotter):
    """
    Toggle the visibility of a point label in the plotter.

    This function is used as a callback for point picking in a 3D visualization.
    It either adds a new label for a picked point or removes an existing label
    if the point has been picked before.

    Args:
        point (tuple): The 3D coordinates of the picked point.
        plotter: The plotter object used for visualization.

    Global Variables:
        picked_points_labels (dict): A dictionary to store point labels.
    """
    point_key = tuple(point)

    # Check if the point already has a label
    global picked_points_labels

    if 'picked_points_labels' not in globals():
        picked_points_labels = {}

    if point_key in picked_points_labels:
        # If it exists, remove the label
        plotter.remove_actor(picked_points_labels[point_key])
        del picked_points_labels[point_key]
    else:
        # Create a new label at the picked point
        label = plotter.add_point_labels(
            [point],
            [f"{point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f}"],
            font_size=12,
            point_color="red",
            text_color="white",
            fill_shape=True
        )
        # Store the label in the dictionary
        picked_points_labels[point_key] = label


def plot_mesh(domain_mesh, opacity=1, show_edges=True, show_scalar_bar=True, pickable=True,
              show_zlabels=False, cmap='terrain_r', show_toplayer=False, normal=None, clim=None,
              window_size=None, link_views=True, view_isometric=False, set_background=True,
              lighting=False):
    """
    Plot a 3D mesh with interactive point picking capabilities.

    Args:
        domain_mesh: The PyVista mesh object to be plotted
        show_edges (bool, optional): Whether to display mesh edges. Defaults to True.
        show_scalar_bar (bool, optional): Whether to show the scalar bar. Defaults to True.
        pickable (bool, optional): Whether to enable point picking. Defaults to True.
        show_zlabels (bool, optional): Whether to show Z-axis labels. Defaults to False.
        window_size (list, optional): Window dimensions [width, height]. Defaults to [1200, 800].

    The function creates an interactive 3D visualization where users can:
    - Click points to toggle coordinate labels
    - View mesh edges if enabled
    - See elevation data via a scalar bar if enabled
    - Interact with the mesh using standard PyVista controls
    """
    if normal is None:
        normal = [0, 0, 1]

    if window_size is None:
        window_size = [640, 480]

    if show_toplayer:
        # toplayer_mesh = domain_mesh.slice(normal=normal)
        zmax = domain_mesh.bounds[5]  # Get maximum z-coordinate from mesh bounds
        toplayer_mesh = domain_mesh.extract_surface().project_points_to_plane(normal=normal)
        toplayer_mesh.points[:, 2] = zmax  # Set Z coordinates to match domain_mesh max height
        shape = (1, 2)
    else:
        shape = (1, 1)

    sargs = dict(height=0.25, vertical=True, position_x=0.05, position_y=0.05)

    pl = pv.Plotter(window_size=window_size, shape=shape)
    picked_points_labels = {}
    pl.add_mesh(
        domain_mesh,
        opacity=opacity,
        lighting=lighting,
        show_edges=show_edges,
        pickable=pickable,
        show_scalar_bar=show_scalar_bar,
        scalar_bar_args=sargs,
        cmap=cmap,
        clim=clim,
    )

    if show_toplayer:
        pl.subplot(0, 1)
        pl.add_mesh(
            toplayer_mesh,
            show_edges=show_edges,
            pickable=pickable,
            show_scalar_bar=True,
            color='white',
            smooth_shading=True,
        )

    # pl.add_scalar_bar(vertical=True, title="Elevation", n_labels=5)
    pl.enable_surface_point_picking(
        callback=lambda point: toggle_pick_callback(point, pl),
        show_point=False,
        picker='point',
    )

    pl.show_bounds(show_zlabels=show_zlabels)
    if link_views:
        pl.link_views()
    if view_isometric:
        pl.view_isometric()
    if set_background:
        pl.set_background("royalblue", top="aliceblue")    
    pl.show()
    return pl


def get_rainfall_from_xml(xml_file, time_obs, sfactor=1, parameter='surface-water_source'):
    """Extract rainfall data from an XML file and convert to observation times.

    Parameters
    ----------
    xml_file : str
        Path to XML file containing rainfall data
    time_obs : array-like
        Observation time points to interpolate rainfall to
    sfactor : float, optional
        Scale factor to apply to rainfall values, default=1

    Returns
    -------
    array-like
        Rainfall values interpolated to observation times
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    water_source = root.find(f".//ParameterList[@name='{parameter}']")
    function = water_source.find(".//ParameterList[@name='function-tabular']")
    x_time = [float(x) for x in function.find("Parameter[@name='x values']").attrib['value'].strip('{}').split(',')]
    y_values = [float(y) for y in function.find("Parameter[@name='y values']").attrib['value'].strip('{}').split(',')]
    num_time = len(x_time)

    x_time = np.array(x_time)/3600
    n = len(time_obs)
    rainfall = np.zeros(n)
    for i in range(num_time-1):
        rainfall[(time_obs >= x_time[i]) & (time_obs <= x_time[i+1])] = y_values[i] * sfactor

    return rainfall


def get_tracer_source_from_xml(xml_file, time_obs, sfactor=1, parameter='source terms'):
    """Extract tracer source data from an XML file and convert to observation times.

    Parameters
    ----------
    xml_file : str
        Path to XML file containing tracer source data
    time_obs : array-like
        Observation time points to interpolate source values to
    sfactor : float, optional
        Scale factor to apply to source values, default=1

    Returns
    -------
    array-like
        Tracer source values interpolated to observation times
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Navigate to the tracer source section
    source_terms = root.find(f".//ParameterList[@name='{parameter}']")
    function = source_terms.find(".//ParameterList[@name='function-tabular']")
    
    # Extract time and value arrays
    x_time = [float(x) for x in function.find("Parameter[@name='x values']").attrib['value'].strip('{}').split(',')]
    y_values = [float(y) for y in function.find("Parameter[@name='y values']").attrib['value'].strip('{}').split(',')]
    num_time = len(x_time)

    # Convert time to hours
    x_time = np.array(x_time)/3600

    # Interpolate to observation times
    n = len(time_obs)
    source = np.zeros(n)
    for i in range(num_time-1):
        source[(time_obs >= x_time[i]) & (time_obs <= x_time[i+1])] = y_values[i] * sfactor

    return source
