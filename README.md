# Week 3: Post Synthesis GLS and STA Fundamentals
 
The focus of this week is 

---

## 📜 Table of Contents
[📋 Prerequisites](#-prerequisites) <br>

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

