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
:- dynamic greater_than/2.
:- dynamic greater_or_equal/2.
:- dynamic less_and_adjacent/2. 

%:- ['BK.pl'].