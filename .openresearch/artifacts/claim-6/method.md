# Claim 6 method

The primary verifier exhausts both possible meta-training task states and both
possible fresh task states with rational arithmetic. It separately checks all
three clauses of Assumption 3.12, the common `p=3` moment requirement, the
empirical risk, conditional population risk, event probability, and displayed
zero right-hand side.

The independent checker reconstructs the model without importing the primary
verifier and performs every within-task replacement and test-sample comparison
on the complete finite domain.

The negative control performs the whole-task replacement used in equation
(104). It changes squared loss by one, which the stated `H=0` does not cover.
A genuine task-level envelope of one covers it exactly.
