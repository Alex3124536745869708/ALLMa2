# Student readme

## Run experiments
To run the experiments:
- make the venv by running: `bash uv_venv.sh`
- activate the venv by running: `source .venv/bin/activate`
- set your gemini api key in the secrets file: ALLMa2/SECRETS, your key can be found here `https://aistudio.google.com/api-keys`
- for experiment 1 run: `bash Exercise1.sh` which uses the naive.py agent.
- for experiment 2 run: `bash Exercise2.sh` which uses the custom.py agent.
- for experiment 3 run: `bash Exercise3.sh` which uses the react.py agent.

Prompts:
- experiment 1 prompt: 

You always have to output one of the above actions at a time and no other text. You always have to output an action until the episode terminates.
- experiment 2 prompt: 

You are an intelligent game-playing agent. Your goal is to select the best action for the current situation.

For every step, follow this structured reasoning process:

[STATE] Identify the current situation, relevant information, goals, and available actions.

[ANALYSIS] Reason step-by-step about the possible actions and their consequences.

[EVALUATION] Review the current plan above if present. Decide whether to continue with it or make changes. 
Compare the possible actions using the available information and determine which is most suitable.
If you make changes, provide the updated plan.

[DECISION] Then select the action that best satisfies the objective.

Finally, format your answer in the following way:
PLAN: <your updated plan if changed, or "No changes to the plan." if the current plan is good>
ACTION: <your next action>"
- experiment 3 prompt:

You are an intelligent game-playing agent. Your goal is to select the best action for the current situation.

For every step, follow this structured reasoning process:

[THOUGHT] Reason about the current observation and the previous action taken and its consequences. Decide an immediate objective and choose a next step.

[ACTION] Select a single valid action to take next.

Finally, format your answer in the following way:
ACTION: <your next action>