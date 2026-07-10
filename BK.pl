:- style_check(-discontiguous).
:- set_prolog_flag(verbose, silent).

:- abolish(port_forward/2).
:- abolish(port_aft/2).
:- abolish(starboard_forward/2).
:- abolish(starboard_aft/2).
:- abolish(port/2).
:- abolish(starboard/2).
:- abolish(forward/2).
:- abolish(aft/2).
:- abolish(dcpa_unsafe/2).
:- abolish(dcpa_safe/2).
:- abolish(tcpa_closing/2).
:- abolish(range_actionable/2).
:- abolish(time_ample/2).
:- abolish(risk_collision/2).
:- abolish(close_quarters_developing/2).
:- abolish(close_quarters/2).
:- abolish(encounter/3).
:- abolish(encounter_and_duty/4).
:- abolish(conduct/3).
:- abolish(rule2_extremis/2).
:- abolish(less_and_adjacent/2).
:- abolish(less_than/2).
:- abolish(less_or_equal/2).
:- abolish(greater_than/2).
:- abolish(greater_or_equal/2).
:- abolish(dcpa_acceptable/2).
:- abolish(dcpa_unacceptable/2).

:- dynamic sector/3.
:- dynamic range/3.
:- dynamic dcpa/3.
:- dynamic tcpa/3.
:- dynamic bearing/3.
:- dynamic distance/3.
:- dynamic arc_overtaking/2.
:- dynamic status/2.
:- dynamic waterway/2.
:- dynamic constraint_draught/1.
:- dynamic clock/1.
:- dynamic port_forward/2.
:- dynamic port_aft/2.
:- dynamic starboard_forward/2.
:- dynamic starboard_aft/2.
:- dynamic port/2.
:- dynamic starboard/2.
:- dynamic forward/2.
:- dynamic aft/2.
:- dynamic dcpa_unsafe/2.
:- dynamic dcpa_safe/2.
:- dynamic tcpa_closing/2.
:- dynamic range_actionable/2.
:- dynamic time_ample/3.
:- dynamic risk_collision/2.
:- dynamic close_quarters_developing/2.
:- dynamic close_quarters/2.
:- dynamic encounter/3.
:- dynamic encounter_and_duty/4.
:- dynamic conduct/4.
:- dynamic extremis_override/2.
:- dynamic cites/2.
:- dynamic less_and_adjacent/2.
:- dynamic less_than/2.
:- dynamic less_or_equal/2.
:- dynamic greater_than/2.
:- dynamic greater_or_equal/2.
:- dynamic cpa_acceptable/2.


%  GEOMETRIC ABSTRACTION

port_forward(X,Y)      :- sector(X,Y,port_bow_forward).
port_forward(X,Y)      :- sector(X,Y,port_bow_broad).
port_forward(X,Y)      :- sector(X,Y,port_beam_forward).
port_aft(X,Y)          :- sector(X,Y,port_beam_aft).
port_aft(X,Y)          :- sector(X,Y,port_quarter_broad).
port_aft(X,Y)          :- sector(X,Y,port_quarter_aft).
starboard_forward(X,Y) :- sector(X,Y,starboard_bow_forward).
starboard_forward(X,Y) :- sector(X,Y,starboard_bow_broad).
starboard_forward(X,Y) :- sector(X,Y,starboard_beam_forward).
starboard_aft(X,Y)     :- sector(X,Y,starboard_beam_aft).
starboard_aft(X,Y)     :- sector(X,Y,starboard_quarter_broad).
starboard_aft(X,Y)     :- sector(X,Y,starboard_quarter_aft).

port(X,Y)      :- port_forward(X,Y).
port(X,Y)      :- port_aft(X,Y).
port(X,Y)      :- sector(X,Y,port_beam).
starboard(X,Y) :- starboard_forward(X,Y).
starboard(X,Y) :- starboard_aft(X,Y).
starboard(X,Y) :- sector(X,Y,starboard_beam).
forward(X,Y)   :- port_forward(X,Y).
forward(X,Y)   :- starboard_forward(X,Y).
forward(X,Y)   :- sector(X,Y,ahead).
aft(X,Y)       :- port_aft(X,Y).
aft(X,Y)       :- starboard_aft(X,Y).
aft(X,Y)       :- sector(X,Y,astern).


% ORDERINGS

<<<<<<< HEAD
% range
less_and_adjacent(far,very_far).
less_and_adjacent(middle,far).
less_and_adjacent(near,middle).
less_and_adjacent(very_near,near).

less_than(X,Z) :- 
    range(_,_,X),
    less_and_adjacent(X,Y), 
    less_than(Y,Z).

less_than(X,Y) :-
    range(_,_,X),
    less_and_adjacent(X,Y).

less_or_equal(X,Y) :- 
    range(_,_,X),
    less_and_adjacent(Y,X).

less_or_equal(X,X) :- 
    range(_,_,X).

greater_than(X,Y) :- 
    range(_,_,X),
    less_than(Y,X).

