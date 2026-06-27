import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

# ── Page config ──
st.set_page_config(
    page_title="Isha Cottage Assistant",
    page_icon="🏡",
    layout="centered"
)

# ── Session state ──
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ──
st.title("🏡 Isha Cottage Assistant")
st.caption("Ask me anything about the Terms & Conditions")

# ── Clear chat button ──
if st.button("Clear Chat"):
    requests.delete(f"{API_URL}/session/{st.session_state.session_id}")
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()

st.divider()

# ── Render chat history ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📄 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- Page **{s['page']}** — `{s['source']}`")

# ── Chat input ──
if prompt := st.chat_input("Ask a question about Isha Cottage T&C..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "query": prompt,
                        "session_id": st.session_state.session_id
                    },
                    timeout=60
                )
                data = response.json()
                answer = data["answer"]
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("📄 Sources"):
                        for s in sources:
                            st.markdown(f"- Page **{s['page']}** — `{s['source']}`")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:
                st.error(f"Error connecting to API: {e}")