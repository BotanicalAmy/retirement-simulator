import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from page_elements import footer, side_content

st.set_page_config(page_title="Financial Design", page_icon="🎨", layout="wide")
st.markdown("# Financial Design")
st.markdown("""
Future outcomes are enabled by small, incremental changes in the present. How you prioritize your spending dictates the options available to you in the future. Intentionally direct your finances to design a future that is aligned with what matters most.

Use the **50/30/20** framework as a starting point: **50% toward needs, 30% toward wants, 20% toward your future.**
""")

st.divider()

def _editor_key(state_key):
    v = st.session_state.get(f"_v_{state_key}", 0)
    return f"editor_{state_key}_v{v}"

def _commit_edits(state_key):
    """Merge all edits into source df; bump widget version on add/delete."""
    key = _editor_key(state_key)
    diff = st.session_state.get(key) or {}
    source = st.session_state[state_key].copy()

    for idx, changes in diff.get("edited_rows", {}).items():
        idx = int(idx)
        for col, val in changes.items():
            if idx < len(source):
                source.at[idx, col] = val

    deleted = sorted([int(i) for i in diff.get("deleted_rows", [])], reverse=True)
    for idx in deleted:
        if idx < len(source):
            source = source.drop(index=idx)
    if deleted:
        source = source.reset_index(drop=True)

    added = diff.get("added_rows", [])
    for r in added:
        new_row = {"Category": r.get("Category", ""), "Monthly Goal": float(r.get("Monthly Goal", 0) or 0)}
        source = pd.concat([source, pd.DataFrame([new_row])], ignore_index=True)

    st.session_state[state_key] = source

    # Bump key on structural changes so the widget reinitializes with a clean diff
    if added or deleted:
        vk = f"_v_{state_key}"
        st.session_state[vk] = st.session_state.get(vk, 0) + 1

def _total_from_diff(state_key):
    """Read current section total from editor diff — no side effects."""
    diff = st.session_state.get(_editor_key(state_key)) or {}
    source = st.session_state.get(state_key)
    if source is None:
        return 0.0
    deleted = set(diff.get("deleted_rows", []))
    rows = diff.get("edited_rows", {})
    total = 0.0
    for i in range(len(source)):
        if i in deleted or str(i) in deleted:
            continue
        r = rows.get(i, rows.get(str(i), {}))
        g = r.get("Monthly Goal", float(source.iloc[i]["Monthly Goal"]))
        total += float(g or 0)
    for r in diff.get("added_rows", []):
        total += float(r.get("Monthly Goal", 0) or 0)
    return total

# --- Income Input ---
inc_col, info_col = st.columns([1, 2])
with inc_col:
    st.markdown("**Monthly take-home pay (after tax)**")
    income_str = st.text_input("Monthly income", label_visibility="collapsed", placeholder="e.g. 5,000")
    monthly_income = 0.0
    if income_str:
        try:
            monthly_income = float(income_str.replace(',', '').replace('$', '').strip())
        except ValueError:
            st.error("Please enter a valid number")

with info_col:
    _needs_now = _total_from_diff('needs_df')
    _wants_now = _total_from_diff('wants_df')
    _future_now = _total_from_diff('future_df')
    _total_now = _needs_now + _wants_now + _future_now
    _inc_disp = monthly_income if monthly_income > 0 else 0
    _pct_alloc = min(_total_now / monthly_income * 100, 100) if monthly_income > 0 else 0
    _future_pct = min(_future_now / monthly_income * 100, 100) if monthly_income > 0 else 0
    st.markdown(
        f'<div style="background-color:#e2e8f7;border:1px solid #c7c2d6;border-radius:4px;padding:12px 16px;margin-top:28px;">'
        f'<b>{_pct_alloc:.0f}%</b> of your &#36;{_inc_disp:,.0f} monthly income has been allocated. '
        f'<b>{_future_pct:.0f}%</b> of your income is dedicated to your future.<br>'
        f'<strong><a href="/Retirement_Explorer" target="_self" style="color:#59579e; text-decoration:none;"'
        f' onmouseover="this.style.color=\'#645c77\'" onmouseout="this.style.color=\'#59579e\'">'
        f'Explore your Retirement</a></strong>'
        f'</div>',
        unsafe_allow_html=True
    )

st.divider()

# --- Default Data ---
col_config = {
    'Category':     st.column_config.TextColumn('Category'),
    'Monthly Goal': st.column_config.NumberColumn('Monthly Goal', format="$%.0f", min_value=0, step=10),
}

def _default(categories):
    return pd.DataFrame({'Category': categories, 'Monthly Goal': [0.0] * len(categories)})

