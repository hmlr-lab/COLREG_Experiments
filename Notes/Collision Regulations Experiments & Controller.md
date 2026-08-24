#### Glossary
- Examples
	- *Scenario*: An instance of a simulator episode example and it's log file
	- *Situation*: A specific moment (clock tic) in a *Scenario*
	- *Literal*: Predicate argument pair passed to ILP for hypothesis learning e.g `take_action(agent_1)` 
- *Learning/Target Predicate*: `take_action/1`, `turn/2`
- *Observation Facts*: List of facts in a situation 
# Controller
## Take Action
Based on current scenario do we need to take action? 
`-? take_action(agent_1)` 
Posed as a purely constant query this will evaluate to either true of false.
Take action could be either:
- *arity-1* `take_action(agent)`
- *arity-2* `take_action(agent, cruiseliner_1)`

*Example/Goal Literal* is arity-1 try to form hypothesis with `take_action/2`   
```prolog
take_action(X):-
	vessel(Y),
	take_action(X,Y).
```
## Compliant Region

### Compliant Region Condition Options
Below is a list of options  for formatting the compliant region conditions list and their pros and cons, for both learning and inference
- **Potentially Positive Conditions**: the conditions list is a set of conditions which may (but do not have to be) true, the compliant region is formed from the Union of these conditions  
	- *Pros*: 
	- Good generalisation, find what situation allows each individual way point condition to be true
	- Natural use of transitive properties in hypothesis
	- Lack of value for a condition clearly implies lack of information and therefore need for human intervention and new examples
	- *Cons*:
	- Negatives will easily over specialise. Just because one aspect of a way point is negative, that does not necessarily make all others negative
	- Output list will be quite large as find_all with transitive properties will propagate list with all constants that may fit
	- Number of examples literals will be larger *(This may not have to be true)*
- **Most Dangerous Compliant Condition**: The condition list contains the least safe compliant conditions, describing the boundary of compliant way points from the positive side. This could be a post processing step on top of `Potentially Positive Conditions` for the controller, which would then not affect learning. This approach may not need the list construction prolog code, instead each condition for each vessel pair could be tested manually e.g `avoid(agent,cruiseliner1,X)` using `X`'s instantiation 
	- *Pros*:
	- Shorter output List
	- Less example literals to learn from
	- *Cons*: 
	- Less natural use of transitive properties
	- Similar problems as above with handling negatives over specialising
	- How to interpret condition with no value? allow all or none
- **Least Dangerous Non-Compliant Condition**: Similarly to `Most Dangerous Compliant Condition` the output describes the boundary, which leads to similar pros and cons.
	- *Pros*:
	- Output follows the model of carving away potential regions for the way point more naturally
	- *Cons* 
	- More example processing before learning
This planning document will continue with the *Potentially Positive Conditions* model


The compliant region will be defined as a list of conditions which are allowed to be true when placing a way point e.g. if a way point would have the condition `side(cruiseliner1,port)` but only `side(cruisliner1,starboard)` is present in the condition list, that is an invalid way point. 
The compliant region list may include both `side(cruiseliner1,port)` and `side(cruisliner1,starboard)` allowing either to be true. 
If neither side was present this would be a fail condition requiring human intervention, which could then be logged and added as an example scenario to prevent future similar failures
### compliant_region query
Query the `compliant_region/2` predicate with the `agent` as the 1st argument and an uninitialised variable `X` as the second argument : `compliant_region(agent,X)`.
The query will return the list of conditions which define the compliant region

`````prolog
-? compliant_region(agent,X)
X = [
	turn(moderate),
	side(cruiseliner1, port), 
	avoid(cruiseliner1, no_risk), 
	resume(cruiseliner2, marginal)
]
`````

### Compliant Region Controller code

To be included with background knowledge and hypothesis when using prolog for inference

`````prolog
compliant_region(X,Conds):- find_all(condition(X,Cond),Cond,Conds)
		
condition(agent1,turn(moderate)):- turn(agent1,moderate).
condition(agent1,side(X,Y)):-      side(agent1,X,Y).
condition(agent1,avoid(X,Y)):-     avoid(agent1,X,Y).
condition(agent1,resume(X,Y)):-    resume(agent1,X,Y).
`````