greater_or_equal(X,Y) :- 
    range(_,_,X),
    greater_than(X,Y).

greater_or_equal(X,X) :- 
    range(_,_,X).

% dcpa
less_and_adjacent(marginal,safe).
less_and_adjacent(close,marginal).
less_and_adjacent(very_close,close).
less_and_adjacent(critical,very_close).


less_than(X,Z) :- 
    dcpa(_,_,X),
    less_and_adjacent(X,Y), 
    less_than(Y,Z).

less_than(X,Y) :-
    dcpa(_,_,X),
    less_and_adjacent(X,Y).

less_or_equal(X,Y) :- 
    dcpa(_,_,X),
    less_and_adjacent(Y,X).

less_or_equal(X,X) :- 
    dcpa(_,_,X).

greater_than(X,Y) :- 
    dcpa(_,_,X),
    less_than(Y,X).

greater_or_equal(X,Y) :- 
    dcpa(_,_,X),
    greater_than(X,Y).

greater_or_equal(X,X) :- 
    dcpa(_,_,X).


% tcpa
less_and_adjacent(long,very_long).
less_and_adjacent(medium,long).
less_and_adjacent(short,medium).
less_and_adjacent(immediate,short).


less_than(X,Z) :- 
    tcpa(_,_,X),
    less_and_adjacent(X,Y), 
    less_than(Y,Z).

less_than(X,Y) :-
    tcpa(_,_,X),
    less_and_adjacent(X,Y).

less_or_equal(X,Y) :- 
    tcpa(_,_,X),
    less_and_adjacent(Y,X).

less_or_equal(X,X) :- 
    tcpa(_,_,X).

greater_than(X,Y) :- 
    tcpa(_,_,X),
    less_than(Y,X).

greater_or_equal(X,Y) :- 
    tcpa(_,_,X),
    greater_than(X,Y).

greater_or_equal(X,X) :- 
    tcpa(_,_,X).





% turn magnitude
less_and_adjacent(large,very_large).
less_and_adjacent(moderate,large).
less_and_adjacent(small,moderate).
less_and_adjacent(insubstantial,small).

%less_than(X,Z) :- 
%   tcpa(_,_,X),
%   less_and_adjacent(X,Y), 
%   less_than(Y,Z).

%less_than(X,Y) :-
%    tcpa(_,_,X),
%    less_and_adjacent(X,Y).

%less_or_equal(X,Y) :- 
%    tcpa(_,_,X),
%    less_and_adjacent(Y,X).

%less_or_equal(X,X) :- 
%   tcpa(_,_,X).

%greater_than(X,Y) :- 
%    tcpa(_,_,X),
%    less_than(Y,X).

%greater_or_equal(X,Y) :- 
%    tcpa(_,_,X),
%    greater_than(X,Y).

%greater_or_equal(X,X) :- 
%    tcpa(_,_,X).






%turn_smaller(X,Z) :- turn_smaller_adjacent(X,Y), turn_smaller(Y,Z). % Recursion
%turn_smaller(X,Y) :- turn_smaller_adjacent(X,Y). % Base case
%turn_smaller_similar(X,Y) :- turn_smaller(X,Y). % Inclusive of boundary
%turn_smaller_similar(X,X).
%turn_larger(X,Y) :- turn_smaller(Y,X). % Inverse
%turn_larger_similar(X,Y) :- turn_larger(X,Y).
%turn_larger_similar(X,X).
%turn_smaller_adjacent(large,very_large).
%turn_smaller_adjacent(moderate,large).
%turn_smaller_adjacent(small,moderate).
%turn_smaller_adjacent(insubstantial,small).
=======
range_nearer(X,Z) :- range_nearer_adjacent(X,Y), range_nearer(Y,Z). % Recursion
range_nearer(X,Y) :- range_nearer_adjacent(X,Y). % Base case
range_nearer_similar(X,Y) :- range_nearer(X,Y). % Inclusive of boundary
range_nearer_similar(X,X).
range_farther(X,Y) :- range_nearer(Y,X). % Inverse
range_farther_similar(X,Y) :- range_farther(X,Y). % Inclusive of boundary
range_farther_similar(X,X).
range_nearer(far,very_far).
range_nearer(middle,far).
range_nearer(near,middle).
range_nearer(very_near,near).

dcpa_closer(X,Z) :- dcpa_closer_adjacent(X,Y), dcpa_closer(Y,Z). % Recursion
dcpa_closer(X,Y) :- dcpa_closer_adjacent(X,Y). % Base case
dcpa_closer_similar(X,Y) :- dcpa_closer(X,Y). % Inclusive of boundary
dcpa_closer_similar(X,X).
dcpa_safer(X,Y) :- dcpa_closer(Y,X). % Inverse
dcpa_safer_similar(X,Y) :- dcpa_safer(X,Y).
dcpa_safer_similar(X,X).
dcpa_closer(marginal,safe).
dcpa_closer(close,marginal).
dcpa_closer(very_close,close).
dcpa_closer(critical,very_close).

