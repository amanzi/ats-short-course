"""Module containing functions for visualizing and processing mesh data from ATS"""

import os
import numpy as np
import h5py
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator


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
    figsize=(12,6),
    plot_ponding=False,
    log_scales=False,
    show_colorbar=True,
    upward_separation=5.0,
    distance_outlet=500,
):
    """
    Plot subsurface
    """
    num_plots = len(variables)
    fig, ax = plt.subplots(num_plots, 1, figsize=figsize, sharex=True, sharey=True)

    if num_plots == 1:
        ax = [ax]

    for k, var in enumerate(variables):
        data = vis_domain.get(var, vis_domain.cycles[step])
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
        poly = vis_domain.getMeshPolygons(
            cmap=colormap, linewidth=mesh_linewidth, edgecolor=edgecolor
        )
        poly.set_array(data)
        ax[k].add_collection(poly)
        poly.set_norm(norm)
        poly.set_clim(cmin, cmax)
        ax[k].set_aspect(aspect)

        elev = vis_surface.get('surface-elevation', vis_domain.cycles[step])
        pd = vis_surface.get('surface-ponded_depth', vis_domain.cycles[step])
        if plot_ponding and k == 0:  # plot ponded depth on surface
            ax[k].fill_between(
                vis_surface.centroids[:, 0],
                upward_separation + elev,
                upward_separation + elev + pd,
                color="k",
                alpha=alpha,
            )
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
    time = vis_domain.times[step]
    ax[0].text(
        0.95, 0.9,
        f'Time: {time:.2f} (day)',
        transform=ax[0].transAxes,
        ha='right', va='top', fontsize=18,
    )
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])  # adjust top margin    
    # plt.show()


def plot_profiles(
    step,
    vis_domain, vis_surface,
    var_domain="saturation_liquid", unit_domain=None,
    var_surface="surface-ponded_depth", unit_surface=None,
    vmin_domain=None, vmax_domain=None,
    vmin_surface=None, vmax_surface=None,
    grid_surface=True,
    cmap="jet",
    aspect=3/1,
    height_ratios=(1, 2),
    edgecolor="w",
    mesh_linewidth=0.0,
    plot_ponding=True,
    figsize=None,
    log_domain=False,
    log_surface=False,
    show_colorbar=True,
):
    """
    Plot both surface and subsurface profile for each variable
    """    
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(2, 1, height_ratios=height_ratios)
    ax = np.empty(2, dtype=object)

    x = vis_surface.centroids[:, 0]
    data_surface = vis_surface.get(var_surface, vis_domain.cycles[step])
    data_domain = vis_domain.get(var_domain, vis_domain.cycles[step])
    ax[0] = fig.add_subplot(gs[0])
    ax[1] = fig.add_subplot(gs[1], sharex=ax[0])

    # PLOT SURFACE
    cmin = (
        vmin_surface
        if vmin_surface and vmin_surface is not None
        else np.floor(np.nanmin(data_surface))
    )
    cmax = (
        vmax_surface
        if vmax_surface and vmax_surface is not None
        else np.ceil(np.nanmax(data_surface))
    )
    if log_surface:
        positive_data = data_surface[data_surface > 0]
        if len(positive_data) > 0:
            cmin = positive_data.min() if cmin is None else cmin
            cmax = positive_data.max() if cmax is None else cmax
        else:
            # fallback if no positive data
            cmin, cmax = 1e-10, 1e-5        
        ax[0].set_yscale('log')

    data_plot = np.where(data_surface <= 0, np.nan, data_surface)
    ax[0].plot(x, data_plot)
    label = var_surface.replace("surface-", "", 1)
    ax[0].set_ylabel(f'{label} ({unit_surface})')
    xmax = np.max(x)
    xmax_rounded = int(np.ceil(xmax / 100.0) * 100)
    ax[0].set_xlim([0, xmax_rounded])

    if grid_surface:
        ax[0].grid(True, linewidth=0.5, linestyle='--')
    ax[0].set_ylim(max(cmin, 1e-10), cmax)  # ensure lower > 0

    # PLOT SUBSURFACE
    colormap = cmap if cmap else 'jet'
    cmin = (
        vmin_domain
        if vmin_domain and vmin_domain is not None
        else np.floor(np.nanmin(data_domain))
    )
    cmax = (
        vmax_domain
        if vmax_domain and vmax_domain is not None
        else np.ceil(np.nanmax(data_domain))
    )

    # normalization (linear or log)
    if log_domain:
        cmin = 1e-8 if cmin == 0 else cmin
        cmax = cmin*10 if cmax == 0 else cmax
        data_domain[data_domain <= cmin] = cmin  # avoid log(0) and negative values
        norm = LogNorm(vmin=data_domain[data_domain > 0].min(), vmax=data_domain.max())
    else:
        norm = None

    # mesh polygons
    poly = vis_domain.getMeshPolygons(cmap=colormap, linewidth=mesh_linewidth, edgecolor=edgecolor)
    poly.set_array(data_domain)
    ax[1].add_collection(poly)
    poly.set_norm(norm)
    poly.set_clim(cmin, cmax)
    ax[1].set_aspect(aspect)

    # labels and axes
    ax[1].set_ylabel('Z [m]')
    # ax[1].set_ylim([-10, 20])

    if plot_ponding:  # plot ponded depth on surface
        elev = vis_surface.get('surface-elevation', vis_domain.cycles[step])
        pd = vis_surface.get('surface-ponded_depth', vis_domain.cycles[step])        
        ax[1].fill_between(
            vis_surface.centroids[:, 0],
            5 + elev,
            5 + elev + pd,
            color="k",
            alpha=0.5,
        )
    else:
        ax[1].plot()
            
    if show_colorbar:
        cax = fig.add_axes([0.25, 0.0, 0.5, 0.03])
        cbar = fig.colorbar(poly, cax=cax, orientation="horizontal")
        cbar.set_label(f'{var_domain} ({unit_domain})')

    time = vis_domain.times[step]
    ax[1].text(
        0.95, 0.9,
        f'Time: {time:.2f} (day)',
        transform=ax[1].transAxes,
        ha='right', va='top', fontsize=18,
    )

    for k in range(2):
        ax[k].set_xlabel('X [m]')        
        ax[k].spines['top'].set_visible(False)
        ax[k].spines['right'].set_visible(False)


