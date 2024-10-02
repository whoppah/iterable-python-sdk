from .base import BaseResource
from ..exceptions import ValidationException


class WorkflowResource(BaseResource):
    def trigger(self, user_id: str, workflow_id: int, data_fields: dict = None):
        """
        Trigger a workflow for a user in Iterable.

        Args:
            user_id (str): The ID of the user to trigger the workflow for.
            workflow_id (int): The ID of the workflow to trigger.
            data_fields (dict, optional): Additional data fields for the workflow.

        Returns:
            dict: The response from the Iterable API.

        Raises:
            ValidationException: If the input parameters are invalid.
            IterableAPIException: If there's an error with the Iterable API.
        """
        if not isinstance(user_id, str) or not user_id:
            raise ValidationException("user_id must be a non-empty string")

        if not isinstance(workflow_id, int) or workflow_id <= 0:
            raise ValidationException("workflow_id must be a positive integer")

        if data_fields is not None and not isinstance(data_fields, dict):
            raise ValidationException("data_fields must be a dictionary or None")

        payload = {
            "userId": user_id,
            "workflowId": workflow_id,
        }

        if data_fields:
            payload["dataFields"] = data_fields

        return self.client.post("workflows/triggerWorkflow", data=payload)
