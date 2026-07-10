% --------------------------------------------------------
% --------------- Instantiate Argument? ------------------
% --------------------------------------------------------
% Instantiate self
X(X),{X}. 
% Single Condition
P(X):-
    Q(X,A),
    {P,Q},
    [A].
% Double Condition
P(X):-
    Q(X,A),
    R(X,B),
    {P,Q,R},
    [A,B].

% --------------------------------------------------------
% ------------------ Head Meta Rules ---------------------
% --------------------------------------------------------
add_waypoint(A,B,DCPA1,DCPA2,Side1,Side2,Magnitude):- 
    P(DCPA1),
    Q(DCPA2),
    R(Magnitude),
    S(A,B),
    {P,Q,R,S},
    [Side1,Side2].
add_waypoint(A,B,DCPA1,DCPA2,Side1,Side2,Magnitude):- 
    P(DCPA1),
    Q(DCPA2),
    R(Magnitude),
    S(A,B),
    {P,Q,R,S},
    [Side2].
add_waypoint(A,B,DCPA1,DCPA2,Side1,Side2,Magnitude):- 
    P(DCPA1),
    Q(DCPA2),
    R(Magnitude),
    S(A,B),
    {P,Q,R,S},
    [Side1].
add_waypoint(A,B,DCPA1,DCPA2,Side1,Side2,Magnitude):- 
    P(DCPA1),
    Q(DCPA2),
    R(Magnitude),
    S(A,B),
    {P,Q,R,S}.

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