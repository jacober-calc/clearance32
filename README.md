![Social Media Preview](assets/clearance32_social_preview.png)

# clearance Statefile

## CONTENTS

1. [Introduction](#1-introduction)
2. [Disclaimer](#2-disclaimer)
3. [Theory of Operations](#3-theory-of-operations)
4. [Variable Definitions](#4-variable-definitions)
5. [Program Descriptions](#5-program-descriptions)
6. [Operating Instructions](#6-operating-instructions)
7. [Example Calculations](#7-example-calculations)
8. [Quick Reference](#8-quick-reference)
9. [Program Listing](#9-program-listing)

---

## 1. INTRODUCTION

This program suite provides comprehensive mine clearance operations planning for Mine Countermeasures (MCM) assets. The calculator determines the number of passes required to achieve a specified confidence level that mine density has been reduced to an acceptable threshold.

### 1.1 Purpose

The program enables operational planners to:

- Calculate required MCM passes for desired confidence levels
- Estimate expected mine encounters during operations
- Determine operational timeline including disposal operations
- Assess residual risk after clearance operations

### 1.2 System Requirements

SwissMicros DM32 calculator with RPN operating system. Program requires approximately 185 program steps.

---

## 2. DISCLAIMER

### IMPORTANT NOTICE

This calculator program and associated documentation contain only non-classified information based on publicly available theoretical concepts and mathematical calculations. All methodologies, equations, and operational parameters described herein are derived from unclassified academic and technical sources.

**Intended Use:** This program is provided for instructional and educational purposes only. It is designed to demonstrate mathematical modeling techniques applicable to mine clearance operations planning. Users are responsible for validating all calculations and applying appropriate operational security measures when using this tool in any professional capacity.

The developer (jacober-calc) makes no warranties, express or implied, regarding the accuracy, completeness, or suitability of this program for any particular operational purpose. Actual mine clearance operations involve complex tactical, environmental, and technical factors beyond the scope of this theoretical model.

**Users must:**

- Consult appropriate operational authorities before applying these calculations to real-world scenarios
- Verify all results independently using approved operational planning tools
- Maintain operational security when discussing or applying these techniques
- Recognize that this is a simplified model and actual operations require comprehensive risk assessment

---

## 3. THEORY OF OPERATIONS

### 3.1 Probability Model

The program uses a Poisson distribution model to calculate the probability of mines remaining after clearance operations. The model assumes:

- Mines are distributed randomly throughout the area
- Each pass is an independent detection event
- Detection probability P remains constant across passes

### 3.2 Key Equations

#### Lambda (Expected Mines Remaining)

```
λ = D × (1 - P)^N × A
```

Where D is density, P is detection probability, N is number of passes, and A is area. Lambda represents the expected number of mines remaining in the entire area of operations after N passes.

#### Expected Mine Encounters

```
E = D × A × (1 - (1 - P)^N)
```

This calculates the total number of mines expected to be detected during N passes.

Every mine in the area is either found or still remaining, so E + λ always equals D × A. Each pass leaves a fraction (1 − P) of the remaining mines, which makes λ fall by the same factor every pass: a straight line on a log scale.

![Found and remaining mines by pass](assets/found_vs_remaining.svg)

#### Confidence Calculation

The confidence C that actual mines remaining ≤ M is calculated using the cumulative Poisson distribution:

```
C = Σ(k=0 to M) [λ^k × e^(-λ) / k!]
```

The chart shows the Poisson distribution of mines remaining after 5, 6, and 7 passes in Example 7.1. Confidence is the green area, k ≤ M. At N = 6 it reaches 0.9361, short of the 0.95 target; the seventh pass lifts it to 0.9844.

![Poisson confidence](assets/poisson_confidence.svg)

#### Time Calculation

```
T = [(A × N) / (V × S) + E × H] / O × 24
```

Where V is velocity, S is swath width, H is handling time per mine, and O is operational tempo.

Search time grows in equal steps with each pass, while disposal time levels off as fewer mines remain to be found. The program rounds E to the nearest whole mine before multiplying by H. Dividing operating hours by O gives operating days, and multiplying by 24 converts them to elapsed hours.

![Mission time](assets/time_breakdown.svg)

### 3.3 Area of Operations

Mine clearance operations involve systematic coverage of the designated area using an MCM asset that follows a search pattern (typically lawn-mower pattern) with defined swath width.

### 3.4 Program Logic Flow

The master program (LBL M) executes an iterative algorithm to determine the minimum number of passes required to achieve the commander's intended confidence level.

```mermaid
flowchart TD
    nM["XEQ M: prompt I, M, D, A, P, S, V, O, H"] --> nZ["N = 0"]
    nZ --> nInc["N = N + 1"]
    nInc --> nW["XEQ W: lambda"]
    nW --> nY["XEQ Y: confidence C"]
    nY --> nQ{"Is I greater than C?"}
    nQ -- "Yes" --> nInc
    nQ -- "No" --> nU["XEQ U: encounters E"]
    nU --> nV["XEQ V: time T"]
    nV --> nOut["T: time, Z: encounters, Y: passes, X: confidence"]
```

**Program Flow:**
1. Initialize N = 0
2. Increment N
3. Calculate Lambda (λ) using XEQ W
4. Calculate Confidence (C) using XEQ Y
5. Check if C ≥ I (intended confidence)
   - If NO: return to step 2
   - If YES: continue to step 6
6. Calculate E (encounters) using XEQ U
7. Calculate T (time) using XEQ V
8. Display results

The chart shows the stopping rule for M = 0, 1, and 2 using the inputs of Example 7.1. A larger M allows more mines to remain, so the required confidence is reached in fewer passes.

![Stopping rule](assets/confidence_by_pass.svg)

---

## 4. VARIABLE DEFINITIONS

| Variable | Description |
|----------|-------------|
| **A** | Area of operations (square nautical miles or km²) |
| **C** | Calculated confidence (probability) |
| **D** | Mine density (mines per unit area) |
| **E** | Expected number of mine encounters (total for AOR) |
| **H** | Handling time per mine (hours) |
| **I** | Commander's intended confidence (target probability) |
| **L** | Lambda - expected mines remaining (Poisson parameter) |
| **M** | Maximum acceptable mines remaining (upper threshold) |
| **N** | Number of passes required |
| **O** | Operational tempo (hours per day) |
| **P** | Probability of detection (MCM asset capability) |
| **S** | Swath width (MCM asset search width) |
| **T** | Time to complete operations (hours) |
| **V** | Velocity (MCM asset search speed) |
| **X, Z** | Subroutine working registers (internal use) |

---

## 5. PROGRAM DESCRIPTIONS

### 5.1 LBL M - Master Operations Planner

The master program integrates all calculations to provide complete operational planning. It iteratively calculates the number of passes required to meet or exceed the commander's intended confidence level.

**Inputs:** I (Commander's intended confidence), M (Maximum acceptable mines), D (Density), A (Area), P (Probability of detection), S (Swath width), V (Velocity), O (Operational tempo), H (Handling time per mine)

**Outputs (Stack display from top to bottom):**
- T: Total operational time
- Z: Expected encounters
- Y: Number of passes
- X: Confidence achieved

### 5.2 LBL L - Lambda Calculator

Calculates the expected number of mines remaining (lambda) for a given density, detection probability, area, and number of passes.

**Inputs:** D (Density), P (Probability of detection), A (Area), N (Number of passes)

**Output:** Lambda (stored in L register)

### 5.3 LBL C - Confidence Calculator

Calculates the confidence level using Poisson distribution that actual mines remaining will not exceed the specified maximum.

**Inputs:** L (Lambda), M (Maximum acceptable mines)

**Output:** Confidence (stored in C register)

### 5.4 LBL N - Required Passes Calculator

Determines the number of passes required to achieve a specified lambda value.

**Inputs:** L (Lambda), D (Density), A (Area), P (Probability of detection)

**Output:** Number of passes (stored in N register)

### 5.5 LBL E - Expected Encounters Calculator

Calculates the expected number of mines that will be encountered during clearance operations.

**Inputs:** D (Density), A (Area), P (Probability of detection), N (Number of passes)

**Output:** Expected encounters (stored in E register)

### 5.6 LBL T - Time Calculator

Calculates total operational time including search passes and mine disposal operations.

**Inputs:** A (Area), N (Number of passes), V (Velocity), S (Swath width), O (Operational tempo), E (Expected encounters), H (Handling time per mine)

**Output:** Total time (stored in T register)

---

## 6. OPERATING INSTRUCTIONS

### 6.1 Running the Master Program (LBL M)

The master program is the primary tool for operational planning. It prompts for all required inputs and calculates the complete mission profile.

**Procedure:**

1. Press `XEQ M`
2. Enter commander's intended confidence when prompted (I?)
3. Enter maximum acceptable mines when prompted (M?)
4. Enter mine density when prompted (D?)
5. Enter area of operations when prompted (A?)
6. Enter detection probability when prompted (P?)
7. Enter swath width when prompted (S?)
8. Enter search velocity when prompted (V?)
9. Enter operational tempo when prompted (O?)
10. Enter handling time per mine when prompted (H?)

**The program will display (from top to bottom on screen):**
- T-register: Total operational time
- Z-register: Expected mine encounters
- Y-register: Number of passes required
- X-register: Confidence achieved

**Note:** To view expected mines remaining (lambda), press `RCL L` after program completion.

### 6.2 Individual Calculators

Individual calculation programs can be run independently for specific analyses:

**LBL L (Lambda):**
`XEQ L`, then enter D (Density), P (Probability of detection), A (Area), N (Number of passes) when prompted

**LBL C (Confidence):**
`XEQ C`, then enter L (Lambda), M (Maximum acceptable mines) when prompted

**LBL N (Required Passes):**
`XEQ N`, then enter L (Lambda), D (Density), A (Area), P (Probability of detection) when prompted

**LBL E (Encounters):**
`XEQ E`, then enter D (Density), A (Area), P (Probability of detection), N (Number of passes) when prompted

**LBL T (Time):**
`XEQ T`, then enter A (Area), N (Number of passes), V (Velocity), S (Swath width), O (Operational tempo), E (Expected encounters), H (Handling time per mine) when prompted

---

## 7. EXAMPLE CALCULATIONS

### 7.1 Complete Mission Planning

**Scenario:**

A mine clearance operation requires 95% confidence that no more than 1 mine remains in a 12.5 nm² area with estimated density of 3.45 mines/nm². The MCM asset has 54% detection probability, 0.1 nm swath, operates at 10 knots, with 20 hours/day operational tempo and 2.5 hours handling time per mine.

**Solution:**

Press: `XEQ M`

| Prompt | Enter | Description |
|--------|-------|-------------|
| I? | 0.95 | Intended confidence |
| M? | 1 | Max acceptable mines |
| D? | 3.45 | Mine density |
| A? | 12.5 | Area |
| P? | 0.54 | Detection probability |
| S? | 0.100 | Swath width |
| V? | 10 | Velocity |
| O? | 20 | Operational tempo |
| H? | 2.5 | Handling time per mine |

**Results (displayed on screen from top to bottom):**

| Register | Value | Meaning |
|----------|-------|---------|
| T | 234.00000 | 234 total hours |
| Z | 42.93705 | 43 mine encounters |
| Y | 7.00000 | 7 passes required |
| X | 0.98440 | 98.44% confidence |

**Interpretation:**

The operation requires 7 passes to achieve 98.44% confidence (exceeding the 95% requirement) that no more than 1 mine remains. Approximately 43 mines will be encountered requiring disposal. Total mission time is 234 hours, equivalent to 11.7 operational days at 20 hours/day tempo.

**Additional Information:** To view expected mines remaining (lambda value), press `RCL L`. Result: 0.18795 mines expected remaining in the entire AOR.

**Planning Sensitivity:**

The chart repeats the master program's calculation across a range of detection probabilities, holding density, area, and M at the Example 7.1 values. Each step marks the point where one fewer pass is needed. Raising the intended confidence from 0.95 to 0.99 usually costs one extra pass, occasionally none or two.

![Passes required by detection probability](assets/passes_vs_detection.svg)

---

## 8. QUICK REFERENCE

### 8.1 Program Labels

| Label | Function |
|-------|----------|
| **M** | Master operations planner |
| **L** | Lambda (expected mines remaining) calculator |
| **C** | Confidence calculator (Poisson distribution) |
| **N** | Number of passes required calculator |
| **E** | Expected mine encounters calculator |
| **T** | Time calculator |
| **A** | Display subroutine (final screen) |
| **W,Y,U,V** | Calculation subroutines (internal) |
| **Z,X** | Loop subroutines (internal) |

### 8.2 Typical Input Ranges

| Variable | Typical Range |
|----------|---------------|
| **I** | 0.90 to 0.99 (90% to 99% confidence) |
| **M** | 0 to 5 mines (acceptable residual) |
| **D** | 0.5 to 10 mines per nm² (varies by threat assessment) |
| **P** | 0.40 to 0.90 (40% to 90% detection per pass) |
| **O** | 12 to 24 hours per day (operational tempo) |
| **H** | 1 to 5 hours per mine (handling/disposal time) |

### 8.3 Important Notes

- All area calculations apply to the TOTAL area of operations, not per unit area
- Expected values (E, L) represent statistical means; actual results will vary
- The master program (LBL M) pre-loads reference confidence values (0.90, 0.95, 0.99) on the stack for convenience
- Confidence C represents the probability that actual mines remaining ≤ M
- Lambda (L) represents expected mines remaining for the entire AOR - press `RCL L` to view after running LBL M

---

## 9. PROGRAM LISTING

The complete program listing is provided below. Program steps are shown in standard DM32 RPN format.

### LBL M - Master Program

```
LBL M
0.90
0.95
0.99
INPUT I
INPUT M
INPUT D
INPUT A
INPUT P
INPUT S
INPUT V
INPUT O
INPUT H
0
STO N
LBL Z
1
STO+ N
XEQ W
XEQ Y
RCL I
x>y?
GTO Z
XEQ U
XEQ V
LBL A
RCL T
RCL E
RCL N
RCL C
RTN
```

### LBL L - Lambda Calculator

```
LBL L
INPUT D
INPUT P
INPUT A
INPUT N
LBL W
RCL D
1
RCL P
-
RCL N
y^x
×
RCL A
×
STO L
CLx
ENTER
ENTER
ENTER
RCL L
RTN
```

### LBL C - Confidence Calculator

```
LBL C
INPUT L
INPUT M
LBL Y
0
STO Z
STO C
RCL M
1000
÷
STO+ Z
LBL X
RCL L
RCL Z
IP
y^x
LASTx
x!
÷
RCL L
+/-
e^x
×
FS? 0
STOP
STO+ C
ISG Z
GTO X
RCL L
SQRT
STO X
CLx
ENTER
ENTER
RCL X
RCL C
RTN
```

### LBL N - Required Passes Calculator

```
LBL N
INPUT L
INPUT D
INPUT A
INPUT P
RCL L
RCL D
RCL A
×
÷
LN
1
RCL P
-
LN
÷
STO N
CLx
ENTER
ENTER
ENTER
RCL N
RTN
```

### LBL E - Expected Encounters Calculator

```
LBL E
INPUT D
INPUT A
INPUT P
INPUT N
LBL U
1
1
RCL P
-
RCL N
y^x
-
RCL A
RCL D
×
×
STO E
CLx
ENTER
ENTER
ENTER
RCL E
RTN
```

### LBL T - Time Calculator

```
LBL T
INPUT A
INPUT N
INPUT V
INPUT S
INPUT O
INPUT E
INPUT H
LBL V
RCL A
RCL N
×
RCL V
RCL S
×
÷
RCL E
0.5
+
IP
RCL H
×
+
RCL O
÷
24
×
STO T
CLx
ENTER
ENTER
ENTER
RCL T
RTN
```

---

## Disclaimer

This program and documentation are provided for educational and instructional purposes only. Users are responsible for validating all calculations and applying appropriate operational security measures.

### By jacober-calc for SwissMicros DM32

> - [SwissMicros Website](https://www.swissmicros.com)
> - [DM32 product page](https://www.swissmicros.com/product/model-dm32)
> - [SwissMicros full products page](https://www.swissmicros.com/products)
> - [DM32 Online User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html)
> - [SwissMicros Calculator Forum](https://forum.swissmicros.com/index.php)
