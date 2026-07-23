% --------------------------------------------------------
% --------------- Instantiate Argument? ------------------
% --------------------------------------------------------

comparitor(X):-
    member(X, [less_than,less_or_equal, greater_than, greater_or_equal]).
% % Instantiate self
% X(X),{X}. 
% Single Condition
P(X):-
    comparitor(Q),
    Q(X,A),
    {P,Q},
    [A].
% Double Condition
P(X):-
    comparitor(Q),
    comparitor(R),
    Q(X,A),
    R(X,B),
    {P,Q,R},
    [A,B].

% --------------------------------------------------------
% ------------------ Head Meta Rules ---------------------
% --------------------------------------------------------
waypoint(A,B,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    Q(A,B),
    {P,Q},
    [Avoid,Resume,Side,End].
waypoint(A,B,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    Q(A,B),
    {P,Q},
    [Avoid,Resume,End].
waypoint(A,B,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    Q(A,B),
    {P,Q},
    [Avoid,Resume,Side].
waypoint(A,B,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    Q(A,B),
    {P,Q},
    [Avoid,Resume].

% --------------------------------------------------------
% ---------------- Condition Chaining --------------------
% --------------------------------------------------------
P(X,Y):-
    Q(X,Y,A),
    {P,Q,A}.
P(X,Y):-
    Q(X,Y,A,B),
    {P,Q,A,B}.

P(X,Y):-
    Q(X,Y),
    R(X,Y),
    {P,Q,R}.
P(X,Y):-
    Q(X,Y,A),
    R(X,Y),
    {P,Q,R,A}.
P(X,Y):-
    Q(X,Y,A,B),
    R(X,Y),
    {P,Q,R,A,B}.

insubstantial(insubstantial).
small(small).
moderate(moderate).
large(large).
very_large(very_large).

% waypoint(Arg_0,Arg_1,no_risk,no_risk,port,forward,Arg_2):-small(Arg_2),pred_862(Arg_0,Arg_1).
% pred_862(Arg_0,Arg_1):-sector(Arg_0,Arg_1,ahead).
% waypoint(Arg_0,Arg_1,no_risk,no_risk,port,forward,Arg_2):-large(Arg_2),pred_1152(Arg_0,Arg_1).
% pred_1152(Arg_0,Arg_1):-sector(Arg_0,Arg_1,port_bow_broad).
% waypoint(Arg_0,Arg_1,no_risk,no_risk,Arg_2,aft,Arg_3):-moderate(Arg_3),pred_666(Arg_0,Arg_1).
% pred_666(Arg_0,Arg_1):-tcpa(Arg_0,Arg_1,medium).