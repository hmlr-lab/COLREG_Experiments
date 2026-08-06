% ----------------------------------------------------------------------------------------------------
waypoint(A,B,no_risk,no_risk,port,forward,C):-small(C),pred_862(A,B).
pred_862(A,B):-sector(A,B,ahead).
waypoint(A,B,no_risk,no_risk,port,forward,C):-large(C),pred_1152(A,B).
pred_1152(A,B):-sector(A,B,port_bow_broad).
waypoint(A,B,no_risk,no_risk,C,aft,D):-moderate(D),pred_666(A,B).
pred_666(A,B):-tcpa(A,B,medium).

waypoint(A,B,no_risk,no_risk,port,forward,small):-sector(A,B,ahead).
waypoint(A,B,no_risk,no_risk,port,forward,large):-sector(A,B,port_bow_broad).
waypoint(A,B,no_risk,no_risk,_,aft,moderate):-tcpa(A,B,medium).
% ----------------------------------------------------------------------------------------------------
% ----------------------------------------------------------------------------------------------------
arc_overtaking(A,B):-
    tcpa_closing(A,B),
    starboard(A,B).
arc_overtaking(A,B):-
    tcpa(A,B,medium),
    close_quarters(A,B).
arc_overtaking(A,B):-
    tcpa(A,B,medium),
    close_quarters(A,B).
waypoint(A,B,no_risk,no_risk,port,C,small):-
    encounter_and_duty(A,B,rule14_head_on,rule16_giveway),
    tcpa_closing(A,B).
waypoint(A,B,no_risk,no_risk,C,D,E):-
    moderate(E),
    encounter_and_duty(A,B,rule13_overtaking,rule16_giveway),
    tcpa_closing(A,B).
waypoint(A,B,no_risk,no_risk,C,D,E):-
    moderate(E),
    encounter_and_duty(A,B,rule13_overtaking,rule16_giveway),
    close_quarters(A,B).
waypoint(A,B,no_risk,no_risk,C,D,E):-
    large(E),
    encounter_and_duty(A,B,rule15_crossing,rule17_standon),
    close_quarters_developing(A,B).
% ----------------------------------------------------------------------------------------------------
pred_1(A,B):-
    tcpa(A,B,short),
    close_quarters_developing(A,B).
waypoint(A,B,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    large(Arg_4),
    encounter_and_duty(A,B,rule15_crossing,rule17_standon),
    pred_1(A,B).
waypoint(A,B,no_risk,no_risk,port,Arg_2,Arg_3):-
    small(Arg_3),
    encounter_and_duty(A,B,rule14_head_on,rule16_giveway),
    tcpa_closing(A,B).
waypoint(A,B,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    moderate(Arg_4),
    encounter_and_duty(A,B,rule13_overtaking,rule16_giveway),
    close_quarters(A,B).
waypoint(A,B,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    moderate(Arg_4),
    encounter_and_duty(A,B,rule13_overtaking,rule16_giveway),
    close_quarters(A,B).
waypoint(A,B,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    moderate(Arg_4),
    encounter_and_duty(A,B,rule15_crossing,rule16_giveway),
    close_quarters_developing(A,B).

pred_1(A,B):-
    tcpa(A,B,short),
    close_quarters_developing(A,B).

waypoint(A,B,no_risk,no_risk,_,_,large):-
    encounter_and_duty(A,B,rule15_crossing,rule17_standon),
    tcpa(A,B,short),
    close_quarters_developing(A,B).
waypoint(A,B,no_risk,no_risk,port,_,small):-
    encounter_and_duty(A,B,rule14_head_on,rule16_giveway),
    tcpa_closing(A,B).
waypoint(A,B,no_risk,no_risk,_,_,moderate):-
    encounter_and_duty(A,B,rule13_overtaking,rule16_giveway),
    close_quarters(A,B).
waypoint(A,B,no_risk,no_risk,_,_,moderate):-
    encounter_and_duty(A,B,rule13_overtaking,rule16_giveway),
    close_quarters(A,B).
waypoint(A,B,no_risk,no_risk,_,_,moderate):-
    encounter_and_duty(A,B,rule15_crossing,rule16_giveway),
    close_quarters_developing(A,B).

waypoint(A,B,C,D,E,F):-
    pred_1(A,B,E),
----------------------------------------------------------------------------------------------------