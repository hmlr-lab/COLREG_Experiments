
body_pred(sector,3).
body_pred(range,3).
body_pred(dcpa,3).
body_pred(tcpa,3).
body_pred(arc_overtaking,2).


body_pred(port_forward,2).
body_pred(port_aft,2).
body_pred(starboard_forward,2).
body_pred(starboard_aft,2).
body_pred(port,2).
body_pred(starboard,2).
body_pred(forward,2).
body_pred(aft,2).


body_pred(less_and_adjacent,2).
body_pred(less_than,2).
body_pred(greater_than,2).
body_pred(less_or_equal,2).
body_pred(greater_or_equal,2).


body_pred(range_gt,3).
body_pred(range_ge,3).
body_pred(range_lt,3).
body_pred(range_le,3).


body_pred(dcpa_gt,3).
body_pred(dcpa_ge,3).
body_pred(dcpa_lt,3).
body_pred(dcpa_le,3).


body_pred(tcpa_gt,3).
body_pred(tcpa_ge,3).
body_pred(tcpa_lt,3).
body_pred(tcpa_le,3).

body_pred(dcpa_unacceptable,2).
body_pred(dcpa_acceptable,2).
body_pred(tcpa_closing,2).
body_pred(actionable_range,2).
body_pred(ample_time,2).

body_pred(collision_risk,2).
body_pred(close_quarters_developing,2).
body_pred(close_quarters,2).
body_pred(encounter,3).
body_pred(mutual_ahead,2).
body_pred(encounter_and_conduct,4).
body_pred(duty,3).
body_pred(rule2_extremis,2).



type(sector,(vessel,vessel,sector_value)).
type(range,(vessel,vessel,range_value)).
type(dcpa,(vessel,vessel,dcpa_value)).
type(tcpa,(vessel,vessel,tcpa_value)).
type(arc_overtaking,(vessel,vessel)).

type(port_forward,(vessel,vessel)).
type(port_aft,(vessel,vessel)).
type(starboard_forward,(vessel,vessel)).
type(starboard_aft,(vessel,vessel)).
type(port,(vessel,vessel)).
type(starboard,(vessel,vessel)).
type(forward,(vessel,vessel)).
type(aft,(vessel,vessel)).

type(sector,(vessel,vessel,sector_value)).
type(range,(vessel,vessel,order_value)).
type(dcpa,(vessel,vessel,order_value)).
type(tcpa,(vessel,vessel,order_value)).

type(less_and_adjacent,(order_value,order_value)).
type(less_than,(order_value,order_value)).
type(greater_than,(order_value,order_value)).
type(less_or_equal,(order_value,order_value)).
type(greater_or_equal,(order_value,order_value)).

type(range_gt,(vessel,vessel,order_value)).
type(range_ge,(vessel,vessel,order_value)).
type(range_lt,(vessel,vessel,order_value)).
type(range_le,(vessel,vessel,order_value)).

type(dcpa_gt,(vessel,vessel,order_value)).
type(dcpa_ge,(vessel,vessel,order_value)).
type(dcpa_lt,(vessel,vessel,order_value)).
type(dcpa_le,(vessel,vessel,order_value)).

type(tcpa_gt,(vessel,vessel,order_value)).
type(tcpa_ge,(vessel,vessel,order_value)).
type(tcpa_lt,(vessel,vessel,order_value)).
type(tcpa_le,(vessel,vessel,order_value)).

type(dcpa_unacceptable,(vessel,vessel)).
type(dcpa_acceptable,(vessel,vessel)).
type(tcpa_closing,(vessel,vessel)).
type(actionable_range,(vessel,vessel)).
type(ample_time,(vessel,vessel)).

type(collision_risk,(vessel,vessel)).
type(close_quarters_developing,(vessel,vessel)).
type(close_quarters,(vessel,vessel)).
type(encounter,(vessel,vessel,encounter_rule)).
type(mutual_ahead,(vessel,vessel)).
type(encounter_and_conduct,(vessel,vessel,encounter_rule,conduct_rule)).
type(duty,(vessel,vessel,duty_rule)).
type(rule2_extremis,(vessel,vessel)).


magic_value(duty_rule).