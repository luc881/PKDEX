from ..models.types.orm import Types

def serialize_types(type: Types):
    """Helper function to serialize a Todos object into a dictionary."""
    return {
        "id": type.id,
        "name": type.name,
    }