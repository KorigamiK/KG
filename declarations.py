import textwrap
import google.ai.generativelanguage as glm

entity = glm.Schema(
    type=glm.Type.OBJECT,
    properties={
        "name": glm.Schema(type=glm.Type.STRING, description="Name of the entity"),
        "description": glm.Schema(
            type=glm.Type.STRING, description="Description of the entity"
        ),
        "type": glm.Schema(type=glm.Type.STRING),
    },
    required=["name", "description", "type"],
)

"""Then define entities as an `ARRAY` of `entity` objects:"""

entities = glm.Schema(type=glm.Type.ARRAY, items=entity)

"""Define the relationship schema:"""
relationship = glm.Schema(
    type=glm.Type.OBJECT,
    properties={
        "from_entity_name": glm.Schema(type=glm.Type.STRING),
        "to_entity_name": glm.Schema(type=glm.Type.STRING),
        "relationship": glm.Schema(
            type=glm.Type.STRING,
            description="Type of relationship between the entities",
        ),
    },
    required=["from_entity_name", "to_entity_name"],
)

relationships = glm.Schema(type=glm.Type.ARRAY, items=relationship)

"""Now build the `FunctionDeclaration`:"""

add_to_database = glm.FunctionDeclaration(
    name="add_to_database",
    description=textwrap.dedent(
        """\
        Adds entities to the database.
        """
    ),
    parameters=glm.Schema(
        type=glm.Type.OBJECT,
        properties={
            "entities": entities,
            "relationships": relationships,
        },
    ),
)