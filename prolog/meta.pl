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
waypoint(X,Y,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    encounter_and_duty(X,Y,Encounter,Duty),
    Q(X,Y),
    {P,Q},
    [Avoid,Resume,Side,End,Encounter,Duty].
waypoint(X,Y,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    encounter_and_duty(X,Y,Encounter,Duty),
    Q(X,Y),
    {P,Q},
    [Avoid,Resume,End,Encounter,Duty].
waypoint(X,Y,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    encounter_and_duty(X,Y,Encounter,Duty),
    Q(X,Y),
    {P,Q},
    [Avoid,Resume,Side,Encounter,Duty].
waypoint(X,Y,Avoid,Resume,Side,End,Turn):- 
    P(Turn),
    encounter_and_duty(X,Y,Encounter,Duty),
    Q(X,Y),
    {P,Q},
    [Avoid,Resume,Encounter,Duty].

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