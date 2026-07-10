% --------------------------------------------------------
% --------------- Instantiate Argument? ------------------
% --------------------------------------------------------

comparitor(X):-
    member(X, [less_than,less_or_equal, greater_than, greater_or_equal]).
% Instantiate self
X(X),{X}. 
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
waypoint(A,B,Avoid,Resume,Side1,Side2,Magnitude):- 
    P(Magnitude),
    Q(A,B),
    {P,Q},
    [Avoid,Resume,Side1,Side2].
waypoint(A,B,Avoid,Resume,Side1,Side2,Magnitude):- 
    P(Magnitude),
    Q(A,B),
    {P,Q},
    [Avoid,Resume,Side2].
waypoint(A,B,Avoid,Resume,Side1,Side2,Magnitude):- 
    P(Magnitude),
    Q(A,B),
    {P,Q},
    [Avoid,Resume,Side1].
waypoint(A,B,Avoid,Resume,Side1,Side2,Magnitude):- 
    P(Magnitude),
    Q(A,B),
    {P,Q},
    [Avoid,Resume].

% --------------------------------------------------------
% ---------------- Condition Chaining --------------------
% --------------------------------------------------------
P(X,Y):-
    Q(X,Y),
    {P,Q}.
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