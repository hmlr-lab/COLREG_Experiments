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
:- abolish(ample_time/2).
:- abolish(is_range/1).
:- abolish(is_dcpa/1).
:- abolish(is_tcpa/1).
:- abolish(actionable_range/2).
:- abolish(collision_risk/2).
:- abolish(mutual_ahead/2).


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
:- dynamic greater_than/2.
:- dynamic greater_or_equal/2.
:- dynamic less_and_adjacent/2. 


:- discontiguous less_and_adjacent/2.
:- discontiguous greater_or_equal/2.
:- discontiguous greater_than/2.
:- discontiguous less_than/2.
:- discontiguous less_or_equal/2. 

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

% range
less_and_adjacent(far,very_far).
less_and_adjacent(middle,far).
less_and_adjacent(near,middle).
less_and_adjacent(very_near,near).

% tcpa
less_and_adjacent(long,very_long).
less_and_adjacent(medium,long).
less_and_adjacent(short,medium).
less_and_adjacent(immediate,short).

% dcpa
less_and_adjacent(marginal,safe).
less_and_adjacent(close,marginal).
less_and_adjacent(very_close,close).
less_and_adjacent(critical,very_close).

% turn magnitude
less_and_adjacent(large,very_large).
less_and_adjacent(moderate,large).
less_and_adjacent(small,moderate).
less_and_adjacent(insubstantial,small).

% Avoid Resume Risks
less_and_adjacent(no_risk, risk_developing).
less_and_adjacent(risk_developing, medium_close).
less_and_adjacent(medium_close, medium_veryclose).
less_and_adjacent(medium_veryclose, medium_close).
less_and_adjacent(medium_critical, short_close).
less_and_adjacent(short_close, short_veryclose).
less_and_adjacent(short_veryclose, short_critical).
less_and_adjacent(short_critical, imminent_close).
less_and_adjacent(imminent_close, imminent_veryclose).
less_and_adjacent(imminent_veryclose, imminent_critical).

less_than(X,Y) :- 
    less_and_adjacent(X,Z), 
    less_than(Z,Y).
less_than(X,Y) :-
    less_and_adjacent(X,Y).

greater_than(X,Y) :- 
    less_and_adjacent(Z,X), 
    greater_than(Z,Y).
greater_than(X,Y) :-
    less_and_adjacent(Y,X).

less_or_equal(X,Y) :- X = Y.
less_or_equal(X,Y) :- less_than(X,Y).

greater_or_equal(X,Y) :- X = Y.
greater_or_equal(X,Y) :- greater_than(X,Y).

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

is_range(Range) :- member(Range,[very_far,far,middle,near,very_near]).
is_dcpa(DCPA) :- member(DCPA,[safe,marginal,close,very_close,critical]). 
is_tcpa(TCPA) :- member(TCPA,[very_long,long,medium,short,immediate]).
is_turn(Turn) :- member(Turn, [very_large, large, moderate, small, insubstantial]).



%  CONCEPTUAL GROUPINGS

dcpa_acceptable(X,Y) :- dcpa(X,Y,marginal).
dcpa_acceptable(X,Y) :- dcpa(X,Y,safe).
dcpa_unacceptable(X,Y) :- not(dcpa_acceptable(X,Y)).

tcpa_closing(X,Y) :- not(tcpa(X,Y,opening)).

actionable_range(X,Y) :- not(range(X,Y,very_far)).


%  ample_time  (Rule 8(a))

ample_time(X,Y)    :- tcpa(X,Y,medium).
ample_time(X,Y)    :- tcpa(X,Y,long).
ample_time(X,Y)    :- tcpa(X,Y,very_long).



%  RISK OF COLLISION (Rule 7)

collision_risk(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,imminent).
collision_risk(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,short).
collision_risk(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,medium).


%  CLOSE-QUARTERS SITUATION (Rule 8)

close_quarters_developing(X,Y) :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,far).
close_quarters_developing(X,Y) :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,middle).
close_quarters(X,Y)            :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,near).
close_quarters(X,Y)            :- dcpa_unacceptable(X,Y), tcpa_closing(X,Y), range(X,Y,very_near).


%  ENCOUNTER  (three types, one per pair) - the finding of fact

encounter(X,Y,rule13_overtaking) :-
    collision_risk(X,Y),
    arc_overtaking(X,Y).

encounter(X,Y,rule14_head_on) :-
    collision_risk(X,Y),
    mutual_ahead(X,Y),
    not(arc_overtaking(X,Y)),
    not(arc_overtaking(Y,X)).

encounter(X,Y,rule15_crossing) :-
    collision_risk(X,Y),
    not(arc_overtaking(X,Y)),
    not(arc_overtaking(Y,X)),
    not(mutual_ahead(X,Y)).

mutual_ahead(X,Y):-
    sector(X,Y,ahead),
    sector(Y,X,ahead).
%  ENCOUNTER + DUTY  (Own, Target, Encounter, Duty) - the conclusion of law

encounter_and_duty(X,Y,rule13_overtaking,rule16_giveway) :- encounter(X,Y,rule13_overtaking).   % X overtakes Y
encounter_and_duty(X,Y,rule13_overtaking,rule17_standon) :- encounter(Y,X,rule13_overtaking).   % Y overtakes X
encounter_and_duty(X,Y,rule14_head_on,rule16_giveway)    :- encounter(X,Y,rule14_head_on).        % head-on: mutual
encounter_and_duty(X,Y,rule15_crossing,rule16_giveway)   :- encounter(X,Y,rule15_crossing), starboard(X,Y).
encounter_and_duty(X,Y,rule15_crossing,rule17_standon)   :- encounter(X,Y,rule15_crossing), port(X,Y).


%  CONDUCT  (action form of the duty) - only stand-on is sub-classified, by ample_time

conduct(X,Y,rule17_standon_maintain) :- encounter_and_duty(X,Y,_,rule17_standon), ample_time(X,Y).
conduct(X,Y,rule17_standon_may_act)  :- encounter_and_duty(X,Y,_,rule17_standon), tcpa(X,Y,short).
conduct(X,Y,rule17_standon_must_act) :- encounter_and_duty(X,Y,_,rule17_standon), tcpa(X,Y,imminent).


%  EMERGENCY  - in extremis, departure from any rule; encounter-agnostic (Rule 2(b))

rule2_extremis(X,Y) :- dcpa_unacceptable(X,Y), tcpa(X,Y,imminent).
%might be a cleaner way to do this
