from test_helpers.tools import addition

from inspect_ai.tool import Content, ToolCall, ToolCallView, ToolDef, tool_with
from inspect_ai.tool._tool_call import ToolCallModelInputHints

NAME = "my_addition"
DESCRIPTION = "my description"
X_DESCRIPTION = "my x description"
Y_DESCRIPTION = "my y description"


def test_tool_with():
    tool = tool_with(
        addition(),
        name=NAME,
        description=DESCRIPTION,
        parameters={"x": X_DESCRIPTION, "y": Y_DESCRIPTION},
    )

    tdef = ToolDef(tool)

    assert tdef.name == NAME
    assert tdef.description == DESCRIPTION
    assert tdef.parameters.properties["x"].description == X_DESCRIPTION
    assert tdef.parameters.properties["y"].description == Y_DESCRIPTION


def _viewer(call: ToolCall) -> ToolCallView:
    return ToolCallView()


def _model_input(
    message_index: int,
    message_total: int,
    content: str | list[Content],
    hints: ToolCallModelInputHints,
) -> str | list[Content]:
    return content


def test_tool_with_parallel_and_viewer():
    tool = tool_with(addition(), parallel=True, viewer=_viewer)

    tdef = ToolDef(tool)

    assert tdef.parallel is True
    assert tdef.viewer is _viewer


def test_tool_with_parallel_and_model_input():
    tool = tool_with(addition(), parallel=True, model_input=_model_input)

    tdef = ToolDef(tool)

    assert tdef.parallel is True
    assert tdef.model_input is _model_input


def test_tool_with_viewer_and_model_input():
    tool = tool_with(addition(), viewer=_viewer, model_input=_model_input)

    tdef = ToolDef(tool)

    assert tdef.viewer is _viewer
    assert tdef.model_input is _model_input


def test_tool_with_parallel_viewer_and_model_input():
    tool = tool_with(
        addition(), parallel=True, viewer=_viewer, model_input=_model_input
    )

    tdef = ToolDef(tool)

    assert tdef.parallel is True
    assert tdef.viewer is _viewer
    assert tdef.model_input is _model_input


def test_tool_with_validation():
    try:
        tool_with(
            addition(),
            parameters={"p": X_DESCRIPTION, "q": Y_DESCRIPTION},
        )
        assert False
    except Exception:
        pass
