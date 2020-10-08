from typing import Any, Dict

from ...models.models import Motion
from ...shared.exceptions import ActionException
from ...shared.patterns import Collection, FullQualifiedId
from ..default_schema import DefaultSchema
from ..generics import UpdateAction
from ..register import register_action


@register_action("motion.set_recommendation")
class MotionSetRecommendationAction(UpdateAction):
    """
    Set a recommendation in a motion.
    """

    model = Motion()
    schema = DefaultSchema(Motion()).get_update_schema(
        properties=["recommendation_id"], required_properties=["recommendation_id"]
    )

    def update_instance(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check recommendation workflow_id and recommendation_label.
        """
        motion = self.database.get(
            FullQualifiedId(Collection("motion"), instance["id"]), ["workflow_id"]
        )
        state = self.database.get(
            FullQualifiedId(Collection("motion_state"), instance["recommendation_id"]),
            ["workflow_id", "recommendation_label"],
        )
        if state.get("workflow_id") != motion.get("workflow_id"):
            raise ActionException(
                "Cannot set recommendation. State is from a different workflow as motion."
            )
        if state.get("recommendation_label") is None:
            raise ActionException(
                "Recommendation_label of a recommendation must be set."
            )
        return instance
