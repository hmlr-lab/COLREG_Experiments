% --------------------------------------------------------
% --------------- Instantiate Argument? ------------------
% --------------------------------------------------------

comparitor(X):-
    member(X, [less_than,less_or_equal, greater_than, greater_or_equal]).
% % Instantiate self
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

% Force transitive for tcpa - dcpa - range
% Single Comparison
P(X,Y):-
    tcpa(X,Y,Z),
    comparitor(Q),
    Q(Z,A),
    [P,Q,A].
P(X,Y):-
    dcpa(X,Y,Z),
    comparitor(Q).
    Q(Z,A).
    [P,Q,A].
P(X,Y):-
    range(X,Y,Z),
    comparitor(Q),
    Q(Z,A),
    [P,Q,A].
% Double comparison
P(X,Y):-
    tcpa(X,Y,Z),
    comparitor(Q),
    comparitor(R),
    Q(Z,A),
    R(Z,B),
    {Q,R},
    [P,A,B].
P(X,Y):-
    dcpa(X,Y,Z),
    comparitor(Q),
    comparitor(R),
    Q(Z,A),
    R(Z,B),
    {Q,R},
    [P,A,B].
P(X,Y):-
    range(X,Y,Z),
    comparitor(Q),
    comparitor(R),
    Q(Z,A),
    R(Z,B),
    {Q,R},
    [P,A,B].

% --------------------------------------------------------
% ---------------- Condition Chaining --------------------
% ----P(X,Y):-
%     Q(X,Y,A),
%     {P,Q,A}.
% P(X,Y):-
%     Q(X,Y,A,B),
%     {P,Q,A,B}.

% P(X,Y):-
%     Q(X,Y),
%     R(X,Y),
%     {P,Q,R}.
% P(X,Y):-
%     Q(X,Y,A),
%     R(X,Y),
%     {P,Q,R,A}.
% P(X,Y):-
%     Q(X,Y,A,B),
%     R(X,Y),
%     {P,Q,R,A,B}.
----------------------------------------------------
% 
% --------------------------------------------------------
% ---------------- Take action clauses  ------------------
% --------------------------------------------------------
P(X):- Q(X,_,Z), R(Z), {P,Q,R}.
P(X):- Q(X), R(X).