sector(agent_1_1,cruiseliner_1_1,starboard_bow_forward).
range(agent_1_1,cruiseliner_1_1,far).
dcpa(agent_1_1,cruiseliner_1_1,very_close).
tcpa(agent_1_1,cruiseliner_1_1,medium).
sector(cruiseliner_1_1,agent_1_1,port_bow_forward).
sector(agent_2_1,cruiseliner_2_1,port_bow_broad).
range(agent_2_1,cruiseliner_2_1,close).
dcpa(agent_2_1,cruiseliner_2_1,very_close).
tcpa(agent_2_1,cruiseliner_2_1,short).
sector(cruiseliner_2_1,agent_2_1,starboard_bow_forward).
sector(agent_3_1,cruiseliner_3_1,ahead).
range(agent_3_1,cruiseliner_3_1,far).
dcpa(agent_3_1,cruiseliner_3_1,very_close).
tcpa(agent_3_1,cruiseliner_3_1,medium).
sector(cruiseliner_3_1,agent_3_1,ahead).
sector(agent_4_1,cruiseliner_4_1,ahead).
range(agent_4_1,cruiseliner_4_1,close).
dcpa(agent_4_1,cruiseliner_4_1,very_close).
tcpa(agent_4_1,cruiseliner_4_1,medium).
sector(cruiseliner_4_1,agent_4_1,astern).
arc_overtaking(agent_4_1,cruiseliner_4_1).
sector(agent_5_1,cruiseliner_5_1,ahead).
range(agent_5_1,cruiseliner_5_1,close).
dcpa(agent_5_1,cruiseliner_5_1,very_close).
tcpa(agent_5_1,cruiseliner_5_1,medium).
sector(cruiseliner_5_1,agent_5_1,astern).
arc_overtaking(agent_5_1,cruiseliner_5_1).


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


is_range(Range) :- member(Range,[very_far,far,middle,near,very_near]).
is_dcpa(DCPA) :- member(DCPA,[safe,marginal,close,very_close,critical]). 
is_tcpa(TCPA) :- member(TCPA,[very_long,long,medium,short,immediate]).

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
    sector(X,Y,ahead), sector(Y,X,ahead),
    not(encounter(X,Y,rule13_overtaking)),
    not(encounter(Y,X,rule13_overtaking)).

encounter(X,Y,rule15_crossing) :-
    collision_risk(X,Y),
    not(encounter(X,Y,rule13_overtaking)),
    not(encounter(Y,X,rule13_overtaking)),
    not(encounter(X,Y,rule14_head_on)).


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
