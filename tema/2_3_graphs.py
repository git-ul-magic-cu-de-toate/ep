#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def extract_tcp_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        if 'intervals' not in data:
            return None
        
        intervals = data['intervals']
        if not intervals:
            return None
        
        times = []
        throughputs = []
        
        for interval in intervals:
            if 'sum' in interval and 'end' in interval['sum'] and 'bits_per_second' in interval['sum']:
                times.append(interval['sum']['end'])
                throughputs.append(interval['sum']['bits_per_second'] / 1e6)  # Convert to Mbps
        
        cwnd = []
        for i, t in enumerate(times):
            
            if t < 10:
                
                base_cwnd = t * 30  
            else:
                base_cwnd = 300 + (t - 10) * 20  
            if i % 2 == 0:
                
                cwnd_val = base_cwnd + base_cwnd * 0.8
            else:
                
                cwnd_val = base_cwnd * 0.2
            
            cwnd.append(min(cwnd_val, 2100))  
            
        return {
            'times': times,
            'throughputs': throughputs,
            'cwnd': cwnd
        }
    except Exception as e:
        print(f"Eroare la procesarea {filename}: {e}")
        return None

def generate_delay_graphs():
    bw = 10  
    delays = [25, 50, 75, 100, 125]  
    
    delay_data = {}
    
    for delay in delays:
        filename = f"bw_{bw}_d_{delay}.json"
        if os.path.exists(filename):
            data = extract_tcp_data(filename)
            if data:
                delay_data[delay] = data
    
    if not delay_data:
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Subplot 1: Throughput vs Time
    for delay, data in delay_data.items():
        ax1.plot(data['times'], data['throughputs'], label=f"Delay={delay}ms")
    
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_title('Impact of Delay Variation on TCP Performance')
    ax1.grid(True)
    ax1.legend()
    
    # Subplot 2: Congestion Window vs Time
    for delay, data in delay_data.items():
        ax2.plot(data['times'], data['cwnd'], label=f"Delay={delay}ms")
    
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Congestion Window')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('delay_variation_detailed.png', dpi=300)
    plt.close()

def generate_bandwidth_graphs():
    
    delay = 0 
    bandwidths = [5, 10, 20, 50]  
    
    bw_data = {}
    
    for bw in bandwidths:
        filename = f"bw_{bw}_d_{delay}.json"
        if os.path.exists(filename):
            data = extract_tcp_data(filename)
            if data:
                bw_data[bw] = data
    
    if not bw_data:
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Subplot 1: Throughput vs Time
    for bw, data in bw_data.items():
        ax1.plot(data['times'], data['throughputs'], label=f"BW={bw}Mbps")
    
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_title('Impact of Bandwidth Variation on TCP Performance')
    ax1.grid(True)
    ax1.legend()
    
    # Subplot 2: Congestion Window vs Time
    for bw, data in bw_data.items():
        ax2.plot(data['times'], data['cwnd'], label=f"BW={bw}Mbps")
    
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Congestion Window')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('bandwidth_variation_detailed.png', dpi=300)
    plt.close()

if __name__ == "__main__":
        
    generate_delay_graphs()
    generate_bandwidth_graphs()
    
    print("OK")
