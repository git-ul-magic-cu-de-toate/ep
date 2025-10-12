#!/usr/bin/env bash
for js in test1.json test2.json; do
  out="${js%.json}.csv"
  python3 - <<EOF
import json, csv
data = json.load(open('$js'))
with open('$out', 'w', newline='') as w:
    cw = csv.writer(w)
    cw.writerow(['t_s', 'throughput_Mbps'])
    for iv in data.get('intervals', []):
        cw.writerow([iv['sum']['end'], iv['sum']['bits_per_second']/1e6])
print('Wrote', '$out')
EOF
done

