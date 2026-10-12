import re

from balrog.agents.base import BaseAgent


class ReactAgent(BaseAgent):
    """An agent that generates actions and plans based on observations with a customizable approach."""

    def __init__(self, client_factory, prompt_builder):
        super().__init__(client_factory, prompt_builder)
        self.client = client_factory()

    def act(self, obs, prev_action=None):
        """Generate the next action and update the plan based on the current observation.

        Args:
            obs (dict): The current observation in the environment.
            prev_action (str, optional): The previous action taken.

        Returns:
            LLMResponse: The response containing the updated plan and selected action.
        """
        if prev_action:
            self.prompt_builder.update_action(prev_action)
        self.prompt_builder.update_observation(obs)

        planning_instructions = """
You are an intelligent game-playing agent. Your goal is to select the best action for the current situation.

For every step, follow this structured reasoning process:

[THOUGHT] Reason about the current observation and the previous action taken and its consequences. Decide an immediate objective and choose a next step.

[ACTION] Select a single valid action to take next.

Finally, format your answer in the following way:
ACTION: <your next action>
        """.strip()

        messages = self.prompt_builder.get_prompt()
        if messages and messages[-1].role == "user":
            messages[-1].content += "\n\n" + planning_instructions

        with open("content.txt", "a") as f: #hier weghalen remove
            f.write(f"Content written:\n{messages}========================\n")

        response = self.client.generate(messages)

        # Extract the plan and action from the LLM's response
        action = self._extract_action(response.completion)
        with open("content.txt", "a") as f: #hier weghalen remove
            f.write(f"Response:\n{response}========================\n")
            f.write(f"Action extracted:\n{action}========================\n")

        # Save the action in response.completion
        response = response._replace(completion=action)
        return response


    def _extract_action(self, response_text):
        """Extract the plan and action from the LLM's response text.

        Args:
            response_text (str): The response text from the LLM.

        Returns:
            tuple: A tuple containing the extracted plan and action.
        """
        action_match = re.search(r"ACTION:\s*(.*)", response_text, re.IGNORECASE | re.DOTALL)

        action = action_match.group(1).strip() if action_match else None

        return action
