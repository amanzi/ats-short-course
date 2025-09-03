"""Module containing functions for visualizing and processing mesh data from ATS"""

import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator
import xml.etree.ElementTree as ET


def get_skip_number(filename):
    """ Count the number of lines starting with '#' in a file """
    with open(filename, 'r') as site:
        return sum(1 for line in site if line.startswith('#'))


def plot_subsurface(
    step,
    vis_domain,
    vis_surface,
    variables,
    vmin=None,
    vmax=None,
    cmap="jet",
    aspect=3/1,
    edgecolor="w",
    mesh_linewidth=0.0,
    alpha=0.5,
    figsize=None,
    plot_ponding=False,
    log_scales=False,
    show_colorbar=True,
    upward_separation=5.0,
    distance_outlet=500,
):
    num_plots = len(variables)
    width = 16  # fixed full width
    if figsize is None:
        height_per_subplot = 0.05 * width * aspect
        height = height_per_subplot * num_plots
        figsize = (width, height)

    _, ax = plt.subplots(num_plots, 1, figsize=figsize, sharex=True, sharey=True)

    if num_plots == 1:
        ax = [ax]

    for k, var in enumerate(variables):
        data = vis_domain.get(var, vis_domain.cycles[step])
        # colormap = cmap[k] if cmap and cmap[k] else 'jet'
        colormap = cmap[k] if cmap[k] else 'jet'
        cmin = vmin[k] if vmin and vmin[k] is not None else np.floor(np.nanmin(data))
        cmax = vmax[k] if vmax and vmax[k] is not None else np.ceil(np.nanmax(data))
        log_scale = log_scales[k] if log_scales is not None else False

        # normalization (linear or log)
        if log_scale:
            cmin = 1e-8 if cmin == 0 else cmin
            cmax = cmin*10 if cmax == 0 else cmax
            data[data <= cmin] = cmin  # avoid log(0) and negative values
            norm = LogNorm(vmin=data[data > 0].min(), vmax=data.max())  # avoid log(0)
        else:
            norm = None

        # mesh polygons
        poly = vis_domain.getMeshPolygons(cmap=colormap, linewidth=mesh_linewidth, edgecolor=edgecolor)
        poly.set_array(data)
        ax[k].add_collection(poly)
        poly.set_norm(norm)
        poly.set_clim(cmin, cmax)
        ax[k].set_aspect(aspect)

        elev = vis_surface.get('surface-elevation', vis_domain.cycles[step])
        pd = vis_surface.get('surface-ponded_depth', vis_domain.cycles[step])
        if plot_ponding and k==0:  # plot ponded depth on surface
            ax[k].fill_between(vis_surface.centroids[:,0], upward_separation+elev, upward_separation+elev+pd, color="k", alpha=alpha)
        else:
            ax[k].plot()

        # labels and axes
        ax[k].set_ylabel('Z [m]')
        ax[k].set_xlim([0, distance_outlet])
        ax[k].spines['top'].set_visible(False)
        ax[k].spines['right'].set_visible(False)

        # add colorbar
        if show_colorbar:
            cbar = plt.colorbar(poly, ax=ax[k], shrink=0.75)
            cbar.set_label(var)

    ax[-1].set_xlabel('X [m]')
    plt.show()



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
