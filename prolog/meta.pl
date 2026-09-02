% --------------------------------------------------------
% ---------------- Take action clauses  ------------------
% --------------------------------------------------------
P(X):- Q(X), R(X). % Branch with agent
P(X):- Q(X,Y), R(X,Y), {P,Q,R}. % Branch with shared vessel
P(X):- Q(X,_,A), {P,Q,A}. % Property true for any vessel
P(X):- Q(X,_,A,B), {P,Q,A,B}. % Property true for any vessel


% --------------------------------------------------------
% ---------------- Vessel Pair Clauses  ------------------
% --------------------------------------------------------

P(X,Y):- Q(X,Y), R(X,Y), {P,Q,R}. % Branch
P(X,Y):- Q(X,Y,A), [P,Q,A]. % Has 1 constant property
P(X,Y):- Q(X,Y,A,B), [P,Q,A,B]. % Has 2 constant property

% --------------------------------------------------------
% ----------------- Transitive Values --------------------
% --------------------------------------------------------
% Force transitive for tcpa - dcpa - range

% Set of comparitors
% comparitor(X):- member(X, [less_than,less_or_equal, greater_than, greater_or_equal]).

% % Single Comparison
% P(X,Y):-
%     tcpa(X,Y,Z),
%     comparitor(Q),
%     Q(Z,A),
%     [P,Q,A].
% P(X,Y):-
%     dcpa(X,Y,Z),
%     comparitor(Q),
%     Q(Z,A),
%     [P,Q,A].
% P(X,Y):-
%     range(X,Y,Z),
%     comparitor(Q),
%     Q(Z,A),
%     [P,Q,A].
% % Double comparison
% P(X,Y):-
%     tcpa(X,Y,Z),
%     comparitor(Q),
%     comparitor(R),
%     Q(Z,A),
%     R(Z,B),
%     {Q,R},
%     [P,A,B].
% P(X,Y):-
%     dcpa(X,Y,Z),
%     comparitor(Q),
%     comparitor(R),
%     Q(Z,A),
%     R(Z,B),
%     {Q,R},
%     [P,A,B].
% P(X,Y):-
%     range(X,Y,Z),
%     comparitor(Q),
%     comparitor(R),
%     Q(Z,A),
%     R(Z,B),
%     {Q,R},
%     [P,A,B].

% % --------------------------------------------------------
% % ----------- Compliance Condition Clauses ---------------
% % --------------------------------------------------------
% P(X,Y,Z):- comparitor(Q), Q(Z,A), R(X,Y), {P,Q,R,A}.
% P(X,Y,Z):- comparitor(Q), comparitor(R), Q(Z,A), R(Z,B), Z(X,Y), {P,Q,R,S,A,B}.



range_gt(X,Y,A):-
    range(X,Y,B),
    greater_than(B,A).
range_ge(X,Y,A):-
    range(X,Y,B),
    greater_or_equal(B,A).
range_lt(X,Y,A):-
    range(X,Y,B),
    less_than(B,A).
range_le(X,Y,A):-
    range(X,Y,B),
    less_or_equal(B,A).


dcpa_gt(X,Y,A):-
    dcpa(X,Y,B),
    greater_than(B,A).
dcpa_ge(X,Y,A):-
    dcpa(X,Y,B),
    greater_or_equal(B,A).
dcpa_lt(X,Y,A):-
    dcpa(X,Y,B),
    less_than(B,A).
dcpa_le(X,Y,A):-
    dcpa(X,Y,B),
    less_or_equal(B,A).

tcpa_gt(X,Y,A):-
    tcpa(X,Y,B),
    greater_than(B,A).
tcpa_ge(X,Y,A):-
    tcpa(X,Y,B),
    greater_or_equal(B,A).
tcpa_lt(X,Y,A):-
    tcpa(X,Y,B),
    less_than(B,A).
tcpa_le(X,Y,A):-
    tcpa(X,Y,B),
    less_or_equal(B,A).