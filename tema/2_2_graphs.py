import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy.interpolate import interp1d

df = pd.read_csv('tcp_metrics.csv')

if 'timestamp' in df.columns:
    df['time'] = df['timestamp'] - df['timestamp'].min()
else:
    df['time'] = range(len(df))

dense_time = np.linspace(df['time'].min(), df['time'].max(), 500)

throughput_interp = interp1d(df['time'], df['throughput_mbps'], kind='linear')
cwnd_interp = interp1d(df['time'], df['cwnd'], kind='linear')

dense_throughput = throughput_interp(dense_time)
dense_cwnd = cwnd_interp(dense_time)

plt.figure(figsize=(12, 10))
gs = GridSpec(2, 1, height_ratios=[1, 1], hspace=0.3)

ax1 = plt.subplot(gs[0])
ax1.plot(dense_time, dense_throughput, 'b-', linewidth=1.5)
ax1.set_ylabel('Throughput (Mbps)')
ax1.set_title('TCP Performance: tcp_test.csv')
ax1.grid(True)
ax1.set_xlim(0, df['time'].max())
ax1.set_ylim(0, max(dense_throughput) * 1.1)  # 10% marjă

ax2 = plt.subplot(gs[1])
ax2.plot(dense_time, dense_cwnd, 'r-', linewidth=1.5)
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Congestion Window')
ax2.grid(True)
ax2.set_xlim(0, df['time'].max())
ax2.set_ylim(0, max(dense_cwnd) * 1.1)  # 10% marjă

ss_end = 5
ca_end = 20
if df['time'].max() > ss_end:
    ax1.axvline(x=ss_end, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=ss_end, color='gray', linestyle='--', alpha=0.5)
if df['time'].max() > ca_end:
    ax1.axvline(x=ca_end, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=ca_end, color='gray', linestyle='--', alpha=0.5)

if df['time'].max() > ss_end and df['time'].max() > ca_end:
    ax1.text(ss_end/2, ax1.get_ylim()[1]*0.9, 'Slow Start', ha='center', bbox=dict(facecolor='white', alpha=0.7))
    ax1.text((ss_end+ca_end)/2, ax1.get_ylim()[1]*0.9, 'Congestion\nAvoidance', ha='center', bbox=dict(facecolor='white', alpha=0.7))
    ax1.text((ca_end+df['time'].max())/2, ax1.get_ylim()[1]*0.9, 'AIMD\nSteady State', ha='center', bbox=dict(facecolor='white', alpha=0.7))

plt.savefig('tcp_performance.png', dpi=300, bbox_inches='tight')

plt.show()
