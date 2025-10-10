# Week 3: Post Synthesis GLS and STA Fundamentals
 
The focus of this week is 

---

## 📜 Table of Contents
[📋 Prerequisites](#-prerequisites) <br>
[1. Gate-Level Simulation (GLS) of VSDBabySoC](#1-gate-level-simulation-gls-of-vsdbabysoc)<br>
[2. Fundamentals of Static Timing Analysis (STA)](#2-fundamentals-of-static-timing-analysis-sta)<br>

---

## 📋 Prerequisites
- Basic understanding of Verilog codes.
- Basic understanding of Linux commands.
- Successful installation of the tools shown in [Week 0.](https://github.com/BitopanBaishya/VSD-Tapeout-Program-2025---Week-0.git)
- Successful Pre-Synthesis Simulation of BabySoC in [Week 2.](https://github.com/BitopanBaishya/RISC-V-SoC-Tapeout-Program-2025---Week-2/blob/a1a81dd4416dbe5e51e05d8c87ce1f84db3291a2/README.md)

---

## 1. Gate-Level Simulation (GLS) of VSDBabySoC.
> [!TIP]
> Before diving into the Post-Synthesis Simulation of the VSDBabySoC, let’s first recall what synthesis and GLS mean in the SoC design flow.
> ### What is Synthesis?
> Synthesis is the process of converting the RTL (Register Transfer Level) description of a design — written in Verilog or VHDL — into a gate-level netlist. In simpler terms, it translates human-readable logic into a network of standard cells (like AND, OR, DFF, etc.) available in a specific technology library.<br>
> This step ensures that the design is now represented in a form that can actually be fabricated on silicon. The synthesis tool (like Yosys) optimizes the RTL logic to meet the required constraints such as area, power, and timing, and outputs a gate-level Verilog file (`netlist.v`) along with synthesis logs and reports.
> ### What is Gate-Level Simulation (GLS)?
> Once synthesis is done, we need to verify that the synthesized netlist still behaves the same way as the RTL description. This is done through Gate-Level Simulation (GLS).<br>
> GLS involves simulating the gate-level netlist (post-synthesis Verilog file) with the same testbench used for RTL simulation. This helps us confirm:
> * The logical functionality of the synthesized circuit matches the RTL.
> * The design is free from synthesis-induced issues like uninitialized nets, mismatched ports, or incorrect optimizations.
>
> To revise RTL Synthesis in detail, visit [here.](https://github.com/BitopanBaishya/RISC-V-SoC-Tapeout-Program-2025---Week-1/blob/39ab28880dd3ad3f48bbed38bf4fd0e14b621c49/Day%201/README.md#3-introduction-to-synthesis-netlist-yosys-and-frontend-libraries)
> To revise GLS in detail, visit [here.](https://github.com/BitopanBaishya/RISC-V-SoC-Tapeout-Program-2025---Week-1/blob/375e2128e691f2ef6fc6c438972b87ab7c131df6/Day%204/README.md)

### <ins>1. Synthesis of the Netlist.</ins>
1. **Step 1: Navigate to Module Directory & Launch Yosys**<br>
   Change the current directory to where the Verilog source files are located and start the Yosys synthesis tool.
   ```
   cd [path to your VSDBabySoC directory]/VSDBabySoC/src/module/
   yosys
   ```
   <div align="center">
     <img src="Images/1.png" alt="Alt Text" width="1000"/>
   </div>
2. **Step 2: Read Verilog Source Files**<br>
   Load the Verilog design files into Yosys for synthesis. The `-I` option specifies an additional include directory for any header or included files.
   ```
   read_verilog -I [path to your VSDBabySoC directory]/VSDBabySoC/src/include vsdbabysoc.v rvmyth.v clk_gate.v
   ```
   <div align="center">
     <img src="Images/2.png" alt="Alt Text" width="1000"/>
   </div>   
3. **Step 3: Load Standard Cell Libraries**<br>
   Import the Liberty format (`.lib`) timing and cell information files for the different modules and the target technology. These libraries provide Yosys with cell definitions, delays, and drive strengths for synthesis and mapping.
   ```
   read_liberty -lib [path to your VSDBabySoC directory]/VSDBabySoC/src/lib/avsdpll.lib
   read_liberty -lib [path to your VSDBabySoC directory]/VSDBabySoC/src/lib/avsddac.lib
   read_liberty -lib [path to your VSDBabySoC directory]/VSDBabySoC/src/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
   ```
   <div align="center">
     <img src="Images/3.png" alt="Alt Text" width="1000"/>
   </div>   
4. **Step 4: Synthesize Top Module**<br>
   Perform RTL-to-gate-level synthesis for the top-level module `vsdbabysoc`, converting Verilog code into a technology-independent gate-level representation.
   ```
   synth -top vsdbabysoc
   ```
   <div align="center">
     <img src="Images/4.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/5.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/6.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/7.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/8.png" alt="Alt Text" width="1000"/>
   </div>
5. **Step 5: Map Flip-Flops to Standard Cells**<br>
   Map all the D flip-flops in the design to the corresponding flip-flop cells from the provided standard cell library (`sky130_fd_sc_hd__tt_025C_1v80.lib`).
   ```
   dfflibmap -liberty [path to your VSDBabySoC directory]/VSDBabySoC/src/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
   ```
   <div align="center">
     <img src="Images/9.png" alt="Alt Text" width="1000"/>
   </div>
6. **Step 6: Optimize the Design**<br>
   Perform general logic optimizations to simplify the circuit and reduce area, delay, and redundant logic.
   ```
   opt
   ```
   <div align="center">
     <img src="Images/10.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/11.png" alt="Alt Text" width="1000"/>
   </div>
7. **Step 7: Technology Mapping with ABC**<br>
   Run the ABC tool to map the synthesized design to the target standard-cell library, applying logic optimization, retiming, and decomposition steps to generate an efficient gate-level netlist.
   ```
   abc -liberty [path to your VSDBabySoC directory]/VSDBabySoC/src/lib/sky130_fd_sc_hd__tt_025C_1v80.lib -script +strash;scorr;ifraig;retime;{D};strash;dch,-f;map,-M,1,{D}
   ```
   <div align="center">
     <img src="Images/12.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/13.png" alt="Alt Text" width="1000"/>
   </div>
8. **Step 8: Flatten the Design and Clean Up**<br>
   * `flatten`: Collapse all module hierarchies into a single top-level design.
   * `setundef -zero`: Set all undefined signals to logic 0.
   * `clean -purge`: Remove unused cells and nets.
   * `rename -enumerate`: Rename all remaining signals and cells systematically for clarity.
   ```
   flatten
   setundef -zero
   clean -purge
   rename -enumerate
   ```
   <div align="center">
     <img src="Images/14.png" alt="Alt Text" width="1000"/>
   </div>
9. **Step 9: Design Statistics**<br>
   Run the `stat` command to display a summary of the current design, including the number of cells, wires, and hierarchical modules, helping you assess the complexity and size of the synthesized netlist.
   ```
   stat
   ```
   <div align="center">
     <img src="Images/15.png" alt="Alt Text" width="1000"/>
   </div>
   <div align="center">
     <img src="Images/16.png" alt="Alt Text" width="1000"/>
   </div>
10. **Step 10: Write Synthesized Netlist**<br>
   Use the `write_verilog` command to export the optimized gate-level netlist to a Verilog file, which can be used for post-synthesis simulations or further design analysis.
   ```
   write_verilog -noattr [path to your VSDBabySoC directory]/VSDBabySoC//output/post_synth_sim/vsdbabysoc.synth.v
   ```
   <div align="center">
     <img src="Images/17.png" alt="Alt Text" width="1000"/>
   </div>
   
11. **Step 11: Exit Yosys**<br>
   Terminate the Yosys synthesis session and return to the regular terminal shell.
   ```
   exit
   ``` 

### <ins>2. Gate-Level Simulation.</ins>
1. **Step 1: Compile Gate-Level Simulation**<br>
   Compile the gate-level netlist along with the testbench using Icarus Verilog, defining macros for post-synthesis simulation and functional behavior, and including necessary directories for source and GLS model files.
   ```
   iverilog -o [path to your VSDBabySoC directory]/VSDBabySoC/output/post_synth_sim/post_synth_sim.out -DPOST_SYNTH_SIM -DFUNCTIONAL -DUNIT_DELAY=#1 -I [path to your VSDBabySoC directory]/VSDBabySoC/src/include -I [path to your VSDBabySoC directory]/VSDBabySoC/src/module -I [path to your VSDBabySoC directory]/VSDBabySoC/src/gls_model -I [path to your VSDBabySoC directory]/VSDBabySoC/output/post_synth_sim [path to your VSDBabySoC directory]/VSDBabySoC/src/module/testbench.v
   ```
2. **Step 2: Navigate to Output Directory**<br>
   Change the current directory to the post-synthesis simulation output folder to access the compiled simulation files and results.
   ```
   cd [path to your VSDBabySoC directory]/VSDBabySoC/output/post_synth_sim/
   ```
3. **Step 3: Run Post-Synthesis Simulation**<br>
   Execute the compiled simulation binary to verify that the gate-level netlist produces the expected functional outputs.
   ```
   ./post_synth_sim.out
   ```
4. **Step 4: View Simulation Waveforms in GTKWave**<br>
   Open the generated VCD (Value Change Dump) file in GTKWave to visually inspect the signal transitions and verify the correctness of the post-synthesis simulation.
   ```
   gtkwave post_synth_sim.vcd
   ```
   <div align="center">
     <img src="Images/18.png" alt="Alt Text" width="1000"/>
   </div>

### <ins>3. Output in GTKWave.</ins>
<div align="center">
  <img src="Images/VSDBabySoC_GLS_GTKWave.png" alt="Alt Text" width="1000"/>
</div>

### <ins>4. The Synthesis Logs.</ins>
The screenshots of the synthesis logs, captured from the terminal, are provided under each corresponding command. These screenshots display the username and timestamps for reference. Note that timestamps could not be captured while running Yosys, as it does not natively support this feature; however, timestamps are visible outside the Yosys environment.<br>
For certain commands, the logs could not be displayed in full within the screenshots due to their extensive length. In these cases, only the beginning and end portions of the command outputs are shown. For those interested in reviewing the complete synthesis logs, the entire terminal output has been exported as a log file, which can be accessed [here.](VSDBabySoC_GLS_Bitopan.log)

### <ins>5. Analysis after GLS.</ins>
After completing both the RTL simulations and gate-level simulations (GLS) of the VSDBabySoC design, a comparison of the outputs was performed using GTKWave. The key observations are as follows:
1. **Functional Equivalence:**
   The outputs of the gate-level simulation exactly match the outputs from the RTL simulation, confirming that the synthesis and subsequent technology mapping have preserved the intended functionality of the design.
2. **Timing and Signal Integrity:**
   No unexpected glitches or incorrect transitions were observed in the GLS outputs. All signals behaved as expected under the defined testbench stimuli, indicating that the design is stable and timing-correct at the synthesized level.
3. **Conclusion:**
   The successful verification of GLS against RTL simulations validates that the synthesized netlist is functionally equivalent to the RTL design. This confirms the correctness of the synthesis flow, cell mapping, and the overall implementation of the VSDBabySoC.

---

## 2. Fundamentals of Static Timing Analysis (STA).
### <ins>1. What is Static Timing Analysis?</ins>
Static Timing Analysis (STA) is a method used in digital design to verify that a circuit meets its timing requirements without simulating actual waveforms. It calculates the expected signal arrival and checks if it meets setup, hold, and other timing constraints.<br>
*Think of STA as “predictive timing verification”—you aren’t simulating waveforms but calculating if the timing rules are satisfied.*

### <ins>2. Core Components of STA</ins>
STA broadly comprises three main components:
- **Timing Checks**:<br>
  These are the first level of diagnosis for a chip, ensuring signals meet timing rules. Examples include:
  * **Setup checks**: Verify signals arrive before the clock edge.
  * **Hold checks**: Ensure signals are stable after the clock edge.
  * **Recovery/Removal checks**: For asynchronous signals like resets.

- **Constraints**:<br>
  Constraints are specifications provided to the STA tool, defining timing requirements for clocks, inputs, outputs, and internal paths.

- **Libraries**:<br>
  Libraries provide the models used in STA. These models define the behavior of standard cells (gates, flip-flops, etc.) under different conditions. Models can be Non-Linear Delay Models (NLDM) or constant current source models
  
### <ins>3. Timing Path</ins>
A timing path is the route that a signal takes from its starting point to its endpoint in a digital circuit.
- **Start point:** Clock pin of a flip-flop or an input port
- **End point:** D pin of a flip-flop or an output port

It is crucial to identify valid timing paths so that STA checks are meaningful.

### <ins>4. Key Timing Parameters</ins>
- **Arrival Time**:<br>
  * The time taken for a signal to travel from the start point to the endpoint.
  * Calculated only at the endpoints of the timing path.
- **Launch Flop and Capture Flop**:<br>
  * **Launch flop**: The flip-flop from which a signal is launched.
  * **Capture flop**: The flip-flop that captures the signal.
- **Required Time**:<br>
  * Defines when a signal is expected to arrive at the endpoint.
  * Example: A signal should arrive after 0.5 ns but before 3 ns.
    * 0.5 ns → minimum expected time
    * 3 ns → maximum expected time
- **Slack**:<br>
Slack is the difference between the arrival time and the required time. It indicates timing margin.
  * Minimum Slack: `arrival time – min required time` → Hold Slack
  * Maximum Slack: `max required time – arrival time` → Setup Slack

### <ins>5. Types of Timing Analysis</ins>
- **Setup/Hold Analysis**
  * **Reg2Reg**: From a register to another register
  * **In2Reg**: From an input port to a flop’s D pin
  * **Reg2Out**: From a flop’s Q pin to an output port
  * **In2Out**: From an input port to an output port

    The last three categories are collectively called I/O timing.
- **Other Timing Checks**
  * **Clock-Gating Analysis**: From clock to gate output
  * **Recovery/Removal Analysis**: From clock to reset of another flip-flop
  * **Data-to-Data Check**: Ensures two signals remain in synchronism
  * **Latch Analysis**: Time borrowing between latches and flops

- **Slew / Transition Analysis**
  * Ensures the rise/fall times of signals are within minimum and maximum limits.
  * Subdivisions:
    * Data slew analysis
    * Clock slew analysis
  * Important for power and signal integrity considerations.

- **Load Analysis**
  * **Fanout analysis**: Ensures maximum/minimum fanout limits are not violated.
  * **Capacitance analysis**: Checks that node capacitances are within acceptable limits.
 
- **Clock Analysis**
  * Skew Analysis:
    * Skew = difference in latency from the clock input to each flip-flop clock port
    * Skew must be managed as it affects setup and hold margins.
  * Pulse Width Analysis: Checks the degradation of pulse width through the circuit.

### <ins>6. Setup Analysis with a Single Clock</ins>
- **Delays in the Circuit**:<br>
  In STA, all components and wires have delays, measured in nanoseconds (ns) or picoseconds (ps), depending on the technology:
  * **Cell delays**:<br>
    Denoted like `a(2)`, meaning element `a` has 2 units of delay.
  * **Wire delays**:<br>
    Example: `0.1`, `0.2`, `0.15` units, depending on the wire length and resistance.
  * **Signal transition delays**:<br>
    When a signal arrives at an input pin, its rise/fall transition times also contribute to the total delay.

  All these delays add up along the timing path and affect the final arrival time of signals.
- **Timing Graph / DAG**:<br>
  To analyze timing efficiently, we represent the circuit as a Directed Acyclic Graph (DAG), also called a timing graph:
  * **Nodes:** represent points in the circuit (pins or cells, depending on convention)
  * **Edges:** represent signal propagation delays

  This graph allows the STA tool to systematically calculate timing parameters across the entire design.
- **Actual Arrival Time (AAT)**:<br>
  * **Definition**: Time at any node when the latest transition occurs after the first clock edge.
  * **Calculation:**
    * Sum of all previous delays from the source to that particular node.
    * For multi-input nodes:
      * Setup analysis: take the largest AAT (worst-case delay)
      * Hold analysis: take the smallest AAT (earliest arrival)

  Intuition: For setup checks, we care about signals that arrive late, while for hold checks, we care about signals that arrive too early.
- **Required Arrival Time (RAT)**:<br>
  * **Definition**: Time at any node when a signal is expected to arrive to meet timing requirements.
  * **Calculation:**
    1. Start at the output pin where the required timing is defined.
    2. Work backwards, subtracting delays along each edge to calculate RAT for each upstream node.
    3. For multi-output nodes: take the smallest RAT, as it represents the most restrictive timing requirement.

   *Think of AAT as “what actually happens” and RAT as “what should happen”.*

- **Slack Computation**:<br>
  Slack indicates whether a design meets timing requirements:
  * **Calculation**: `Slack=RAT−AAT`
  * **Positive slack**: timing requirement satisfied
  * **Negative slack**: timing violation
    * When slack is negative at outputs, we can trace back through the graph to identify the nodes causing the largest negative slack.
    * Tuning the delays of these nodes improves overall timing.

  *Slack is your signal health indicator—negative slack highlights trouble spots.*

- **Graph-Based vs Path-Based Analysis**:<br>
  STA can be performed in two approaches:
  1. Graph-Based Analysis (Node-based):
     * DAG is represented using pin-node convention: each pin of a cell is a node, and the cell itself disappears.
     * AAT, RAT, and slack are computed at every node, giving a detailed view of timing across the circuit.
  2. Path-Based Analysis:
     * Focuses only on specific timing paths, from launch to capture points.
     * Easier for high-level timing checks but less detailed than node-based graph analysis.

     Graph-based analysis is considered more accurate and detailed, especially for complex designs.

### <ins>7. Flip-Flop Timing, Clock Skew, and Jitter</ins>

































