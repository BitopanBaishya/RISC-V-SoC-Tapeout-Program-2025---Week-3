#!/usr/bin/env python3
import re
from graphviz import Digraph
from pathlib import Path

REPORT = Path("sta_report.txt")
OUTNAME = "timing_graph"   # will produce timing_graph.png

if not REPORT.exists():
    print(f"Error: {REPORT} not found. Put this script in the folder with your sta_report.txt")
    raise SystemExit(1)

text = REPORT.read_text()

# Split the file into path blocks using "Startpoint:" occurrences
blocks = re.split(r'(?=Startpoint:)', text)

# We'll process every block that contains a "Delay    Time   Description" table
processed = 0
for bi, block in enumerate(blocks):
    if "Delay    Time   Description" not in block:
        continue

    processed += 1
    # header info
    start_match = re.search(r'Startpoint:\s*(.+)', block)
    end_match   = re.search(r'Endpoint:\s*(.+)', block)
    start_label = start_match.group(1).strip() if start_match else f"start_{bi}"
    end_label   = end_match.group(1).strip() if end_match else f"end_{bi}"

    # extract data arrival / required times and slack
    darr_match = re.search(r'([+-]?\d+\.\d+)\s+data arrival time', block)
    dreq_match = re.search(r'([+-]?\d+\.\d+)\s+data required time', block)
    slack_match = re.search(r'([+-]?\d+\.\d+)\s+slack', block)

    data_arrival = float(darr_match.group(1)) if darr_match else None
    data_required = float(dreq_match.group(1)) if dreq_match else None
    slack_val = float(slack_match.group(1)) if slack_match else None

    # parse lines between the header and the next dashed line block
    # collect lines that contain a '^' or 'v' (these show pin nodes)
    lines = block.splitlines()
    node_entries = []
    for line in lines:
        if '^' in line or 'v' in line:
            # find which caret exists (choose first occurrence)
            caret = '^' if '^' in line else 'v'
            pos = line.find(caret)
            before = line[:pos].strip()
            after = line[pos+1:].strip()

            # parse delay (first token of 'before' if numeric)
            delay = None
            before_tokens = before.split()
            if before_tokens:
                try:
                    delay = float(before_tokens[0])
                except:
                    delay = None

            # parse node name and optional cell type from 'after'
            # after typically looks like: "_10450_/CLK (sky130_fd_sc_hd__dfxtp_1)"
            node_name = after.split()[0] if after.split() else after
            cell_type = None
            m = re.search(r'\(([^)]+)\)', after)
            if m:
                cell_type = m.group(1)

            node_entries.append({
                "raw_line": line.strip(),
                "caret": caret,
                "node": node_name,
                "cell": cell_type,
                "delay": delay
            })

    # Build graph
    dot = Digraph(comment=f"Timing Path {processed}", format="png")
    dot.attr(rankdir="LR", fontsize="10")

    # Title/label summary on graph
    title_items = [f"Start: {start_label}", f"End: {end_label}"]
    if data_arrival is not None:
        title_items.append(f"DataArrival={data_arrival:.3f} ns")
    if data_required is not None:
        title_items.append(f"DataRequired={data_required:.3f} ns")
    if slack_val is not None:
        title_items.append(f"Slack={slack_val:.3f} ns")
    graph_label = "  |  ".join(title_items)
    dot.attr(label=graph_label, labelloc="t", labeljust="l")

    # add nodes (use nice display: node name + short cell + delay)
    for i, ent in enumerate(node_entries):
        nodeid = f"n{i}"
        label_lines = [ent["node"]]
        if ent["cell"]:
            label_lines.append(ent["cell"])
        if ent["delay"] is not None:
            label_lines.append(f"delay {ent['delay']:.3f} ns")
        label = "\n".join(label_lines)

        # color flip-flops differently (heuristic: cell name contains 'dfx' or 'dff' or 'latch')
        fillcolor = "#D6EAF8"  # default light-blue
        if ent["cell"]:
            c = ent["cell"].lower()
            if any(k in c for k in ("dfx", "dff", "flop", "latch")):
                fillcolor = "#F9E79F"  # yellow for flops
            elif "inv" in c or "buf" in c:
                fillcolor = "#ABEBC6"  # green for buffers/inverters
            else:
                fillcolor = "#D6EAF8"

        dot.node(nodeid, label=label, shape="box", style="filled,rounded", fillcolor=fillcolor)

    # add edges with optional edge labels (we'll label an edge with the delay of the destination node)
    for i in range(len(node_entries)-1):
        src = f"n{i}"
        dst = f"n{i+1}"
        dst_delay = node_entries[i+1].get("delay")
        elabel = f"{dst_delay:.3f} ns" if dst_delay is not None else ""
        dot.edge(src, dst, label=elabel)

    # Render file name per path (append index)
    outfile = f"{OUTNAME}_{processed}"
    dot.render(outfile, cleanup=True)
    print(f"Generated: {outfile}.png (Start:{start_label} End:{end_label} Slack:{slack_val})")

if processed == 0:
    print("No path blocks found in the report. Make sure the report includes full 'Delay    Time   Description' tables.")

