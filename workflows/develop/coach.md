# Develop: AI-in-the-loop coaching

Use this workflow for a problem, decision, conflict, or leadership challenge.

## Stages

1. **Frame**
   - situation
   - decision
   - stakeholders
   - constraints
   - known evidence
   - uncertainty
   - desired outcome

2. **Initial recommendation**
   - recommended action
   - alternatives
   - assumptions
   - confidence

3. **Critical review**
   - compelling/useful
   - generic or weak
   - unsupported assumptions
   - missing context
   - risks and second-order effects

4. **Refinement**
   - improve the question
   - generate a more situation-specific response

5. **Human judgment**
   - ask what the user knows that the model does not
   - invite disagreement
   - identify the better answer or reversible experiment

6. **Record**
   - final decision or experiment
   - rationale
   - dissenting considerations
   - confidence
   - next action
   - review date
   - prompt lesson

Write structured JSON and call:

```bash
python -m pco coach add --input <json-file>
```

Do not record a final decision until the user has supplied the human-judgment layer.

