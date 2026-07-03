:- style_check(-discontiguous).
:- set_prolog_flag(verbose, silent).

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


%  CONCEPTUAL GROUPINGS

dcpa_unsafe(X,Y) :- dcpa(X,Y,very_close).
dcpa_unsafe(X,Y) :- dcpa(X,Y,close).
dcpa_unsafe(X,Y) :- dcpa(X,Y,near).
dcpa_safe(X,Y) :- dcpa(X,Y,marginal).
dcpa_safe(X,Y) :- dcpa(X,Y,safe).

tcpa_closing(X,Y) :- \+ tcpa(X,Y,opening).

range_actionable(X,Y) :- \+ range(X,Y,very_far).


%  time_ample  (Rule 8(a))

time_ample(X,Y)    :- tcpa(X,Y,medium).
time_ample(X,Y)    :- tcpa(X,Y,long).
time_ample(X,Y)    :- tcpa(X,Y,very_long).



%  RISK OF COLLISION (Rule 7)

risk_collision(X,Y) :- dcpa_unsafe(X,Y), tcpa(X,Y,imminent).
risk_collision(X,Y) :- dcpa_unsafe(X,Y), tcpa(X,Y,short).
risk_collision(X,Y) :- dcpa_unsafe(X,Y), tcpa(X,Y,medium).


%  CLOSE-QUARTERS SITUATION (Rule 8)

close_quarters_developing(X,Y) :- dcpa_unsafe(X,Y), tcpa_closing(X,Y), range(X,Y,middle).
close_quarters_developing(X,Y) :- dcpa_unsafe(X,Y), tcpa_closing(X,Y), range(X,Y,far).
close_quarters(X,Y)            :- dcpa_unsafe(X,Y), tcpa_closing(X,Y), range(X,Y,close).
close_quarters(X,Y)            :- dcpa_unsafe(X,Y), tcpa_closing(X,Y), range(X,Y,very_close).


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

rule2_extremis(X,Y) :- dcpa_unsafe(X,Y), tcpa(X,Y,imminent).
%might be a cleaner way to do this


