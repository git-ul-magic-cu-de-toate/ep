#!/usr/bin/env python3
import matplotlib.pyplot as plt
import csv, glob, os

os.makedirs('plots', exist_ok=True)

def read(path):
    t, v = [], []
    with open(path) as f:
        for r in csv.reader(f):
            if r[0].startswith('t_s'): continue
            t.append(float(r[0])); v.append(float(r[1]))
    return t, v

# a) Overlay throughput
plt.figure()
for label, path in [('No bpftune','test1.csv'),
                    ('With bpftune','test2.csv')]:
    t, v = read(path)
    plt.plot(t, v, label=label)
plt.xlabel('Timp (s)')
plt.ylabel('Throughput (Mbps)')
plt.title('Task 2.4 – Impactul bpftune')
plt.legend()
plt.savefig('2.4_throughput.png', dpi=320)