### Ordering
- 0 take_action
- 1 turn
- 2 side
- 3 avoid
- 4 resume

## Controller Algorithm
```pseudo
\begin{algorithm}
\caption{Controller}
\begin{algorithmic}
\Procedure{ControllerLoop}{$agent$}
	\If{Query(take_action($agent$))}
		\State $conditions \gets$ Query(compliant_region($agent$,$conditions$))
		\State $compliantRegion \gets$ BuildRegion($conditions$)
		\State $bestWaypoint \gets$ FindBestWaypoint($compliantRegion$)
		\State PlaceWaypoint($bestWaypoint$) 
    \EndIf
\EndProcedure
\end{algorithmic}
\end{algorithm}
```

# Examples
Example literals for `take_action/1` should be separate from compliant region in the learning but may come from the same example scenario. Each example scenario can then be classified as positive or negative for take action, and positive or negative for compliant region

|                        | -   | take_action                                          | $\neg$take_action                                    |
| ---------------------- | --- | ---------------------------------------------------- | ---------------------------------------------------- |
| compliant_region       | -   | Positive example scenario <br>of collision avoidance | Valid waypoint, did<br>not need to take action       |
| $\neg$compliant_region | -   | Action was needed <br>but invalid waypoint           | Placed a bad waypoint when<br>no action was required |
## Take Action

Example literals of the take action predicate are the most simple to implement, as it is a simple true false condition based on the background knowledge, with each example scenario having only 1 example literal of the `take_action/1` predicate.

Negative examples of take actions:
- should not be that an action was taken too late, better to act late than never
- No action was needed
- Taking an action too early, but action is needed

## Compliant Region

The example scenarios will be split into separate example literals, 1 for each possible compliance region condition. 1 compiled example literal from a log file e.g. `avoid(agent_1,cl1,short_close)` will be translated into multiple safer example literals through the transitive property for each constant class 

`````prolog
% Minimum turn
turn(agent1,moderate)
% Maximum allowable risk
avoid(agent_1, cl1, short_close)
resume(agent_1, cl1, no_risk)
% Side of agent to put cruiseliner on at CPA
side(agent_1, cl1, port)

avoid(agent_1, cl2, medium_veryclose)
resume(agent_1, cl2, no_risk)
side(agent_1, cl2, starboard)
`````

### Negative Examples
If negative example literals are naively extracted from the example scenarios we will likely over specialise. Some potential solutions are: 
#### 1 Hand Code
One approach is to engineer negative examples by hand, to try and isolate specific aspects of the way point which are incorrect whilst removing the compliant example literals. This presents obvious downsides as each example will take more work to create, and once the system is operational it would be harder for end users to provide new negative examples
#### 2 Multiple Negative Way Points per Situation 
By providing multiple negative way points for an example scenario we can try to isolate which specific conditions are negative for that scenario, perhaps with a simple intersection operation, this may be less precise than hand coding but it becomes much easier to generate good negatives
#### 3 Noise Cancelling
If we leave all condition example literals from the scenarios we could use a system to determine which example literals could be considered noise. This simplest way to achieve this is to attempt learning with overlapping subsets of negatives, some of which may fail to find a hypothesis. This could then be used to remove example literals from the set of negatives if they are considered to be noise and not useful information. The identified problematic literals could be removed through a brute force approach, removing them all and adding 1 back at a time to see if they prevent a hypothesis being learnt. Alternatively after testing the different subsets, a simple score and threshold could be used to remove literals, this would run quicker but might remove too much useful information
#### Combining 2 & 3
Combining approaches 2 and 3 may provide the best balance of effort per example and accuracy. Starting with method 2 we could reduce the amount of starting noise guided partially by a human teacher. Using noise cancelling on this reduced set would then both be more likely to keep important information and run quicker with less example literals to consider


## Positive and Negative Waypoint examples for a situation