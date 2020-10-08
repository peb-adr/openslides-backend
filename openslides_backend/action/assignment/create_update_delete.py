from ...models.models import Assignment
from ..action_set import ActionSet
from ..agenda_item.agenda_creation import (
    CreateActionWithAgendaItemMixin,
    agenda_creation_properties,
)
from ..agenda_item.create import AgendaItemCreate
from ..create_action_with_dependencies import CreateActionWithDependencies
from ..default_schema import DefaultSchema
from ..generics import DeleteAction, UpdateAction
from ..list_of_speakers.create import ListOfSpeakersCreate
from ..list_of_speakers.list_of_speakers_creation import (
    CreateActionWithListOfSpeakersMixin,
)
from ..register import register_action_set

create_schema = DefaultSchema(Assignment()).get_create_schema(
    required_properties=["title", "meeting_id"],
    optional_properties=[
        "description",
        "open_posts",
        "phase",
        "default_poll_description",
        "number_poll_candidates",
        "attachment_ids",
        "tag_ids",
    ],
)

create_schema["items"]["properties"].update(agenda_creation_properties)


class AssignmentCreate(
    CreateActionWithDependencies,
    CreateActionWithAgendaItemMixin,
    CreateActionWithListOfSpeakersMixin,
):
    model = Assignment()
    schema = create_schema
    dependencies = [AgendaItemCreate, ListOfSpeakersCreate]


@register_action_set("assignment")
class AssignmentActionSet(ActionSet):
    """
    Actions to create, update and delete assignments.
    """

    model = Assignment()
    create_schema = create_schema
    update_schema = DefaultSchema(Assignment()).get_update_schema(
        optional_properties=[
            "title",
            "description",
            "open_posts",
            "phase",
            "default_poll_description",
            "number_poll_candidates",
            "attachment_ids",
            "tag_ids",
        ]
    )
    delete_schema = DefaultSchema(Assignment()).get_delete_schema()
    routes = {
        "create": AssignmentCreate,
        "update": UpdateAction,
        "delete": DeleteAction,
    }
