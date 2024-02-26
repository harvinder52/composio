import json
from typing import Dict, Any, List, Union, Type
import logging
import requests
from pydantic import BaseModel, create_model, Field

from llama_index.core.tools.tool_spec.base import BaseToolSpec

logger = logging.getLogger(__name__)

def map_composio_type_to_python(type_spec) -> Type[BaseModel]:
    print("type_spec:", type_spec)
    if isinstance(type_spec, dict):
        type_str = type_spec.get('type')
        if type_str == 'string':
            return str
        elif type_str == 'integer':
            return int
        elif type_str == 'number':
            return float
        elif type_str == 'boolean':
            return bool
        elif type_str == 'object':
            properties = type_spec.get('properties', {})
            required = type_spec.get('required', [])
            fields = {prop: (map_composio_type_to_python(prop_spec), Field(...)) for prop, prop_spec in properties.items() if prop in required}
            fields.update({prop: (map_composio_type_to_python(prop_spec), Field(None)) for prop, prop_spec in properties.items() if prop not in required})
            model_name = f"DynamicModel_{hash(frozenset(fields.items()))}"
            return create_model(model_name, **fields)
        elif type_str == 'array':
            items_spec = type_spec.get('items', {})
            return List[map_composio_type_to_python(items_spec)] if items_spec else List[Any]
        # Add more mappings as necessary
    # Fallback or default type
    return Any  # Using Any for unspecified or complex types

class ComposioToolSpec(BaseToolSpec):
    """Generic tool spec based on composio_tool.json schema."""

    def __init__(self, tool_schema: str, composio_token: str, user_id: str) -> None:
        """Initialize with composio tool schema."""
        self.tool_schema = json.loads(tool_schema)
        self.spec_functions = self._generate_spec_functions()

    def _generate_spec_functions(self) -> List[str]:
        """Generate spec functions based on the tools actions."""
        spec_functions = []
        for tool in self.tool_schema.get("tools", []):
            for action in tool.get("Actions", []):
                function_name = tool["Name"] + "_" + action["Id"]
                spec_functions.append(function_name)
                input_params = action["Signature"]["Input"]["properties"]
                setattr(self, function_name, self._create_function(action["Id"], action["Description"], input_params, action["Signature"]["Input"].get("required", [])))
        return spec_functions

    def _create_function(self, action_id: str, description: str, input_params: Dict[str, Any], required_params: List[str] = []):
        """Create a function for the given action with typed arguments."""

        # Function template that uses **kwargs to accept any arguments and performs an actual API call.
        def template_function(**kwargs) -> Dict[str, Any]:
            missing_params = [param for param in input_params if param not in kwargs and param in required_params]
            if missing_params:
                return {"error": f"Missing required params: {missing_params}"}
            params = {param: kwargs[param] for param in input_params if param in kwargs}
            logger.info(f"Executing action {action_id} with {params}")
            
            request_body = json.dumps(params)
            response = requests.post(f"http://api.example.com/{action_id}", data=request_body, headers={'Content-Type': 'application/json'})
            return response.json()

        
        parameters = []
        for name in input_params:
            python_type = map_composio_type_to_python(input_params[name])
            field_value = Field(... if name in required_params else None)
            parameters.append((name, (python_type, field_value)))
            if name == "grouping":
                print(f"Parameter added: {name}, Type: {python_type}, Field Value: {field_value}")
        dynamic_model = create_model(f"{action_id}_ParamsModel", **dict(parameters), __base__=BaseModel)
        
        def wrapper_function(*args, **kwargs) -> Dict[str, Any]:
            model_instance = dynamic_model(**kwargs)
            return template_function(**model_instance.dict())

        wrapper_function.__signature__ = dynamic_model.__signature__
        wrapper_function.__doc__ = description
        wrapper_function.__name__ = action_id

        return wrapper_function

