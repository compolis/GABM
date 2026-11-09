"""Independent tests for the optional two-stage survey executor."""

from dataclasses import FrozenInstanceError
from unittest.mock import Mock, call

import pytest

from gabm.abm.survey import TwoStageSurveyResult, execute_two_stage_question


def test_neutral_question_preserves_prompts_and_intermediate_recording_order():
    events = []

    def send(system, user, stage):
        events.append((stage, system, user))
        return "I prefer quiet spaces." if stage == "reasoning" else "B"

    def record(reasoning):
        events.append(("record", reasoning))

    def build(system, reasoning):
        events.append(("build", system, reasoning))
        return f"{system}\nNotes: {reasoning}"

    result = execute_two_stage_question(
        system_prompt="You are a library visitor.",
        reasoning_prompt="What matters when choosing a reading room?",
        answer_prompt="Choose A: lively or B: quiet.",
        send=send,
        build_answer_system=build,
        on_reasoning=record,
    )

    assert result == TwoStageSurveyResult("I prefer quiet spaces.", "B")
    assert events == [
        ("reasoning", "You are a library visitor.",
         "What matters when choosing a reading room?"),
        ("record", "I prefer quiet spaces."),
        ("build", "You are a library visitor.", "I prefer quiet spaces."),
        ("answer", "You are a library visitor.\nNotes: I prefer quiet spaces.",
         "Choose A: lively or B: quiet."),
    ]
    with pytest.raises(FrozenInstanceError):
        result.answer = "A"


@pytest.mark.parametrize("failure_stage", ["reasoning", "record", "build", "answer"])
def test_errors_propagate_without_subsequent_work(failure_stage):
    error = RuntimeError(f"failure at {failure_stage}")
    events = Mock()
    events.send.side_effect = (
        error if failure_stage == "reasoning"
        else ["notes", error if failure_stage == "answer" else "raw answer"]
    )
    events.record.side_effect = error if failure_stage == "record" else None
    events.build.side_effect = error if failure_stage == "build" else None
    events.build.return_value = "answer context"

    with pytest.raises(RuntimeError) as raised:
        execute_two_stage_question(
            system_prompt="context", reasoning_prompt="why?", answer_prompt="choice?",
            send=events.send, build_answer_system=events.build,
            on_reasoning=events.record,
        )

    assert raised.value is error
    expected = [
        call.send("context", "why?", "reasoning"),
        call.record("notes"),
        call.build("context", "notes"),
        call.send("answer context", "choice?", "answer"),
    ]
    assert events.mock_calls == expected[:[
        "reasoning", "record", "build", "answer",
    ].index(failure_stage) + 1]


def test_raw_responses_are_not_parsed_trimmed_or_replaced():
    send = Mock(side_effect=["  notes\n", "not a valid choice\n"])

    result = execute_two_stage_question(
        system_prompt="", reasoning_prompt="", answer_prompt="",
        send=send, build_answer_system=lambda system, reasoning: reasoning,
        on_reasoning=lambda reasoning: None,
    )

    assert result == TwoStageSurveyResult("  notes\n", "not a valid choice\n")
    assert send.call_args_list == [
        call("", "", "reasoning"),
        call("  notes\n", "", "answer"),
    ]
