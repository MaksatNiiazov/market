from esdbclient import NewEvent

from tanda_backend.common.eventstore import serialize, append_to_stream
from tanda_backend.products.models import OptionType, OptionValue
from tanda_backend.products.models.category import Category, CategoryOptionRequirement


def send_option_type_created_event(option_type: OptionType) -> None:
    data = {
        "public_id": str(option_type.public_id),
        "name": option_type.name,
        "code": option_type.code,
    }

    event = NewEvent(
        type="OptionTypeCreated",
        data=serialize(data),
    )
    stream_name = "option_types"
    append_to_stream(event, stream_name)


def send_option_type_updated_event(option_type: OptionType) -> None:
    data = {
        "public_id": str(option_type.public_id),
        "name": option_type.name,
        "code": option_type.code,
    }

    event = NewEvent(
        type="OptionTypeUpdated",
        data=serialize(data),
    )
    stream_name = "option_types"
    append_to_stream(event, stream_name)


def send_option_type_deleted_event(option_type_id: str) -> None:
    data = {
        "public_id": option_type_id,
    }

    event = NewEvent(
        type="OptionTypeDeleted",
        data=serialize(data),
    )
    stream_name = "option_types"
    append_to_stream(event, stream_name)


def send_option_value_created_event(option_value: OptionValue) -> None:
    data = {
        "public_id": str(option_value.public_id),
        "value": option_value.value,
        "meta_data": option_value.meta_data or {},
        "option_type": {
            "public_id": str(option_value.option_type.public_id),
            "name": option_value.option_type.name,
            "code": option_value.option_type.code,
        }
    }

    event = NewEvent(
        type="OptionValueCreated",
        data=serialize(data),
    )
    stream_name = "option_values"
    append_to_stream(event, stream_name)


def send_option_value_updated_event(option_value: OptionValue) -> None:
    data = {
        "public_id": str(option_value.public_id),
        "value": option_value.value,
        "option_type": {
            "public_id": str(option_value.option_type.public_id),
            "name": option_value.option_type.name,
            "code": option_value.option_type.code,
        },
        "meta_data": option_value.meta_data or {},
    }

    event = NewEvent(
        type="OptionValueUpdated",
        data=serialize(data),
    )
    stream_name = "option_values"
    append_to_stream(event, stream_name)


def send_option_value_deleted_event(option_value_id: str) -> None:
    data = {
        "public_id": option_value_id,
    }

    event = NewEvent(
        type="OptionValueDeleted",
        data=serialize(data),
    )
    stream_name = "option_values"
    append_to_stream(event, stream_name)


def send_category_created_event(category: Category) -> None:
    data = {
        "public_id": str(category.public_id),
        "name": category.name,
        "lft": category.lft,
        "rght": category.rght,
        "level": category.level,
        "tree_id": category.tree_id,
    }

    if category.parent:
        data["parent"] = {
            "public_id": str(category.parent.public_id),
            "name": category.parent.name,
        }

    event = NewEvent(
        type="CategoryCreated",
        data=serialize(data),
    )
    stream_name = "categories"
    append_to_stream(event, stream_name)


def send_category_updated_event(category: Category) -> None:
    data = {
        "public_id": str(category.public_id),
        "name": category.name,
        "lft": category.lft,
        "rght": category.rght,
        "level": category.level,
        "tree_id": category.tree_id,
    }

    if category.parent:
        data["parent"] = {
            "public_id": str(category.parent.public_id),
            "name": category.parent.name,
        }

    event = NewEvent(
        type="CategoryUpdated",
        data=serialize(data),
    )
    stream_name = "categories"
    append_to_stream(event, stream_name)


def send_category_deleted_event(category_id: str) -> None:
    data = {
        "public_id": category_id,
    }

    event = NewEvent(
        type="CategoryDeleted",
        data=serialize(data),
    )
    stream_name = "categories"
    append_to_stream(event, stream_name)


def send_category_option_requirement_created_event(requirement: CategoryOptionRequirement) -> None:
    data = {
        "public_id": str(requirement.public_id),
        "is_main": requirement.is_main,
        "is_required": requirement.is_required,
        "sort_order": requirement.sort_order,
        "category": {
            "public_id": str(requirement.category.public_id),
            "name": requirement.category.name,
        },
        "option_type": {
            "public_id": str(requirement.option_type.public_id),
            "name": requirement.option_type.name,
            "code": requirement.option_type.code,
        },
    }

    event = NewEvent(
        type="CategoryOptionRequirementCreated",
        data=serialize(data),
    )
    stream_name = "category_option_requirements"
    append_to_stream(event, stream_name)


def send_category_option_requirement_updated_event(requirement: CategoryOptionRequirement) -> None:
    data = {
        "public_id": str(requirement.public_id),
        "is_main": requirement.is_main,
        "is_required": requirement.is_required,
        "sort_order": requirement.sort_order,
        "category": {
            "public_id": str(requirement.category.public_id),
            "name": requirement.category.name,
        },
        "option_type": {
            "public_id": str(requirement.option_type.public_id),
            "name": requirement.option_type.name,
            "code": requirement.option_type.code,
        }
    }

    event = NewEvent(
        type="CategoryOptionRequirementUpdated",
        data=serialize(data),
    )
    stream_name = "category_option_requirements"
    append_to_stream(event, stream_name)


def send_category_option_requirement_deleted_event(requirement_id: str) -> None:
    data = {
        "public_id": requirement_id,
    }

    event = NewEvent(
        type="CategoryOptionRequirementDeleted",
        data=serialize(data),
    )
    stream_name = "category_option_requirements"
    append_to_stream(event, stream_name)
