import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    raw_df = pd.read_csv("reddit_sim_unmoderated.csv")
    mod_df = pd.read_csv("reddit_sim_moderated.csv")

    for df in (raw_df, mod_df):
        df["comment_id"] = df["comment_id"].astype(int)
        df["thread_id"] = df["thread_id"].astype(int)
        df["step"] = df["step"].astype(int)
        df["author_display"] = df["author_id"].apply(lambda x: f"User {int(x)}")

    if "flagged" in mod_df.columns:
        mod_df["flagged"] = mod_df["flagged"].astype(bool)
    else:
        mod_df["flagged"] = False

    if "moderation_message" not in mod_df.columns:
        mod_df["moderation_message"] = ""

    return raw_df, mod_df


raw_df, mod_df = load_data()

# Page setup
st.set_page_config(page_title="Reddit Simulation", layout="wide")

st.markdown(
    """
    <h1> Simulated Reddit</h1>
    <p style="color:#555; font-size:0.9rem;">
        Reddit-style conversations generated from our simulation, shown with and without the ToxiMuncher (Lite) moderator.
    </p>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    body { background-color: #dae0e6; }

    /* make posts and the first comment feel closer */
    .post-block {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 8px;    
        border: 1px solid #ccc;
    }

    .post-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 4px;
    }

    .comment {
        background-color: #ffffff;
        border-radius: 4px;
        padding: 8px;
        margin-top: 2px;       /* small gap above each comment */
        border-left: 3px solid #bbb;
        font-size: 0.9rem;
    }

    .comment-removed {
        background-color: #f8f8f8;
        border-radius: 4px;
        padding: 8px;
        margin-top: 2px;
        border-left: 3px solid #ff4500;
        font-size: 0.9rem;
        color: #555;
        font-style: italic;
    }

    .meta {
        font-size: 0.75rem;
        color: #555;
        margin-bottom: 3px;
    }

    .depth-0 { margin-left: 0px; }
    .depth-1 { margin-left: 18px; }
    .depth-2 { margin-left: 36px; }
    .depth-3 { margin-left: 54px; }
    .depth-4 { margin-left: 72px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# Helper: build thread order
def build_thread_tree(thread_df):
    thread_df = thread_df.sort_values(["step", "comment_id"])
    rows = thread_df.to_dict("records")

    by_id = {r["comment_id"]: r for r in rows}
    children = {r["comment_id"]: [] for r in rows}
    roots = []

    for r in rows:
        cid = r["comment_id"]
        pid = r["parent_id"]
        if pd.isna(pid):
            roots.append(cid)
        else:
            children[int(pid)].append(cid)

    ordered = []

    def dfs(cid, depth):
        ordered.append((by_id[cid], depth))
        for child in children.get(cid, []):
            dfs(child, depth + 1)

    for root in roots:
        dfs(root, 0)

    return ordered


# Sidebar filters
st.sidebar.header("Options")

subreddits = sorted(raw_df["subreddit"].unique())
selected_subreddit = st.sidebar.selectbox(
    "Subreddit",
    options=["All"] + subreddits,
)

if selected_subreddit != "All":
    raw_view = raw_df[raw_df["subreddit"] == selected_subreddit].copy()
    mod_view = mod_df[mod_df["subreddit"] == selected_subreddit].copy()
else:
    raw_view = raw_df.copy()
    mod_view = mod_df.copy()

all_thread_ids = sorted(raw_view["thread_id"].unique())
thread_ids = all_thread_ids  


# Function to create threads
def render_threads(df_view, thread_ids, use_moderation=False):
    for tid in thread_ids:
        thread_df = df_view[df_view["thread_id"] == tid]
        if thread_df.empty:
            continue

        ordered = build_thread_tree(thread_df)

        # top post
        post_row, _ = ordered[0]
        post_text = post_row["text"]
        post_author = post_row["author_display"]
        post_subreddit = post_row["subreddit"]
        post_num = int(tid) + 1

        st.markdown(
            f"""
            <div class="post-block">
                <div class="post-title">
                    Post {post_num} in {post_subreddit}
                </div>
                <div class="meta">
                    Posted by {post_author}
                </div>
                <div style="margin-top: 6px; font-size: 0.9rem;">
                    {post_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # comments
        for row, depth in ordered[1:]:
            author = row["author_display"]
            step = int(row["step"])
            depth_class = f"depth-{min(depth, 4)}"

            if use_moderation and row.get("flagged", False):
                msg = row.get(
                    "moderation_message",
                    "ToxiMuncher (Lite): comment removed for toxic or aggressive behaviour.",
                )
                html = f"""
                <div class="comment-removed {depth_class}">
                    <div class="meta">
                        {author} • step {step}
                    </div>
                    <div>{msg}</div>
                </div>
                """
            else:
                text = row["text"]
                html = f"""
                <div class="comment {depth_class}">
                    <div class="meta">
                        {author} • step {step}
                    </div>
                    <div>{text}</div>
                </div>
                """

            st.markdown(html, unsafe_allow_html=True)


# Tabs: before vs after moderation
tab1, tab2 = st.tabs(["Unmoderated view", "Moderated view (ToxiMuncher Lite)"])

with tab1:
    st.write("### Original conversations (no moderator)")
    render_threads(raw_view, thread_ids, use_moderation=False)

with tab2:
    st.write("### Conversations with ToxiMuncher (Lite model)")
    render_threads(mod_view, thread_ids, use_moderation=True)