def get_var_names(directory='.', domain=None, filename=None):
    """
    Get variable names from ats results file
    """
    if filename is None:
        if domain is None:
            filename = 'ats_vis_data.h5'
        else:
            filename = f'ats_vis_{domain}_data.h5'
    fname = os.path.join(directory, filename)
    h5f = h5py.File(fname)
    var_names = list(h5f.keys())
    return h5f, var_names


def plot_group(vis_domain, vis_surface, options, data_groups, group_name, step=0):
    """
    Function to call plot profiles
    """
    group = data_groups[group_name]
    params = {**options, **group}
    plot_profiles(
        step=step,
        vis_domain=vis_domain,
        vis_surface=vis_surface,
        var_surface=params["var_surface"],
        unit_surface=params["unit_surface"],
        vmin_surface=params["vmin_surface"],
        vmax_surface=params["vmax_surface"],       
        log_surface=params["log_surface"],

        var_domain=params["var_domain"],
        unit_domain=params["unit_domain"],
        vmin_domain=params["vmin_domain"],
        vmax_domain=params["vmax_domain"],
        log_domain=params["log_domain"],

        cmap=params["cmap"],
        figsize=params["figsize"],
        show_colorbar=params["show_colorbar"],
        aspect=options["aspect"],
        height_ratios=options["height_ratios"],
        plot_ponding=options["plot_ponding"],
    )


def plot_all_domains(vis_domain, vis_surface, options, data_groups, step=0):
    """Plot all subsurface domains."""
    plot_subsurface(
        step,
        vis_domain,
        vis_surface,
        variables=[g["var_domain"] for g in data_groups.values()],
        vmin=[g["vmin_domain"] for g in data_groups.values()],
        vmax=[g["vmax_domain"] for g in data_groups.values()],
        cmap=[g["cmap"] for g in data_groups.values()],
        log_scales=[g["log_domain"] for g in data_groups.values()],
        plot_ponding=[g["plot_ponding"] for g in data_groups.values()],
        aspect=options["aspect"],
        figsize=options["figsize"],
        show_colorbar=options["show_colorbar"]
    )
    

def plot_field_timeseries(time, data, labels, sfactor=1, fontsize=12, xlabel='Time (d)',
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