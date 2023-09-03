from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass
class Query:
    """
    A PromptWiz Query
        
    Parameters
    ----------
        prompt_id : :class:`int`\n
            The Prompt Wiz prompt ID\n
        args : Optional[Dict[:class:`str`, :class:`str`]]\n
            The arguments for the prompt parameters, or `None` if the prompt does\n
            not have any parameters\n
        link_id : Optional[:class:`int`]\n
            A unique ID for the query. This ID will be echoed back by Prompt Wiz in results\n
            to allow linking queries in a query set to results in a result set\n
        model_api_key : Optional[:class:`str`]\n
            An optional model service (e.g. OpenAI) API key to use when requesting evaluation\n
            for this particular query. If this field is provided, the API key must be updated\n
            to the relevant model service API key if the model is changed in a new prompt version\n
            If this field is not provided, PromptWiz will use the relevant model service API key\n
            saved in your organisations API keys
    """
    prompt_id: int
    args: Optional[Dict[str, str]] = None
    link_id: Optional[Union[int, str]] = None
    model_api_key: Optional[str] = None

    def as_dict(self):
        query = dict(promptId=self.prompt_id)
        if self.args:
            query["args"] = self.args
        if self.link_id:
            query["linkId"] = self.link_id
        if self.model_api_key:
            query["modelApiKey"] = self.model_api_key
        return query