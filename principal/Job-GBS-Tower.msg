1

   Abaqus Learning Edition 2025                                  Date 14-janv.-2026   Time 11:28:12
   

 Calcul GBS et Tour                                                              
                                                                                 
 STEP    1     INCREMENT     1     STEP TIME    0.00    


                        S T E P       1     S T A T I C   A N A L Y S I S


                                                                                          

     AUTOMATIC TIME CONTROL WITH -
          A SUGGESTED INITIAL TIME INCREMENT OF                8.000E-02
          AND A TOTAL TIME PERIOD OF                            4.00    
          THE MINIMUM TIME INCREMENT ALLOWED IS                4.000E-05
          THE MAXIMUM TIME INCREMENT ALLOWED IS                8.000E-02

     LINEAR EQUATION SOLVER TYPE         DIRECT SPARSE

 CONVERGENCE TOLERANCE PARAMETERS FOR FORCE    
     CRITERION FOR RESIDUAL FORCE     FOR A NONLINEAR PROBLEM          5.000E-03
     CRITERION FOR DISP.    CORRECTION IN A NONLINEAR PROBLEM          1.000E-02
     INITIAL VALUE OF TIME AVERAGE FORCE                               1.000E-02
     AVERAGE FORCE     IS TIME AVERAGE FORCE    
     ALTERNATE CRIT. FOR RESIDUAL FORCE     FOR A NONLINEAR PROBLEM    2.000E-02
     CRITERION FOR ZERO FORCE     RELATIVE TO TIME AVRG. FORCE         1.000E-05
     CRITERION FOR RESIDUAL FORCE     WHEN THERE IS ZERO FLUX          1.000E-05
     CRITERION FOR DISP.    CORRECTION WHEN THERE IS ZERO FLUX         1.000E-03
     CRITERION FOR RESIDUAL FORCE     FOR A LINEAR INCREMENT           1.000E-08
     FIELD CONVERSION RATIO                                             1.00    
     CRITERION FOR ZERO FORCE     REL. TO TIME AVRG. MAX. FORCE        1.000E-05
     CRITERION FOR ZERO DISP.    RELATIVE TO CHARACTERISTIC LENGTH     1.000E-08

 CONVERGENCE TOLERANCE PARAMETERS FOR MOMENT   
     CRITERION FOR RESIDUAL MOMENT    FOR A NONLINEAR PROBLEM          5.000E-03
     CRITERION FOR ROTATION CORRECTION IN A NONLINEAR PROBLEM          1.000E-02
     INITIAL VALUE OF TIME AVERAGE MOMENT                              1.000E-02
     AVERAGE MOMENT    IS TIME AVERAGE MOMENT   
     ALTERNATE CRIT. FOR RESIDUAL MOMENT    FOR A NONLINEAR PROBLEM    2.000E-02
     CRITERION FOR ZERO MOMENT    RELATIVE TO TIME AVRG. MOMENT        1.000E-05
     CRITERION FOR RESIDUAL MOMENT    WHEN THERE IS ZERO FLUX          1.000E-05
     CRITERION FOR ROTATION CORRECTION WHEN THERE IS ZERO FLUX         1.000E-03
     CRITERION FOR RESIDUAL MOMENT    FOR A LINEAR INCREMENT           1.000E-08
     FIELD CONVERSION RATIO                                             1.00    
     CRITERION FOR ZERO MOMENT    REL. TO TIME AVRG. MAX. MOMENT       1.000E-05

     VOLUMETRIC STRAIN COMPATIBILITY TOLERANCE FOR HYBRID SOLIDS       1.000E-05
     AXIAL STRAIN COMPATIBILITY TOLERANCE FOR HYBRID BEAMS             1.000E-05
     TRANS. SHEAR STRAIN COMPATIBILITY TOLERANCE FOR HYBRID BEAMS      1.000E-05
     SOFT CONTACT CONSTRAINT COMPATIBILITY TOLERANCE FOR P>P0          5.000E-03
     SOFT CONTACT CONSTRAINT COMPATIBILITY TOLERANCE FOR P=0.0         0.100    
     CONTACT FORCE ERROR TOLERANCE FOR CONVERT SDI=YES                 1.00    
     DISPLACEMENT COMPATIBILITY TOLERANCE FOR DCOUP ELEMENTS           1.000E-05
     ROTATION COMPATIBILITY TOLERANCE FOR DCOUP ELEMENTS               1.000E-05

 EQUILIBRIUM WILL BE CHECKED FOR SEVERE DISCONTINUITY ITERATIONS

 TIME INCREMENTATION CONTROL PARAMETERS:
     FIRST EQUILIBRIUM ITERATION FOR CONSECUTIVE DIVERGENCE CHECK              4
     EQUILIBRIUM ITERATION AT WHICH LOG. CONVERGENCE RATE CHECK BEGINS         8
     EQUILIBRIUM ITERATION AFTER WHICH ALTERNATE RESIDUAL IS USED              9
     MAXIMUM EQUILIBRIUM ITERATIONS ALLOWED                                   16
     EQUILIBRIUM ITERATION COUNT FOR CUT-BACK IN NEXT INCREMENT               10
     MAXIMUM EQUILIB. ITERS IN TWO INCREMENTS FOR TIME INCREMENT INCREASE      4
     MAXIMUM ITERATIONS FOR SEVERE DISCONTINUITIES                            50
     MAXIMUM ATTEMPTS ALLOWED IN AN INCREMENT                                  5
     MAXIMUM DISCON. ITERS IN TWO INCREMENTS FOR TIME INCREMENT INCREASE      50
     MAXIMUM CONTACT AUGMENTATIONS FOR *SURFACE BEHAVIOR,AUGMENTED LAGRANGE   50
     CUT-BACK FACTOR AFTER DIVERGENCE                                 0.2500    
     CUT-BACK FACTOR FOR TOO SLOW CONVERGENCE                         0.5000    
     CUT-BACK FACTOR AFTER TOO MANY EQUILIBRIUM ITERATIONS            0.7500    
     CUT-BACK FACTOR AFTER TOO MANY SEVERE DISCONTINUITY ITERATIONS   0.2500    
     CUT-BACK FACTOR AFTER PROBLEMS IN ELEMENT ASSEMBLY               0.2500    
     INCREASE FACTOR AFTER TWO INCREMENTS THAT CONVERGE QUICKLY        1.500    
     MAX. TIME INCREMENT INCREASE FACTOR ALLOWED                       1.500    
     MAX. TIME INCREMENT INCREASE FACTOR ALLOWED (DYNAMICS)            1.250    
     MAX. TIME INCREMENT INCREASE FACTOR ALLOWED (DIFFUSION)           2.000    
     MINIMUM TIME INCREMENT RATIO FOR EXTRAPOLATION TO OCCUR          0.1000    
     MAX. RATIO OF TIME INCREMENT TO STABILITY LIMIT                   1.000    
     FRACTION OF STABILITY LIMIT FOR NEW TIME INCREMENT               0.9500    
     TIME INCREMENT INCREASE FACTOR BEFORE A TIME POINT                1.000    
     GLOBAL STABILIZATION CONTROL IS NOT USED

          PRINT OF INCREMENT NUMBER, TIME, ETC., EVERY    1  INCREMENTS

     THE MAXIMUM NUMBER OF INCREMENTS IN THIS STEP IS                    100

     LINEAR EXTRAPOLATION WILL BE USED

     CHARACTERISTIC ELEMENT LENGTH      4.71    

     DETAILS REGARDING ACTUAL SOLUTION WAVEFRONT REQUESTED

     DETAILED OUTPUT OF DIAGNOSTICS TO DATABASE REQUESTED

     PRINT OF INCREMENT NUMBER, TIME, ETC., TO THE MESSAGE FILE EVERY     1  INCREMENTS

     COLLECTING MODEL CONSTRAINT INFORMATION FOR OVERCONSTRAINT CHECKS

     COLLECTING STEP CONSTRAINT INFORMATION FOR OVERCONSTRAINT CHECKS


  INCREMENT     1 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02

 ***WARNING: THERE ARE 2 UNCONNECTED REGIONS IN THE MODEL.

 ***NOTE: SFM TYPE SURFACE ELEMENTS USED TO DEFINE CONTACT SURFACES NOT PART OF 
          A RIGID BODY MAY INCREASE THE NUMBER OF UNCONNECTED REGIONS REPORTED.
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  18ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       1.04       TIME AVG. FORCE        1.04    
 LARGEST SCALED RESIDUAL FORCE      4.719E-11   AT NODE        205   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      4.719E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       4.92    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  2.000E-02
 STEP TIME COMPLETED       8.000E-02,  TOTAL TIME COMPLETED        8.000E-02


  INCREMENT     2 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  8ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       7.02       TIME AVG. FORCE        4.03    
 LARGEST SCALED RESIDUAL FORCE     -1.860E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.860E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.711E-19   AT NODE         91   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       4.92    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.027E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  4.000E-02
 STEP TIME COMPLETED       0.160    ,  TOTAL TIME COMPLETED        0.160    


  INCREMENT     3 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       10.5       TIME AVG. FORCE        6.19    
 LARGEST SCALED RESIDUAL FORCE     -1.744E-11   AT NODE        256   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.744E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -1.356E-19   AT NODE         91   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       19.0    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.540E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  6.000E-02
 STEP TIME COMPLETED       0.240    ,  TOTAL TIME COMPLETED        0.240    


  INCREMENT     4 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  11ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       14.0       TIME AVG. FORCE        8.15    
 LARGEST SCALED RESIDUAL FORCE      1.640E-11   AT NODE        257   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.640E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        3.292E-22   AT NODE        104   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       29.2    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      2.054E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  8.000E-02
 STEP TIME COMPLETED       0.320    ,  TOTAL TIME COMPLETED        0.320    


  INCREMENT     5 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  21ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       17.5       TIME AVG. FORCE        10.0    
 LARGEST SCALED RESIDUAL FORCE      1.890E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.890E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -3.561E-22   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       38.4    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      2.567E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.100    
 STEP TIME COMPLETED       0.400    ,  TOTAL TIME COMPLETED        0.400    


  INCREMENT     6 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       21.0       TIME AVG. FORCE        11.9    
 LARGEST SCALED RESIDUAL FORCE     -1.682E-11   AT NODE        257   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.682E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        4.127E-22   AT NODE         97   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       47.2    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      3.081E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.120    
 STEP TIME COMPLETED       0.480    ,  TOTAL TIME COMPLETED        0.480    


  INCREMENT     7 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       24.6       TIME AVG. FORCE        13.7    
 LARGEST SCALED RESIDUAL FORCE     -1.946E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.946E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.870E-22   AT NODE        292   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       55.9    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      3.594E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.140    
 STEP TIME COMPLETED       0.560    ,  TOTAL TIME COMPLETED        0.560    


  INCREMENT     8 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  20ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       28.1       TIME AVG. FORCE        15.5    
 LARGEST SCALED RESIDUAL FORCE     -1.231E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.231E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -4.410E-22   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       64.4    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      4.108E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.160    
 STEP TIME COMPLETED       0.640    ,  TOTAL TIME COMPLETED        0.640    


  INCREMENT     9 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       31.6       TIME AVG. FORCE        17.3    
 LARGEST SCALED RESIDUAL FORCE     -1.561E-11   AT NODE         91   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.561E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -3.809E-22   AT NODE        106   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       72.9    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      4.621E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.180    
 STEP TIME COMPLETED       0.720    ,  TOTAL TIME COMPLETED        0.720    


  INCREMENT    10 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       35.1       TIME AVG. FORCE        19.0    
 LARGEST SCALED RESIDUAL FORCE     -2.331E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -2.331E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.565E-22   AT NODE        308   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       81.3    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      5.135E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.200    
 STEP TIME COMPLETED       0.800    ,  TOTAL TIME COMPLETED        0.800    


  INCREMENT    11 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  14ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       38.6       TIME AVG. FORCE        20.8    
 LARGEST SCALED RESIDUAL FORCE      1.286E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.286E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        6.812E-22   AT NODE        106   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       89.7    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      5.648E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.220    
 STEP TIME COMPLETED       0.880    ,  TOTAL TIME COMPLETED        0.880    


  INCREMENT    12 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       42.1       TIME AVG. FORCE        22.6    
 LARGEST SCALED RESIDUAL FORCE      1.344E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.344E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -7.993E-22   AT NODE        106   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       98.0    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      6.162E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.240    
 STEP TIME COMPLETED       0.960    ,  TOTAL TIME COMPLETED        0.960    


  INCREMENT    13 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  6ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       45.6       TIME AVG. FORCE        24.4    
 LARGEST SCALED RESIDUAL FORCE     -1.391E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.391E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        6.938E-22   AT NODE         93   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       106.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      6.675E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.260    
 STEP TIME COMPLETED        1.04    ,  TOTAL TIME COMPLETED         1.04    


  INCREMENT    14 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       49.1       TIME AVG. FORCE        26.1    
 LARGEST SCALED RESIDUAL FORCE     -1.482E-11   AT NODE         94   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.482E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        7.019E-22   AT NODE        103   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       115.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      7.189E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.280    
 STEP TIME COMPLETED        1.12    ,  TOTAL TIME COMPLETED         1.12    


  INCREMENT    15 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  9ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       52.6       TIME AVG. FORCE        27.9    
 LARGEST SCALED RESIDUAL FORCE      1.500E-11   AT NODE        278   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.500E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.052E-21   AT NODE         99   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       123.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      7.702E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.300    
 STEP TIME COMPLETED        1.20    ,  TOTAL TIME COMPLETED         1.20    


  INCREMENT    16 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  10ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       56.1       TIME AVG. FORCE        29.7    
 LARGEST SCALED RESIDUAL FORCE     -1.255E-11   AT NODE        308   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.255E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -4.438E-22   AT NODE         99   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       131.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      8.216E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.320    
 STEP TIME COMPLETED        1.28    ,  TOTAL TIME COMPLETED         1.28    


  INCREMENT    17 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       59.6       TIME AVG. FORCE        31.4    
 LARGEST SCALED RESIDUAL FORCE      1.373E-11   AT NODE        275   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.373E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -6.867E-22   AT NODE        101   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       140.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      8.729E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.340    
 STEP TIME COMPLETED        1.36    ,  TOTAL TIME COMPLETED         1.36    


  INCREMENT    18 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  7ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       63.1       TIME AVG. FORCE        33.2    
 LARGEST SCALED RESIDUAL FORCE      2.076E-11   AT NODE        309   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      2.076E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        6.836E-22   AT NODE        100   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       148.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      9.243E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.360    
 STEP TIME COMPLETED        1.44    ,  TOTAL TIME COMPLETED         1.44    


  INCREMENT    19 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  16ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       66.6       TIME AVG. FORCE        34.9    
 LARGEST SCALED RESIDUAL FORCE      1.511E-11   AT NODE        304   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.511E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.099E-21   AT NODE         97   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       156.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      9.756E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.380    
 STEP TIME COMPLETED        1.52    ,  TOTAL TIME COMPLETED         1.52    


  INCREMENT    20 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  15ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       70.2       TIME AVG. FORCE        36.7    
 LARGEST SCALED RESIDUAL FORCE      1.631E-11   AT NODE        263   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.631E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -1.095E-21   AT NODE        106   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       165.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.027E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.400    
 STEP TIME COMPLETED        1.60    ,  TOTAL TIME COMPLETED         1.60    


  INCREMENT    21 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       73.7       TIME AVG. FORCE        38.5    
 LARGEST SCALED RESIDUAL FORCE     -1.645E-11   AT NODE        257   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.645E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -5.803E-22   AT NODE        103   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       173.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.078E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.420    
 STEP TIME COMPLETED        1.68    ,  TOTAL TIME COMPLETED         1.68    


  INCREMENT    22 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       77.2       TIME AVG. FORCE        40.2    
 LARGEST SCALED RESIDUAL FORCE     -1.643E-11   AT NODE        263   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.643E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        4.034E-22   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       181.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.130E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.440    
 STEP TIME COMPLETED        1.76    ,  TOTAL TIME COMPLETED         1.76    


  INCREMENT    23 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  5ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       80.7       TIME AVG. FORCE        42.0    
 LARGEST SCALED RESIDUAL FORCE     -1.503E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.503E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        7.775E-22   AT NODE        106   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       189.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.181E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.460    
 STEP TIME COMPLETED        1.84    ,  TOTAL TIME COMPLETED         1.84    


  INCREMENT    24 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  10ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       84.2       TIME AVG. FORCE        43.7    
 LARGEST SCALED RESIDUAL FORCE     -1.423E-11   AT NODE         95   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.423E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -6.722E-22   AT NODE        106   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       198.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.232E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.480    
 STEP TIME COMPLETED        1.92    ,  TOTAL TIME COMPLETED         1.92    


  INCREMENT    25 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  12ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       87.7       TIME AVG. FORCE        45.5    
 LARGEST SCALED RESIDUAL FORCE      2.818E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      2.818E-11
 LARGEST INCREMENT OF DISP.         2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -4.397E-21   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       206.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.284E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION     5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.500    
 STEP TIME COMPLETED        2.00    ,  TOTAL TIME COMPLETED         2.00    


  INCREMENT    26 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  13ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       84.2       TIME AVG. FORCE        47.0    
 LARGEST SCALED RESIDUAL FORCE     -9.123E-11   AT NODE        245   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -9.123E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -4.584E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       214.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.232E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.520    
 STEP TIME COMPLETED        2.08    ,  TOTAL TIME COMPLETED         2.08    


  INCREMENT    27 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  14ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       80.7       TIME AVG. FORCE        48.2    
 LARGEST SCALED RESIDUAL FORCE     -1.756E-11   AT NODE        258   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.756E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -5.431E-19   AT NODE         91   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       221.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.181E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.540    
 STEP TIME COMPLETED        2.16    ,  TOTAL TIME COMPLETED         2.16    


  INCREMENT    28 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  6ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       77.2       TIME AVG. FORCE        49.3    
 LARGEST SCALED RESIDUAL FORCE      2.316E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      2.316E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.727E-19   AT NODE         91   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       227.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.130E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.560    
 STEP TIME COMPLETED        2.24    ,  TOTAL TIME COMPLETED         2.24    


  INCREMENT    29 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       73.7       TIME AVG. FORCE        50.1    
 LARGEST SCALED RESIDUAL FORCE      2.121E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      2.121E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -1.537E-21   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       232.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.078E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.580    
 STEP TIME COMPLETED        2.32    ,  TOTAL TIME COMPLETED         2.32    


  INCREMENT    30 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       70.2       TIME AVG. FORCE        50.8    
 LARGEST SCALED RESIDUAL FORCE     -1.856E-11   AT NODE        257   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.856E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -3.452E-22   AT NODE        104   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       236.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.027E-31   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.600    
 STEP TIME COMPLETED        2.40    ,  TOTAL TIME COMPLETED         2.40    


  INCREMENT    31 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       66.7       TIME AVG. FORCE        51.3    
 LARGEST SCALED RESIDUAL FORCE     -1.907E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.907E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.383E-21   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       239.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      9.756E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.620    
 STEP TIME COMPLETED        2.48    ,  TOTAL TIME COMPLETED         2.48    


  INCREMENT    32 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  10ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       63.2       TIME AVG. FORCE        51.7    
 LARGEST SCALED RESIDUAL FORCE      1.918E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.918E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -8.020E-22   AT NODE        100   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       241.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      9.243E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.640    
 STEP TIME COMPLETED        2.56    ,  TOTAL TIME COMPLETED         2.56    


  INCREMENT    33 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  7ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       59.7       TIME AVG. FORCE        51.9    
 LARGEST SCALED RESIDUAL FORCE     -1.408E-11   AT NODE        307   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.408E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -5.612E-22   AT NODE        101   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       243.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      8.729E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.660    
 STEP TIME COMPLETED        2.64    ,  TOTAL TIME COMPLETED         2.64    


  INCREMENT    34 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       56.2       TIME AVG. FORCE        52.0    
 LARGEST SCALED RESIDUAL FORCE     -2.408E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -2.408E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        5.782E-22   AT NODE        101   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       244.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      8.216E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.680    
 STEP TIME COMPLETED        2.72    ,  TOTAL TIME COMPLETED         2.72    


  INCREMENT    35 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       52.6       TIME AVG. FORCE        52.0    
 LARGEST SCALED RESIDUAL FORCE     -2.187E-11   AT NODE        263   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -2.187E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.963E-22   AT NODE        292   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       245.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      7.702E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.700    
 STEP TIME COMPLETED        2.80    ,  TOTAL TIME COMPLETED         2.80    


  INCREMENT    36 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  2ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       49.1       TIME AVG. FORCE        52.0    
 LARGEST SCALED RESIDUAL FORCE      1.852E-11   AT NODE        261   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.852E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -3.723E-22   AT NODE         93   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       245.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      7.189E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.720    
 STEP TIME COMPLETED        2.88    ,  TOTAL TIME COMPLETED         2.88    


  INCREMENT    37 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  6ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       45.6       TIME AVG. FORCE        51.8    
 LARGEST SCALED RESIDUAL FORCE      1.716E-11   AT NODE        290   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.716E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        4.579E-22   AT NODE          8   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       245.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      6.675E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.740    
 STEP TIME COMPLETED        2.96    ,  TOTAL TIME COMPLETED         2.96    


  INCREMENT    38 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  11ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       42.1       TIME AVG. FORCE        51.5    
 LARGEST SCALED RESIDUAL FORCE     -1.644E-11   AT NODE        263   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.644E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -3.429E-22   AT NODE         99   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       244.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      6.162E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.760    
 STEP TIME COMPLETED        3.04    ,  TOTAL TIME COMPLETED         3.04    


  INCREMENT    39 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  7ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       38.6       TIME AVG. FORCE        51.2    
 LARGEST SCALED RESIDUAL FORCE     -1.416E-11   AT NODE        308   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.416E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -3.650E-22   AT NODE        107   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       243.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      5.648E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.780    
 STEP TIME COMPLETED        3.12    ,  TOTAL TIME COMPLETED         3.12    


  INCREMENT    40 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       35.1       TIME AVG. FORCE        50.8    
 LARGEST SCALED RESIDUAL FORCE     -2.216E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -2.216E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        3.756E-22   AT NODE        100   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       241.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      5.135E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.800    
 STEP TIME COMPLETED        3.20    ,  TOTAL TIME COMPLETED         3.20    


  INCREMENT    41 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  12ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       31.6       TIME AVG. FORCE        50.3    
 LARGEST SCALED RESIDUAL FORCE      1.801E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.801E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -2.939E-22   AT NODE         91   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       239.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      4.621E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.820    
 STEP TIME COMPLETED        3.28    ,  TOTAL TIME COMPLETED         3.28    


  INCREMENT    42 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       28.1       TIME AVG. FORCE        49.8    
 LARGEST SCALED RESIDUAL FORCE     -1.296E-11   AT NODE        255   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.296E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.891E-22   AT NODE         93   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       237.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      4.108E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.840    
 STEP TIME COMPLETED        3.36    ,  TOTAL TIME COMPLETED         3.36    


  INCREMENT    43 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  8ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       24.6       TIME AVG. FORCE        49.2    
 LARGEST SCALED RESIDUAL FORCE      1.044E-11   AT NODE        306   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.044E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.944E-22   AT NODE         99   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       234.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      3.594E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.860    
 STEP TIME COMPLETED        3.44    ,  TOTAL TIME COMPLETED         3.44    


  INCREMENT    44 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  2ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       21.1       TIME AVG. FORCE        48.6    
 LARGEST SCALED RESIDUAL FORCE     -1.373E-11   AT NODE        257   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.373E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.022E-22   AT NODE          7   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       232.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      3.081E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.880    
 STEP TIME COMPLETED        3.52    ,  TOTAL TIME COMPLETED         3.52    


  INCREMENT    45 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  3ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       17.6       TIME AVG. FORCE        47.9    
 LARGEST SCALED RESIDUAL FORCE      2.041E-11   AT NODE        290   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      2.041E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        3.210E-22   AT NODE        105   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       229.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      2.567E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.900    
 STEP TIME COMPLETED        3.60    ,  TOTAL TIME COMPLETED         3.60    


  INCREMENT    46 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       14.1       TIME AVG. FORCE        47.2    
 LARGEST SCALED RESIDUAL FORCE     -1.600E-11   AT NODE        263   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.600E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.       -4.217E-22   AT NODE        104   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       225.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      2.054E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.920    
 STEP TIME COMPLETED        3.68    ,  TOTAL TIME COMPLETED         3.68    


  INCREMENT    47 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  10ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       10.6       TIME AVG. FORCE        46.4    
 LARGEST SCALED RESIDUAL FORCE     -2.289E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -2.289E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        1.395E-22   AT NODE        110   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       222.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.540E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: TOWER-1                                                                         
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.940    
 STEP TIME COMPLETED        3.76    ,  TOTAL TIME COMPLETED         3.76    


  INCREMENT    48 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  4ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       7.09       TIME AVG. FORCE        45.6    
 LARGEST SCALED RESIDUAL FORCE      1.581E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE      1.581E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.793E-22   AT NODE         99   DOF  3
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       218.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.027E-32   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.960    
 STEP TIME COMPLETED        3.84    ,  TOTAL TIME COMPLETED         3.84    


  INCREMENT    49 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  11ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                       1.04       TIME AVG. FORCE        44.7    
 LARGEST SCALED RESIDUAL FORCE     -2.230E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -2.230E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        2.273E-22   AT NODE        100   DOF  1
   INSTANCE: GBS-1                                                                           
          THE FORCE     EQUILIBRIUM RESPONSE WAS LINEAR IN THIS INCREMENT

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       214.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED  0.980    
 STEP TIME COMPLETED        3.92    ,  TOTAL TIME COMPLETED         3.92    


  INCREMENT    50 STARTS. ATTEMPT NUMBER  1, TIME INCREMENT  8.000E-02
 
	SYMMETRIC PURE THREAD-BASED DIRECT SPARSE SOLVER RUNNING ON
 	1 HOST x 1 MPI RANK PER HOST x 1 THREAD PER RANK
        NUMBER OF EQUATIONS:  1518
        NUMBER OF RHS:        1
        NUMBER OF FLOPS:      1.286e+07
        SOLVER ELAPSED TIME:  7ms

               CONVERGENCE CHECKS FOR EQUILIBRIUM ITERATION     1


 AVERAGE FORCE                      8.834E-14   TIME AVG. FORCE        44.7    
 LARGEST SCALED RESIDUAL FORCE     -1.556E-11   AT NODE        260   DOF  3
   INSTANCE: GBS-1                                                                           
  CORRESPONDING RESIDUAL FORCE     -1.556E-11
 LARGEST INCREMENT OF DISP.        -2.292E-07   AT NODE        103   DOF  3
   INSTANCE: GBS-1                                                                           
 LARGEST CORRECTION TO DISP.        3.099E-22   AT NODE        307   DOF  3
   INSTANCE: GBS-1                                                                           
          THERE IS ZERO FORCE     EVERYWHERE

 AVERAGE MOMENT                      0.00       TIME AVG. MOMENT       210.    
                                                (FROM FORCE     FIELD)
 ALL MOMENT    RESIDUALS ARE ZERO
 LARGEST INCREMENT OF ROTATION      1.187E-66   AT NODE          1   DOF  6
   INSTANCE: {assembly node}                                                                 
 LARGEST CORRECTION TO ROTATION    -5.135E-33   AT NODE          1   DOF  4
   INSTANCE: {assembly node}                                                                 
          THERE IS ZERO MOMENT    EVERYWHERE

 ITERATION SUMMARY FOR THE INCREMENT:   1 TOTAL ITERATIONS, OF WHICH
   0 ARE SEVERE DISCONTINUITY ITERATIONS AND  1 ARE EQUILIBRIUM ITERATIONS.

 TIME INCREMENT COMPLETED  8.000E-02,  FRACTION OF STEP COMPLETED   1.00    
 STEP TIME COMPLETED        4.00    ,  TOTAL TIME COMPLETED         4.00    


          THE ANALYSIS HAS BEEN COMPLETED



     ANALYSIS SUMMARY:
     TOTAL OF         50  INCREMENTS
                       0  CUTBACKS IN AUTOMATIC INCREMENTATION
                      50  ITERATIONS INCLUDING CONTACT ITERATIONS IF PRESENT
                      50  PASSES THROUGH THE EQUATION SOLVER OF WHICH 
                       1  INVOLVE MATRIX DECOMPOSITION, INCLUDING
                       0  DECOMPOSITION(S) OF THE MASS MATRIX
                       1  REORDERING OF EQUATIONS TO MINIMIZE WAVEFRONT
                       0  ADDITIONAL RESIDUAL EVALUATIONS FOR LINE SEARCHES
                       0  ADDITIONAL OPERATOR EVALUATIONS FOR LINE SEARCHES
                       1  WARNING MESSAGES DURING USER INPUT PROCESSING
                       1  WARNING MESSAGES DURING ANALYSIS
                       0  ANALYSIS WARNINGS ARE NUMERICAL PROBLEM MESSAGES
                       0  ANALYSIS WARNINGS ARE NEGATIVE EIGENVALUE MESSAGES
                       0  ERROR MESSAGES



     JOB TIME SUMMARY
       USER TIME (SEC)      =      17.    
       SYSTEM TIME (SEC)    =      6.7    
       TOTAL CPU TIME (SEC) =      24.    
       WALLCLOCK TIME (SEC) =           11
       MEMORY PEAK (GB)     =            0
