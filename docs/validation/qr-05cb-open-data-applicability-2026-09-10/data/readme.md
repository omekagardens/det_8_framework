This dataset was collected as part of an experimental investigation into nonlinear quantum interference phenomena. 
The study aimed to demonstrate violations of the CHSH inequality using unentangled photons in the frustrated interference. 
By controlling the interferometer’s internal phases, the experiment explored the relationship between multi-photon interference and quantum correlations.

File: VBI_Coincidence_20230707.dat\
Description: This file record all the single and coincidence counts in the Bell test of the four-photon frustrated interference. We use the counts to estimate 
the violation of CHSH inequality. This file is a two-dimensional table:

Columns 1-2: Motorized stage positions (Alice, Bob);\
Columns 3-4: Piezoelectric translation stage positions (Alice, Bob);\
Remaining columns: Single counts and coincidence counts\
Columns 5-8: Single counts on channel 1, 2, 3, 4;\
Column 9: Coincidence of channel 1, 2, 3 and 4;\
Column 10: Coincidence of channel 1 and 2;\
Column 11: Coincidence of channel 3 and 4;

File: main.m\
Description: The code is a MATLAB script that processes the data file "VBI_Coincidence_20230707.dat". The code contains detailed comments for clarification.
It plots Fig. 1-4.\
Fig. 1 shows the raw data of four-photon-coincidence count in different phase settings α and β. \
Fig. 2 shows the correlation results of four-photon-coincidence counts (C. C.) N(α, β) with α being 0, pi, pi/2 and 3pi/2. β varies from 0 to 4pi.\
Fig. 3 is the verification of quantum correlation.\
Fig. 4 shows the visibility of the four-photon interference using quantum indistinguishability by path identity.
