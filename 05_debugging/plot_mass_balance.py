import h5py
import pandas
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker
import sys,os

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', None]
jul_doy = [1,32,61,92,122,153,183,214,245,275,306,336,366]

def plot(data, name, linestyle='-', fig=None, axs=None, legend=True):
    diff = data['P'] + data['SM'] - data['ET'] - data['Q']
    error = np.cumsum(diff) - (data['water'] - data['water'][0])
    max_error = error.max()

    xticks = np.concatenate([np.array(jul_doy), np.array(jul_doy)+365])[1::2]
    xlabels = (months+months)[1::2]

    xlabels = [f"{xl} ({xd})" for (xd, xl) in zip(xticks, xlabels) if xd >= 275 and xd <= 275+365]
    xticks = [xd for xd in xticks if xd >= 275 and xd <= 275+365]

    def format_ticks(value, tick_number):
        val_mod = value % 365
        mo_i = next(i for i in range(len(jul_doy)) if jul_doy[i] > (val_mod + 1)) - 1
        mo = months[mo_i]
        mo_dy = int(np.floor(val_mod + 1 - jul_doy[mo_i]))
        return f"{int(value)} ({mo} {mo_dy})"

    
    # plot
    if fig is None:
        fig = plt.figure()

    nplots = 3
    if 'canopy water' in data:
        nplots = 4

    if axs is None:
        axs = fig.subplots(nplots,1)
        
    # plot surface cumulative
    axs[0].plot(data['time'], np.cumsum(data['P']), linestyle, color='b', label='P')
    axs[0].plot(data['time'], np.cumsum(data['SM']), linestyle, color='darkorange', label='SM')
    axs[0].plot(data['time'], np.cumsum(data['ET']), linestyle, color='forestgreen', label='ET')
    axs[0].plot(data['time'], np.cumsum(data['Q']), linestyle, color='r', label='Q')
    axs[0].plot(data['time'], data['water'] - data['water'][0], linestyle, color='k', label='water')
    axs[0].plot(data['time'], np.cumsum(diff), linestyle, color='gray', label='P+SM-ET-Q')
    axs[0].plot(data['time'], error, '-', color='grey', marker='x', markevery=10, label='error')

    if legend:
        axs[0].legend()
    
    axs[0].set_title(f'mass balance')
    axs[0].xaxis.set_major_formatter(plt.FuncFormatter(format_ticks))
    axs[0].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    axs[0].set_xlabel('time [d]')
    axs[0].set_ylabel('cumulative flux [m]')

    # plot surface fluxes
    axs[1].plot(data['time'], data['P'], linestyle, color='b', label='P')
    axs[1].plot(data['time'], data['S'], linestyle, color='c', label='P_snow')
    axs[1].plot(data['time'], data['SM'], linestyle, color='darkorange', label='SM')
    axs[1].plot(data['time'], data['ET'], linestyle, color='forestgreen', label='ET')
    axs[1].plot(data['time'], data['Q'], linestyle, color='r', label='Q')
    axs[1].plot(data['time'], error[1:] - error[:-1], linestyle, color='grey', label='delta error')
    if legend:
        axs[1].legend()
    axs[1].set_title('fluxes')
    axs[1].set_xlabel('time [d]')
    axs[1].set_ylabel('flux [m / d]')
    axs[1].xaxis.set_major_formatter(plt.FuncFormatter(format_ticks))
    axs[1].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

    diff = data['S'] - data['SM']

    # plot snow cumulative
    axs[2].plot(data['time'], np.cumsum(data['S']), linestyle, color='c', label='P_snow')
    axs[2].plot(data['time'], np.cumsum(data['SM']), linestyle, color='darkorange', label='SM')

    try:
        axs[2].plot(data['time'], np.cumsum(data['E_snow']), linestyle, color='forestgreen', label='E_snow')
        diff = diff - data['E_snow']
    except KeyError:
        pass
    error = np.cumsum(diff) - (data['snow'] - data['snow'][0])
    max_error = error.max()

    axs[2].plot(data['time'], data['snow'], linestyle, color='k', label='snow depth')
    axs[2].plot(data['time'], np.cumsum(diff), linestyle, color='grey', label='P_snow - SM')
    axs[2].plot(data['time'], error, marker='x', markevery=10, color='grey', label='error')
    if legend:
        axs[2].legend()
    axs[2].set_ylabel('cumulative flux (snow) [m]')
    axs[2].set_xlabel('time [d]')
    axs[2].xaxis.set_major_formatter(plt.FuncFormatter(format_ticks))
    axs[2].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))


def load(dirname, delimiter=',', surf_area=None):
    data = dict()
    # surface area
    if surf_area is None:
        d = h5py.File(os.path.join(dirname, 'ats_vis_surface_data.h5'),'r')
        a_key = list(d['surface-cell_volume.cell.0'].keys())[0]
        surf_area = d['surface-cell_volume.cell.0'][a_key][:].sum() # m^2
        d.close()
    data['surf_area'] = surf_area

    # load data
    obs_filename = os.path.join(dirname, 'water_balance.dat')
    df = pandas.read_csv(obs_filename, comment='#', delimiter=delimiter)

    # process
    try:
        data['time'] = df['time [d]']
    except KeyError:
        data['time'] = df['time']
        
    data['P'] = df['rain precipitation [m d^-1]']
    data['SM'] = df['snow melt [m d^-1]']
    data['ET'] = df['evapotranspiration [m d^-1]'] 
    data['Q'] = df['runoff generation [mol d^-1]']/55500./surf_area
    data['water'] = (df['surface water content [mol]'] + df['subsurface water content [mol]']) / 55500 / surf_area

    try:
        data['canopy water'] = df['canopy water content [mol]'] / 55500 / surf_area
        data['I'] = df['canopy interception [m d^-1]']
        data['D'] = df['canopy drainage [m d^-1]']
        data['E_can'] = df['canopy evaporation [m d^-1]']
    except KeyError:
        pass
    
    try:
        data['E_snow'] = df['snow evaporation [m d^-1]']
    except KeyError:
        pass
                        

    data['snow'] = df['snow water content [mol]'] / 55500 / surf_area
    data['S'] = df['snow precipitation [m d^-1]']
    return data

if __name__ == '__main__':
    fig = plt.figure(figsize=(14,8))
    axs = fig.subplots(3,1)

    dirname = sys.argv[1:]
    data = load(dirname)
    plot(data, dirname, '-', fig, axs)
    plt.tight_layout()
    plt.show()
