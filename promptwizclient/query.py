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
            to allow linking queries in a query set to results in a result set
    """
    prompt_id: int
    args: Optional[Dict[str, str]] = None
    link_id: Optional[Union[int, str]] = None

    def as_dict(self):
        query = dict(promptId=self.prompt_id)
        if self.args:
            query["args"] = self.args
        if self.link_id:
            query["linkId"] = self.link_id
        return query