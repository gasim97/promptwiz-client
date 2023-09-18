from __future__ import annotations

import json
import requests
from typing import Any, Dict, List, Optional, Tuple

from promptwizclient.query import Query


_SUPPORTED_API_VERSIONS = ["0.1"]

DEFAULT_API_VERSION = "0.1"
DEFAULT_PROMPT_WIZ_URL = "https://promptwiz.co.uk"


class _PromptWizClient:
    def __init__(self):
        self._api_key = None
        self._api_version = DEFAULT_API_VERSION
        self._prompt_wiz_url = DEFAULT_PROMPT_WIZ_URL
    
    @property
    def api_key(self) -> str:
        """The PromptWiz API key used in requests"""
        return self._api_key
    
    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self._api_key = api_key
    
    @property
    def api_version(self) -> str:
        """The PromptWiz API version used in requests"""
        return self._api_version
    
    @api_version.setter
    def api_version(self, api_version: str | float) -> None:
        if isinstance(api_version, float):
            api_version = str(api_version)
        if api_version not in _SUPPORTED_API_VERSIONS:
            raise ValueError(f"Unsupported PromptWiz API version: {api_version}")
        self._api_version = api_version
    
    @property
    def prompt_wiz_url(self) -> str:
        """The PromptWiz URL targeted in requests"""
        return self._prompt_wiz_url
    
    @prompt_wiz_url.setter
    def prompt_wiz_url(self, prompt_wiz_url: str) -> None:
        self._prompt_wiz_url = prompt_wiz_url
    
    @property
    def _prompt_wiz_api_url(self) -> str:
        return f"{self._prompt_wiz_url}/api/v{self.api_version}"
    
    @property
    def _prompt_wiz_evaluate_api_url(self) -> str:
        return f"{self._prompt_wiz_api_url}/evaluate/"

    def __call__(
        self, 
        query_set: List[Query], 
        accept_partial: Optional[bool] = None, 
        api_key: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[List[Dict[str, str]]], int]:
        """
        Evaluates a given request
        
        Parameters
        ----------
            query_set : List[:class:`promptwiz.Query`]\n
                A list of Prompt Wiz queries to be evaluated, see :class:`promptwiz.Query`\n
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
            querySet=[query.as_dict() for query in query_set],
        )
        if accept_partial is not None:
            request_payload["acceptPartial"] = accept_partial
        response = requests.post(self._prompt_wiz_evaluate_api_url, json=request_payload)
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


Client = _PromptWizClient()