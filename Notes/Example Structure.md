# ColReg Experiments Example Folder
- Examples
	- take_action
		- pos (facts)
		- neg (facts)
	- waypoint
		- situation1 
			- facts
			- pos
				- 1
				- 2
				- 3
			- neg
				- 1
				- 2


- Examples
	- situations
		- 1
			- waypoint
				- pos
				- neg
		- 2
		- 3
	- take_action_pos (csv list of situation IDs)
	- take_action_neg ""
# Situation - Way Points 


## Situation Facts
```prolog
sector(agent_0,cruiseliner1,ahead).
sector(cruiseliner1,agent_0,astern).
range(agent_0,cruiseliner1,near).
dcpa(agent_0,cruiseliner1,critical).
tcpa(agent_0,cruiseliner1,medium).
arc_overtaking(agent_0,cruiseliner1).
```
## Example Way point
`````prolog
turn(agent1,moderate)
avoid(agent_1, cl1, no_risk)
resume(agent_1, cl1, no_risk)
side(agent_1, cl1, starboard)
`````


# Situation - Take Action 

Pos:
- situation 1
- situation 2
Neg:
- situation 3
- situation 4

```prolog
take_action(X):- pred_1(X), pred_2(X).
pred_1(X):- %some conditions
pred_2(X):- %some conditions
```