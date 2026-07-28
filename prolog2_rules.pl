% ----------------------------------------------------------------------------------------------------
waypoint(Arg_0,Arg_1,no_risk,no_risk,port,forward,Arg_2):-small(Arg_2),pred_862(Arg_0,Arg_1).
pred_862(Arg_0,Arg_1):-sector(Arg_0,Arg_1,ahead).
waypoint(Arg_0,Arg_1,no_risk,no_risk,port,forward,Arg_2):-large(Arg_2),pred_1152(Arg_0,Arg_1).
pred_1152(Arg_0,Arg_1):-sector(Arg_0,Arg_1,port_bow_broad).
waypoint(Arg_0,Arg_1,no_risk,no_risk,Arg_2,aft,Arg_3):-moderate(Arg_3),pred_666(Arg_0,Arg_1).
pred_666(Arg_0,Arg_1):-tcpa(Arg_0,Arg_1,medium).

waypoint(Arg_0,Arg_1,no_risk,no_risk,port,forward,small):-sector(Arg_0,Arg_1,ahead).
waypoint(Arg_0,Arg_1,no_risk,no_risk,port,forward,large):-sector(Arg_0,Arg_1,port_bow_broad).
waypoint(Arg_0,Arg_1,no_risk,no_risk,_,aft,moderate):-tcpa(Arg_0,Arg_1,medium).
% ----------------------------------------------------------------------------------------------------
% ----------------------------------------------------------------------------------------------------
arc_overtaking(Arg_0,Arg_1):-
    tcpa_closing(Arg_0,Arg_1),
    starboard(Arg_0,Arg_1).
arc_overtaking(Arg_0,Arg_1):-
    tcpa(Arg_0,Arg_1,medium),
    close_quarters(Arg_0,Arg_1).
arc_overtaking(Arg_0,Arg_1):-
    tcpa(Arg_0,Arg_1,medium),
    close_quarters(Arg_0,Arg_1).
waypoint(Arg_0,Arg_1,no_risk,no_risk,port,Arg_2,small):-
    encounter_and_duty(Arg_0,Arg_1,rule14_head_on,rule16_giveway),
    tcpa_closing(Arg_0,Arg_1).
waypoint(Arg_0,Arg_1,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    moderate(Arg_4),
    encounter_and_duty(Arg_0,Arg_1,rule13_overtaking,rule16_giveway),
    tcpa_closing(Arg_0,Arg_1).
waypoint(Arg_0,Arg_1,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    moderate(Arg_4),
    encounter_and_duty(Arg_0,Arg_1,rule13_overtaking,rule16_giveway),
    close_quarters(Arg_0,Arg_1).
waypoint(Arg_0,Arg_1,no_risk,no_risk,Arg_2,Arg_3,Arg_4):-
    large(Arg_4),
    encounter_and_duty(Arg_0,Arg_1,rule15_crossing,rule17_standon),
    close_quarters_developing(Arg_0,Arg_1).
% ----------------------------------------------------------------------------------------------------