DEFAULTS = {
    'needs_df':  _default(['Housing','Utilities','Phone','Insurance','Auto','Groceries','Gas','Clothing','Maintenance']),
    'wants_df':  _default(['Dining Out','Subscriptions','Personal Care','Giving']),
    'future_df': _default(['Investments','Debt Payment']),
}
for key, df in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = df.copy()


def section(title, target_pct, state_key, income):
    target_amt = income * target_pct
    actual_amt = _total_from_diff(state_key)
    header = f"**{title}**"
    if income > 0:
        header += (
            f"&nbsp; <small>target &#36;{target_amt:,.0f}/mo"
            f"&nbsp;|&nbsp;actual &#36;{actual_amt:,.0f}/mo</small>"
        )
    st.markdown(header, unsafe_allow_html=True)

    editor_key = _editor_key(state_key)
    diff = st.session_state.get(editor_key) or {}
    n_rows = (len(st.session_state[state_key])
              + len(diff.get("added_rows", []))
              - len(diff.get("deleted_rows", [])))
    height = 38 + (n_rows + 1) * 35

    edited: pd.DataFrame = st.data_editor(
        st.session_state[state_key],
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config=col_config,
        key=editor_key,
        height=height,
        on_change=_commit_edits,
        args=(state_key,),
    )

    goals = pd.to_numeric(edited['Monthly Goal'], errors='coerce').fillna(0)
    return goals.sum(), edited


# --- Layout: needs | wants+future | chart ---
left_col, mid_col, right_col = st.columns([1, 1, 1], gap="large")

with left_col:
    needs_total, needs_edited = section("Needs", 0.50, 'needs_df', monthly_income)

with mid_col:
    wants_total, wants_edited   = section("Wants",  0.30, 'wants_df',  monthly_income)
    st.markdown("")
    future_total, future_edited = section("Future", 0.20, 'future_df', monthly_income)

with right_col:
    st.markdown("**Financial Design**")

    buckets = ['Needs', 'Wants', 'Future']
    totals  = [needs_total, wants_total, future_total]
    colors  = ['#59579e', '#54758e', '#cc9a48']

    pcts = [t / monthly_income * 100 for t in totals] if monthly_income > 0 else [0.0, 0.0, 0.0]

    fig = go.Figure()

    for bucket, pct, color in zip(buckets, pcts, colors):
        fig.add_trace(go.Bar(
            x=[bucket], y=[pct],
            marker_color=color,
            showlegend=False,
            text=f"{pct:.1f}%" if monthly_income > 0 else "",
            textposition='outside',
            textfont=dict(color='#374151'),
            hovertemplate=f"{bucket}: %{{y:.1f}}%<extra></extra>",
        ))

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=13, color='#374151')),
        yaxis=dict(
            range=[0, 80],
            ticksuffix='%',
            tickfont=dict(size=13, color='#374151'),
            title='% of Income',
            title_font=dict(size=13, color='#374151'),
        ),
        paper_bgcolor='#f7f7f9',
        plot_bgcolor='#f7f7f9',
        height=360,
        margin=dict(l=10, r=20, t=30, b=40),
        hoverlabel=dict(bgcolor='white'),
    )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={"displayModeBar": False})

    if monthly_income > 0:
        total_allocated = needs_total + wants_total + future_total
        unallocated = monthly_income - total_allocated
        if unallocated > 0:
            st.markdown(f"<small>&#36;{unallocated:,.0f}/mo unallocated</small>", unsafe_allow_html=True)
        elif unallocated < 0:
            st.markdown(f'<small style="color:red;font-weight:bold;">&#36;{abs(unallocated):,.0f}/mo over budget</small>', unsafe_allow_html=True)
        else:
            st.markdown('<small style="color:green;font-weight:bold;">Fully allocated ✓</small>', unsafe_allow_html=True)

    st.markdown("")
    st.download_button(
        label="Download Budget as CSV",
        data=pd.concat([
            needs_edited.assign(Bucket='Needs'),
            wants_edited.assign(Bucket='Wants'),
            future_edited.assign(Bucket='Future'),
        ], ignore_index=True)[['Bucket','Category','Monthly Goal']].to_csv(index=False),
        file_name="financial_design.csv",
        mime="text/csv",
    )

# --- Pass totals to other pages via session state ---
st.session_state['budget_annual_income']       = monthly_income * 12
st.session_state['budget_annual_contribution'] = future_total * 12
st.session_state['budget_total_allocated']     = needs_total + wants_total + future_total

footer()

with st.sidebar:
    side_content()
