#!/usr/bin/env python3
import re
import csv
import sys
import os

def parse_socket_diag_output(input_file, output_file):
    # Define regex patterns to extract data
    connection_start_pattern = re.compile(r'=+')
    sport_pattern = re.compile(r'sport\s+:\s+(\d+)')
    dport_pattern = re.compile(r'dport\s+:\s+(\d+)')
    src_ip_pattern = re.compile(r'src ip\s+:\s+([0-9.]+)')
    dst_ip_pattern = re.compile(r'dst ip\s+:\s+([0-9.]+)')
    inode_pattern = re.compile(r'inode\s+:\s+(\d+)')
    cwnd_pattern = re.compile(r'Congestion window:\s+(\d+)')
    rtt_pattern = re.compile(r'RTT:\s+(\d+)\s+microseconds')
    bytes_acked_pattern = re.compile(r'Bytes acked:\s+(\d+)')
    unacked_pattern = re.compile(r'Unacked packets:\s+(\d+)')
    retrans_pattern = re.compile(r'Retransmitted packets:\s+(\d+)')
    total_retrans_pattern = re.compile(r'Total retransmits:\s+(\d+)')
    delivery_rate_pattern = re.compile(r'Delivery rate:\s+(\d+)\s+bytes/s')
    throughput_pattern = re.compile(r'Estimated throughput:\s+([\d.]+)\s+MB/s')
    
    # Define CSV fields (removed timestamp)
    fields = ['connection_id', 'sport', 'dport', 'src_ip', 'dst_ip', 
              'inode', 'cwnd', 'rtt_us', 'bytes_acked', 'unacked', 'retrans', 
              'total_retrans', 'delivery_rate', 'throughput_mbps']
    
    # Open input and output files
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        # Create CSV writer
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        
        # Variables to track current connection data
        current_data = {}
        in_connection = False
        connection_count = 0
        sample_count = 0
        
        # Process each line
        for line in infile:
            line = line.strip()
            
            # Check for sample line (we won't use the timestamp but count samples)
            sample_match = re.search(r'=== Sample (\d+)', line)
            if sample_match:
                sample_count = int(sample_match.group(1))
                continue
            
            # Check for connection start/end
            if connection_start_pattern.match(line):
                # If we were already in a connection, process the previous one
                if in_connection and current_data:
                    # Create connection_id
                    if 'src_ip' in current_data and 'sport' in current_data and 'dst_ip' in current_data and 'dport' in current_data:
                        current_data['connection_id'] = f"{current_data['src_ip']}:{current_data['sport']}-{current_data['dst_ip']}:{current_data['dport']}"
                    
                    # Calculate throughput in Mbps (1 MB/s = 8 Mbps)
                    if 'throughput_mbps' in current_data:
                        try:
                            current_data['throughput_mbps'] = float(current_data['throughput_mbps']) * 8
                        except ValueError:
                            pass
                    
                    # Write the data to CSV
                    writer.writerow(current_data)
                    connection_count += 1
                
                # Start a new connection
                current_data = {}
                in_connection = True
                continue
            
            # Parse connection data if we're in a connection
            if in_connection:
                # Match each pattern and update current_data
                sport_match = sport_pattern.search(line)
                if sport_match:
                    current_data['sport'] = sport_match.group(1)
                    continue
                
                dport_match = dport_pattern.search(line)
                if dport_match:
                    current_data['dport'] = dport_match.group(1)
                    continue
                
                src_ip_match = src_ip_pattern.search(line)
                if src_ip_match:
                    current_data['src_ip'] = src_ip_match.group(1)
                    continue
                
                dst_ip_match = dst_ip_pattern.search(line)
                if dst_ip_match:
                    current_data['dst_ip'] = dst_ip_match.group(1)
                    continue
                
                inode_match = inode_pattern.search(line)
                if inode_match:
                    current_data['inode'] = inode_match.group(1)
                    continue
                
                cwnd_match = cwnd_pattern.search(line)
                if cwnd_match:
                    current_data['cwnd'] = cwnd_match.group(1)
                    continue
                
                rtt_match = rtt_pattern.search(line)
                if rtt_match:
                    current_data['rtt_us'] = rtt_match.group(1)
                    continue
                
                bytes_acked_match = bytes_acked_pattern.search(line)
                if bytes_acked_match:
                    current_data['bytes_acked'] = bytes_acked_match.group(1)
                    continue
                
                unacked_match = unacked_pattern.search(line)
                if unacked_match:
                    current_data['unacked'] = unacked_match.group(1)
                    continue
                
                retrans_match = retrans_pattern.search(line)
                if retrans_match:
                    current_data['retrans'] = retrans_match.group(1)
                    continue
                
                total_retrans_match = total_retrans_pattern.search(line)
                if total_retrans_match:
                    current_data['total_retrans'] = total_retrans_match.group(1)
                    continue
                
                delivery_rate_match = delivery_rate_pattern.search(line)
                if delivery_rate_match:
                    current_data['delivery_rate'] = delivery_rate_match.group(1)
                    continue
                
                throughput_match = throughput_pattern.search(line)
                if throughput_match:
                    current_data['throughput_mbps'] = throughput_match.group(1)
                    continue
        
        # Process the last connection if needed
        if in_connection and current_data:
            # Create connection_id
            if 'src_ip' in current_data and 'sport' in current_data and 'dst_ip' in current_data and 'dport' in current_data:
                current_data['connection_id'] = f"{current_data['src_ip']}:{current_data['sport']}-{current_data['dst_ip']}:{current_data['dport']}"
            
            # Calculate throughput in Mbps (1 MB/s = 8 Mbps)
            if 'throughput_mbps' in current_data:
                try:
                    current_data['throughput_mbps'] = float(current_data['throughput_mbps']) * 8
                except ValueError:
                    pass
            
            # Write the data to CSV
            writer.writerow(current_data)
            connection_count += 1
    
    return connection_count

def main():
    # Check command line arguments
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = "tcp_metrics.csv"
    else:
        # Use default file names
        input_file = "raw.txt"
        output_file = "tcp_metrics.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        print("Usage: python parse_socket_diag.py [input_file] [output_file]")
        sys.exit(1)
    
    # Parse the file
    connection_count = parse_socket_diag_output(input_file, output_file)

if __name__ == "__main__":
    main()
