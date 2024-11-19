# otf_general

Implementation of On-The-Fly (OTF) Optimization for alchemical binding free energy simulations using thermodynamic integration in AMBER20. See 10.26434/chemrxiv-2023-rtpsz for details.

## ***Setup***
***

1. Create a directory, clone otf_general.
2. Install [Anaconda](https://docs.anaconda.com/anaconda/install/).
3. Install dependencies: pymbar==4.0.3, alchemlyb==2.3.1, scipy==1.8.1, AMBER20, GAUSSIAN 09 or GAUSSIAN 16 (for ligand parameterization).


## ***Algorith***
***

Algorithm: On-the-Fly Resource Optimization for Binding Free Energy Simulations

1. Perform an initial run of the simulation.

2. Apply Automatic Equilibration Detection (AED) and decorrelation:
    - Split gradient data in half and bin it into histograms.
    - Calculate the Jensen-Shannon (JS) distance between the histograms.

3. Evaluate the JS distance:
    if JS distance < 0.1:
        - Terminate simulation (converged).
    else:
        - Check if simulation time is less than 6.5 nanoseconds (ns):
            if yes:
                - Proceed to Step 4 (short additional simulation).
            else:
                - Check if there are more than 50 decorrelated samples:
                    if yes:
                        - Terminate simulation (sufficient decorrelated samples).
                    else:
                        - Proceed to Step 4 (short additional simulation).

4. Run a short additional simulation and increment the simulation time.

5. Evaluate total computed simulation time:
    if total simulation time < 10.5 ns:
        - Repeat from Step 2.
    else:
        - Terminate simulation (time limit reached).
