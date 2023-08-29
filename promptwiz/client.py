import json
import requests
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

@dataclass
class PromptWizQuery:
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


class PromptWizClient:

    PROMPT_WIZ_URL = "https://promptwiz.co.uk"
    PROMPT_WIZ_API_URL = f"{PROMPT_WIZ_URL}/api/v0.1"
    PROMPT_WIZ_EVALUATE_API_URL = f"{PROMPT_WIZ_API_URL}/evaluate/"

    def __init__(self, api_key: Optional[str] = None):
        self._api_key = api_key
    
    @property
    def api_key(self) -> str:
        return self._api_key
    
    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self._api_key = api_key

    def __call__(
        self, 
        query_set: List[PromptWizQuery], 
        accept_partial: Optional[bool] = None, 
        api_key: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[List[Dict[str, str]]], int]:
        """
        Evaluates a given request
        
        Parameters
        ----------
            query_set : List[:class:`PromptWizQuery`]\n
                A list of Prompt Wiz queries to be evaluated, see :class:`PromptWizQuery`\n
            accept_partial : Optional[:class:`bool`]\n
                A boolean indicating whether partial result sets are accepted.\n
                A partial result set is one that does not contain a result for\n
                for every query in the query set\n
            api_key : Optional[:class:`str`]\n
                The Prompt Wiz API key to use for the query set. If this argument is not\n
                provided, please set an API key to be used for all requests:\n
                `promptwizclient.api_key = ...`
        
        Returns
        -------
            results_set : List[Dict[:class:`str`, Any]]\n
                The result set\n
            erros : List[Dict[:class:`str`, :class:`str`]]\n
                A list of Prompt Wiz errors, or `None` if there are no errors\n
            status_code : :class:`int`\n
                A HTTP status code
        """
        request_payload = dict(
            apiKey=api_key or self._api_key or "",
            querySet=json.dumps([query.as_dict() for query in query_set]),
        )
        if accept_partial is not None:
            request_payload["acceptPartial"] = accept_partial
        response = requests.post(self.PROMPT_WIZ_EVALUATE_API_URL, data=request_payload)
        try:
            response_payload = json.loads(response.text)
            return response_payload.get("resultSet", []), response_payload.get("errors"), response.status_code
        except Exception as err:
            return (
                [], 
                [
                    dict(
                        code="UNKOWN_RESPONSE", 
                        description=f"Could not parse the PromptWiz response: {err}\n{response.text}"
                    ),
                ], 
                response.status_code,
            )