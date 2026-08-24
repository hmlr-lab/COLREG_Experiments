## Facts
```prolog
sector(agent_0,cruiseliner1,ahead).
sector(cruiseliner1,agent_0,astern).
range(agent_0,cruiseliner1,near).
dcpa(agent_0,cruiseliner1,critical).
tcpa(agent_0,cruiseliner1,medium).
arc_overtaking(agent_0,cruiseliner1).
```
## Example Literals
`````prolog
take_action(agent_1),
turn(agent1,moderate),
side(agent_1, cl1, starboard),
avoid(agent_1, cl1, no_risk),
resume(agent_1, cl1, no_risk).
`````