tcpa_sooner(X,Z) :- tcpa_sooner_adjacent(X,Y), tcpa_sooner(Y,Z). % Recursion
tcpa_sooner(X,Y) :- tcpa_sooner_adjacent(X,Y). % Base case
tcpa_sooner_similar(X,Y) :- tcpa_sooner(X,Y). % Inclusive of boundary
tcpa_sooner_similar(X,X).
tcpa_later(X,Y) :- tcpa_sooner(Y,X). % Inverse
tcpa_later_similar(X,Y) :- tcpa_later(X,Y).
tcpa_later_similar(X,X).
tcpa_sooner(long,very_long).
tcpa_sooner(medium,long).
tcpa_sooner(short,medium).
tcpa_sooner(immediate,short).
% Opening does not belong here

turn_smaller(X,Z) :- turn_smaller_adjacent(X,Y), turn_smaller(Y,Z). % Recursion
turn_smaller(X,Y) :- turn_smaller_adjacent(X,Y). % Base case
turn_smaller_similar(X,Y) :- turn_smaller(X,Y). % Inclusive of boundary
turn_smaller_similar(X,X).
turn_larger(X,Y) :- turn_smaller(Y,X). % Inverse
turn_larger_similar(X,Y) :- turn_larger(X,Y).
turn_larger_similar(X,X).
turn_smaller(long,very_long).
turn_smaller(medium,long).
turn_smaller(short,medium).
turn_smaller(immediate,short).
>>>>>>> 5e17b96ec22bdd732376bbc5504e07b29d1cd755


%  CONCEPTUAL GROUPINGS

dcpa_unacceptable(X,Y) :- dcpa(X,Y,critical).
dcpa_unacceptable(X,Y) :- dcpa(X,Y,very_close).
dcpa_unacceptable(X,Y) :- dcpa(X,Y,close).
dcpa_acceptable(X,Y) :- dcpa(X,Y,marginal).
dcpa_acceptable(X,Y) :- dcpa(X,Y,safe).

tcpa_closing(X,Y) :- not(tcpa(X,Y,opening)).

range_actionable(X,Y) :- not(range(X,Y,very_far)).


%  time_ample  (Rule 8(a))

time_ample(X,Y)    :- tcpa(X,Y,medium).
time_ample(X,Y)    :- tcpa(X,Y,long).
time_ample(X,Y)    :- tcpa(X,Y,very_long).



%  RISK OF COLLISION (Rule 7)

risk_collision(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,imminent).
risk_collision(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,short).
risk_collision(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,medium).


%  CLOSE-QUARTERS SITUATION (Rule 8)

close_quarters_developing(X,Y) :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,far).
close_quarters_developing(X,Y) :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,middle).
close_quarters(X,Y)            :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,near).
close_quarters(X,Y)            :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,very_near).


%  ENCOUNTER  (three types, one per pair) - the finding of fact

encounter(X,Y,rule13_overtaking) :-
    risk_collision(X,Y),
    arc_overtaking(X,Y).

encounter(X,Y,rule14_head_on) :-
    risk_collision(X,Y),
    sector(X,Y,ahead), sector(Y,X,ahead),
    not(encounter(X,Y,rule13_overtaking)),
    not(encounter(Y,X,rule13_overtaking)).

encounter(X,Y,rule15_crossing) :-
    risk_collision(X,Y),
    not(encounter(X,Y,rule13_overtaking)),
    not(encounter(Y,X,rule13_overtaking)),
    not(encounter(X,Y,rule14_head_on)).


%  ENCOUNTER + DUTY  (Own, Target, Encounter, Duty) - the conclusion of law

encounter_and_duty(X,Y,rule13_overtaking,rule16_giveway) :- encounter(X,Y,rule13_overtaking).   % X overtakes Y
encounter_and_duty(X,Y,rule13_overtaking,rule17_standon) :- encounter(Y,X,rule13_overtaking).   % Y overtakes X
encounter_and_duty(X,Y,rule14_head_on,rule16_giveway)    :- encounter(X,Y,rule14_head_on).        % head-on: mutual
encounter_and_duty(X,Y,rule15_crossing,rule16_giveway)   :- encounter(X,Y,rule15_crossing), starboard(X,Y).
encounter_and_duty(X,Y,rule15_crossing,rule17_standon)   :- encounter(X,Y,rule15_crossing), port(X,Y).


%  CONDUCT  (action form of the duty) - only stand-on is sub-classified, by time_ample

conduct(X,Y,rule17_standon_maintain) :- encounter_and_duty(X,Y,_,rule17_standon), time_ample(X,Y).
conduct(X,Y,rule17_standon_may_act)  :- encounter_and_duty(X,Y,_,rule17_standon), tcpa(X,Y,short).
conduct(X,Y,rule17_standon_must_act) :- encounter_and_duty(X,Y,_,rule17_standon), tcpa(X,Y,imminent).


%  EMERGENCY  - in extremis, departure from any rule; encounter-agnostic (Rule 2(b))

rule2_extremis(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,imminent).
%might be a cleaner way to do this
