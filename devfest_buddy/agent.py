import json
from datetime import datetime
from pathlib import Path

from google.adk.agents import Agent


# Load the sample conference sessions from the JSON file.
DATA_FILE = Path(__file__).parent / "sessions.json"

with DATA_FILE.open("r", encoding="utf-8") as file:
    SESSIONS = json.load(file)


def find_sessions(
    topic: str,
    available_from: str,
    available_until: str,
) -> dict:
    """Find sessions matching a topic within a requested time window.

    Args:
        topic: Topic or interest, such as AI, agents, or cloud.
        available_from: Start of the available time in HH:MM format.
        available_until: End of the available time in HH:MM format.

    Returns:
        Matching sessions from the sample conference agenda.
    """
    topic = topic.lower()

    start_window = datetime.strptime(available_from, "%H:%M").time()
    end_window = datetime.strptime(available_until, "%H:%M").time()

    matches = []

    for session in SESSIONS:
        session_start = datetime.strptime(
            session["start_time"], "%H:%M"
        ).time()
        session_end = datetime.strptime(
            session["end_time"], "%H:%M"
        ).time()

        topic_matches = (
            topic in session["title"].lower()
            or any(topic in tag.lower() for tag in session["tags"])
        )

        time_matches = (
            session_start >= start_window
            and session_end <= end_window
        )

        if topic_matches and time_matches:
            matches.append(session)

    return {
        "count": len(matches),
        "sessions": matches,
    }


def validate_schedule(session_ids: list[str]) -> dict:
    """Validate selected session IDs and check for schedule overlaps.

    Args:
        session_ids: IDs of the selected sessions, such as ["S001", "S003"].

    Returns:
        Validation status and any detected schedule conflicts.
    """
    sessions_by_id = {
        session["id"]: session for session in SESSIONS
    }

    unknown_ids = [
        session_id
        for session_id in session_ids
        if session_id not in sessions_by_id
    ]

    selected_sessions = [
        sessions_by_id[session_id]
        for session_id in session_ids
        if session_id in sessions_by_id
    ]

    selected_sessions.sort(key=lambda session: session["start_time"])

    conflicts = []

    for index in range(len(selected_sessions) - 1):
        current = selected_sessions[index]
        next_session = selected_sessions[index + 1]

        if current["end_time"] > next_session["start_time"]:
            conflicts.append({
                "session_1": current["title"],
                "session_2": next_session["title"],
                "overlap": (
                    f'{next_session["start_time"]}–'
                    f'{current["end_time"]}'
                ),
            })

    is_valid = not unknown_ids and not conflicts

    return {
        "valid": is_valid,
        "unknown_session_ids": unknown_ids,
        "conflicts": conflicts,
        "message": (
            "Schedule is valid."
            if is_valid
            else "Schedule has issues. Review the conflicts or IDs."
        ),
    }


root_agent = Agent(
    name="devfest_buddy",
    model="gemini-3.5-flash",
    description="A conference assistant that finds and validates sessions.",
    instruction="""
    You are DevFest Buddy, a conference session assistant.

    Help users find sessions based on their interests and available time.

    Use find_sessions to retrieve matching sessions.
    Use validate_schedule to check selected session IDs before presenting
    a final schedule.

    Never invent sessions. Use only the provided sample agenda.
    If the schedule has conflicts, explain them clearly.
    Include session titles, times, and locations in your response.
    """,
    tools=[find_sessions, validate_schedule],
)