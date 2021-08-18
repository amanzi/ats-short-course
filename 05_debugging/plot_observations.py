import sys,os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import colors

def plot(dirname, axs):
    surface_area = 1000
    key = dirname

    df = dict()
    df[dirname] = pd.read_csv(os.path.join(dirname, 'water_balance.dat'), comment='#')

    runoff_key = 'runoff generation [mol d^-1]'
    axs[0].plot(df[key]['time [d]']/365, df[key][runoff_key][:]/55000/surface_area, label='Q', color='r')

    axs[3].plot(df[key]['time [d]']/365, df[key]['rain precipitation [m d^-1]'][:], label='Prain', color='b')
    axs[3].plot(df[key]['time [d]']/365, df[key]['snow precipitation [m d^-1]'][:], label='Psnow', color='c')

    et_key = 'evapotranspiration [m d^-1]'
    axs[1].plot(df[key]['time [d]']/365, df[key][et_key][:], label=f'ET', color='forestgreen')


    df[key]['total water content [mol]'] = df[key]['subsurface water content [mol]'].array \
        + df[key]['surface water content [mol]'].array

    axs[2].plot(df[key]['time [d]']/365, df[key]['total water content [mol]'][:]/55000/surface_area, label='WC', color='k')

def decorate(axs):
    axs[0].set_xlabel('time [y]')
    axs[0].set_ylabel('runoff generated [m d^-1]')
    axs[0].legend()

    axs[1].set_xlabel('time [d]')
    axs[1].set_ylabel('total ET [m d^-1]')
    axs[3].set_ylabel('precipitation [m d^-1]')

    axs[2].set_xlabel('time [y]')
    axs[2].set_ylabel('total water [m]')

if __name__ == '__main__':
    fig = plt.figure(figsize=(14,8))
    axs = fig.subplots(3,1)
    axs = list(axs)
    axs.append(axs[1].twinx())

    dirname = sys.argv[-1]
    plot(dirname, axs)
    decorate(axs)
    plt.tight_layout()
    plt.show()
    




