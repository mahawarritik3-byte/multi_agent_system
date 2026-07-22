import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexusResearch OS · Intelligence Synthesis",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS: Obsidian & Gold Cyberpunk Workspace ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

/* ── Base Reset ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    color: #e2e8f0;
}

.stApp {
    background-color: #07080a;
    background-image: 
        radial-gradient(at 0% 0%, rgba(245, 158, 11, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(217, 119, 6, 0.05) 0px, transparent 50%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3.5rem 4rem; max-width: 1400px; }

/* ── Header Studio ── */
.studio-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(245, 158, 11, 0.2);
    margin-bottom: 2rem;
}
.studio-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.03em;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.studio-logo span {
    color: #f59e0b;
}
.studio-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 0.25rem 0.7rem;
    border-radius: 4px;
    letter-spacing: 0.1em;
}

/* ── Command Box ── */
.search-card {
    background: rgba(15, 17, 23, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    margin-bottom: 2rem;
}

.stTextInput > div > div > input {
    background: rgba(7, 8, 10, 0.9) !important;
    border: 1px solid rgba(245, 158, 11, 0.25) !important;
    border-radius: 8px !important;
    color: #f8fafc !important;
    font-size: 1.05rem !important;
    padding: 0.8rem 1.2rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15) !important;
}

/* ── Action Button ── */
.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: #07080a !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border-radius: 8px !important;
    padding: 0.8rem 1.8rem !important;
    border: none !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.25) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(245, 158, 11, 0.4) !important;
}

/* ── Side Telemetry Cards ── */
.telemetry-card {
    background: rgba(15, 17, 23, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    position: relative;
}
.telemetry-card.running {
    border-color: rgba(245, 158, 11, 0.6);
    background: rgba(245, 158, 11, 0.05);
}
.telemetry-card.done {
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.04);
}
.node-id {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    margin-bottom: 0.2rem;
}
.node-title {
    font-weight: 600;
    font-size: 0.92rem;
    color: #f1f5f9;
}
.node-status {
    position: absolute;
    top: 1rem;
    right: 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
}
.status-wait { color: #475569; }
.status-run { color: #f59e0b; animation: blink 1.2s infinite; }
.status-ok  { color: #10b981; }

@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.3; }
    100% { opacity: 1; }
}

/* ── Content Workspace ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    color: #64748b !important;
    padding-bottom: 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    color: #f59e0b !important;
    border-bottom-color: #f59e0b !important;
}

.deliverable-box {
    background: rgba(15, 17, 23, 0.7);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 12px;
    padding: 2.2rem;
    margin-top: 1.2rem;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}

.footer-note {
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #475569;
    margin-top: 4rem;
}
</style>
""", unsafe_allow_html=True)


# ── Render Node Card ──────────────────────────────────────────────────────────
def render_node(node_id: str, title: str, state: str):
    label_map = {
        "waiting": ("STANDBY", "status-wait"),
        "running": ("ACTIVE",  "status-run"),
        "done":    ("SUCCESS", "status-ok"),
    }
    label, cls = label_map.get(state, ("STANDBY", "status-wait"))
    card_cls = {"running": "running", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="telemetry-card {card_cls}">
        <span class="node-status {cls}">{label}</span>
        <div class="node-id">AGENT NODE // 0{node_id}</div>
        <div class="node-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)


# ── State Init ────────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="studio-header">
    <div class="studio-logo">
        ⚛️ Nexus<span>Research</span>
    </div>
    <div class="studio-tag">SYSTEM v3.0 ACTIVE</div>
</div>
""", unsafe_allow_html=True)


# ── Split Workspace Layout ───────────────────────────────────────────────────
col_telemetry, col_workspace = st.columns([1.1, 2.5], gap="large")

with col_telemetry:
    st.markdown('<div style="font-family:\'Space Mono\', monospace; font-size:0.75rem; color:#f59e0b; margin-bottom:0.8rem; letter-spacing:0.1em;">AGENTS CONTROL CONSOLE</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def get_state(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    render_node("1", "Web Intelligence Node", get_state("search"))
    render_node("2", "Source Content Extractor", get_state("reader"))
    render_node("3", "Synthesis & Writer Agent", get_state("writer"))
    render_node("4", "Quality Evaluation Critic", get_state("critic"))


with col_workspace:
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    c_in, c_btn = st.columns([3.5, 1.2], gap="small")
    with c_in:
        topic = st.text_input(
            "Target Subject",
            placeholder="Describe topic e.g. Autonomous AI Agents framework in 2026",
            key="topic_input",
            label_visibility="collapsed"
        )
    with c_btn:
        run_btn = st.button("Synthesize ⚡", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Preset Chips
    st.markdown("""
    <div style="display:flex; gap:0.5rem; align-items:center; margin-top:-1.2rem; margin-bottom:2rem;">
        <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#64748b;">PRESETS:</span>
    """, unsafe_allow_html=True)
    for preset in ["Multi-agent LLM systems", "Generative AI in healthcare", "Quantum hardware 2026"]:
        st.markdown(f"""
        <span style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 4px;
            padding: 0.2rem 0.5rem;
            font-size: 0.72rem;
            color: #94a3b8;
        ">{preset}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Output Space
    res = st.session_state.results
    if res:
        tab1, tab2, tab3 = st.tabs(["📄 Synthesis Report", "🎯 Peer Evaluation", "🔬 Raw Telemetry Log"])

        with tab1:
            if "writer" in res:
                st.markdown('<div class="deliverable-box">', unsafe_allow_html=True)
                st.markdown(res["writer"])
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    label="Export Report (.md)",
                    data=res["writer"],
                    file_name=f"nexus_research_{int(time.time())}.md",
                    mime="text/markdown",
                )

        with tab2:
            if "critic" in res:
                st.markdown('<div class="deliverable-box">', unsafe_allow_html=True)
                st.markdown(res["critic"])
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            if "search" in res:
                with st.expander("Search Node Output Log", expanded=False):
                    st.code(res["search"], language="markdown")
            if "reader" in res:
                with st.expander("Extractor Node Output Log", expanded=False):
                    st.code(res["reader"], language="markdown")


# ── Execution Loop ────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # Step 1
    with st.spinner("Search Node querying sources…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 2
    with st.spinner("Reader Node scraping resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 3
    with st.spinner("Writer Node drafting report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # Step 4
    with st.spinner("Critic Node evaluating report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
    NexusResearch OS · Multi-Agent Intelligence Platform
</div>
""", unsafe_allow_html=True)