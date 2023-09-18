# PromptWiz Client

A client to interact with the <a href="https://promptwiz.co.uk/">PromptWiz</a> API.

The PromptWiz API provides a way to execute prompts defined in the PromptWiz app. The API will build the model input based on your inputs and the prompt defined in the PromptWiz app, then return the results from the model service (e.g. OpenAI) as well as store them in PromptWiz for the purpose of analysis via the PromptWiz app.


## Pre-requisites

<ul>
<li>You must create a prompt, and prompt version (and save it)</li>
<li>A prompt version must be set as ‘active’ in the prompt page</li>
<li>You must have a model service API key (e.g. OpenAI) set under <a href="https://promptwiz.co.uk/api_keys/">API Keys page</a>, or alternatively you can populate the model service API key in each query. Passing the model API key is not a preffered method as it requires updating the value if the model service used is changed in a later version of the prompt</li>
</ul>


## Example Usage

```
import promptwizclient as pwc

pwc.Client.api_key = "<PROMPT_WIZ_API_KEY>"

query_set = [
    pwc.Query(prompt_id=7, variables=dict(EXAMPLE_VARIABLE_1="VARIABLE 1 Value 1", EXAMPLE_VARIABLE_2="VARIABLE 2 Value 1")),
    pwc.Query(prompt_id=7, variables=dict(EXAMPLE_VARIABLE_1="VARIABLE 1 Value 2", EXAMPLE_VARIABLE_2="VARIABLE 2 Value 2")),
]
results, errors, status_code = pwc.Client(query_set=query_set)
```

## [POST] Request Body (JSON)

The client provides an interface to build and make requests following the API request schema below.

### Request Fields

| Field                      	| Required 	| Description  |
|----------------------------	|----------	|------------  |
| apiKey<br>_String_         	| Yes      	| PromptWiz API Key available under <a href="https://promptwiz.co.uk/api_keys/">API Keys page</a> |
| querySet<br>_Array_        	| Yes      	| A list of queries, each having the fields listed in Query Fields below |
| acceptPartial<br>_Boolean_ 	| No       	| Indicates whether partially successful queries can be returned. When set to false the response will fail if ANY query for querySet fails.<br><br>**If not provided, this field is defaulted to False.** |

### Query Fields

| Field                           	    | Required 	| Description  |
|--------------------------------------	|----------	|------------  |
| promptId<br>_Integer_           	    | Yes      	| The ID of the prompt, available on the PromptWiz web application |
| variables<br>_String to String JSON_ 	| Yes/No   	| An JSON of key-value pairs.<br><br>The keys are the prompt variables and the values are their assigned values.<br><br>A value must be assigned to every prompt variable. <br><br>**This field can be omitted only if the prompt has no variables.** |
| linkId<br>_Integer or String_   	    | No       	| An ID used to link a result in the response to a query in the request. This simplifies matching request on your backend if you’re making more than 1 request at a time.<br><br>If this field is omitted, PromptWiz will assign each query its index as the link ID.<br><br>If this field is provided in any query in the query set, it must be provided on all.<br><br>If this field is provided in the queries, it must be unique across the queries. |
| modelApiKey<br>_String_         	    | No       	| An API key for the model service (e.g. OpenAI) to be queried. This allows for an override to the organisation’s API key saved under the <a href="https://promptwiz.co.uk/api_keys/">API Keys page</a>. Please keep in mind if this parameter is used, the value may have to be updated if the model service is changed in a newer prompt version. |
| resultsSize<br>_Integer_              | No      	| The number of results to generate |