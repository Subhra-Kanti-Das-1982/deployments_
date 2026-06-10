import streamlit as st

from rag.ingest import ingest
from rag.retriever import retrieve

from memory.user_memory import (
    load_memory,
    save_memory,
    update_profile,
    dominant_pattern
)

from coaching.analyzer import (
    analyze,
    create_search_query
)

from scoring.scorecard import (
    generate_scorecard
)

from scoring.radar import (
    render_radar
)

st.set_page_config(
    page_title=
    "Dharma Reflection Assistant",
    page_icon="🕉️",
    layout="wide"
)

st.title(
    "🕉️ Dharma Reflection Assistant"
)

st.markdown(
"""
Describe a situation.

Example:

> I insulted my friend publicly because he lied to me.

> Did I do anything wrong?

The assistant evaluates actions through:

- Dharma
- Karma
- Satya
- Karuna
- Self-Control

using Indian mythology.
"""
)

with st.spinner(
    "Loading mythology corpus..."
):
    ingest()

profile = load_memory()

with st.sidebar:

    st.header(
        "Behavior Profile"
    )

    st.json(profile)

    st.markdown("---")

    st.subheader(
        "Recurring Pattern"
    )

    st.info(
        dominant_pattern(
            profile
        )
    )

if "history" not in st.session_state:

    st.session_state.history = []

for role, content in st.session_state.history:

    with st.chat_message(role):

        st.markdown(content)

question = st.chat_input(
    "Describe your action..."
)

if question:

    st.session_state.history.append(
        (
            "user",
            question
        )
    )

    with st.chat_message(
        "user"
    ):
        st.markdown(question)

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Reflecting through Dharma..."
        ):

            search_query = (
                create_search_query(
                    question
                )
            )

            docs, sources = retrieve(
                search_query
            )

            context = (
                "\n\n".join(
                    docs
                )
            )

            answer = analyze(
                question,
                context,
                profile
            )

            scores = (
                generate_scorecard(
                    question,
                    context
                )
            )

            profile = update_profile(
                profile,
                scores
            )

            save_memory(
                profile
            )

            st.markdown(
                answer
            )

            st.markdown(
                "---"
            )

            st.subheader(
                "Dharma Scorecard"
            )

            render_radar(
                scores
            )

            cols = st.columns(6)

            metrics = [
                (
                    "Dharma",
                    scores["dharma"]
                ),
                (
                    "Satya",
                    scores["satya"]
                ),
                (
                    "Karuna",
                    scores["karuna"]
                ),
                (
                    "Self Control",
                    scores[
                        "self_control"
                    ]
                ),
                (
                    "Responsibility",
                    scores[
                        "responsibility"
                    ]
                ),
                (
                    "Ego",
                    scores["ego"]
                )
            ]

            for col, item in zip(
                cols,
                metrics
            ):

                label, value = item

                col.metric(
                    label,
                    value
                )

            st.markdown(
                "---"
            )

            st.subheader(
                "Behavioral Reflection"
            )

            pattern = (
                dominant_pattern(
                    profile
                )
            )

            st.info(
                f"""
Recurring tendency detected:

{pattern}

Dharma is shaped not by a single
action but by repeated patterns.

Reflect on whether this theme
appears repeatedly in your life.
"""
            )

            st.subheader(
                "Sources"
            )

            displayed = set()

            for source in sources:

                src = source[
                    "source"
                ]

                if src in displayed:
                    continue

                displayed.add(src)

                st.write(
                    f"• {src}"
                )

    st.session_state.history.append(
        (
            "assistant",
            answer
        )
    )