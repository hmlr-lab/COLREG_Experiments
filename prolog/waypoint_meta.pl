% --------------------------------------------------------
% ----------- Compliance Condition Clauses ---------------
% --------------------------------------------------------
P(X,Y,Z):- comparitor(Q), Q(Z,A), R(X,Y), {P,Q,R,A}.
P(X,Y,Z):- comparitor(Q), comparitor(R), Q(Z,A), R(Z,B), S(X,Y), {P,Q,R,S,A,B}.