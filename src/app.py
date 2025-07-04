import streamlit as st

from contents_fetcher import fetch_dummy
from contents_filtering_simulator import FilterBubbleSimulator

# --- セッション状態の初期化 ---
if "simulator" not in st.session_state:
    st.session_state.simulator = FilterBubbleSimulator(
        {
            "general": 0.2,
            "entertainment": 0.2,
            "sports": 0.2,
            "technology": 0.2,
            "science": 0.1,
            "business": 0.1,
        },
        fetcher=fetch_dummy,
    )

if "articles" not in st.session_state:
    st.session_state.articles = []

if "last_read" not in st.session_state:
    st.session_state.last_read = None

if "read_trigger" not in st.session_state:
    st.session_state.read_trigger = False

sim = st.session_state.simulator

# --- タイトル ---
st.title("Filterbubble Simulator")

# --- 直前に読んだ記事があれば表示 ---
if st.session_state.read_trigger and st.session_state.last_read:
    a = st.session_state.last_read
    st.success(f"✅ 「{a['category']}」カテゴリの記事を読みました！")
    st.session_state.read_trigger = False  # 表示したらリセット

# --- 積み上げ棒グラフでカテゴリの重みの推移を描画 ---
st.subheader("バラエティの推移")

fig = sim.plot()  # ファイル保存なしでFigureを返す

st.pyplot(fig)

# --- おすすめ記事表示 ---
# 1ステップ分の記事を取得して表示
st.subheader("おすすめ記事")

# --- 記事のリストをセッションに保持（初期表示 or 再ステップ）
if "article_list" not in st.session_state:
    st.session_state.article_list = sim.step(num_articles=10)

article_list = st.session_state.article_list

# --- 記事ボタン表示
for i, article in enumerate(article_list):
    btn_label = f"[{article['category']}] {article['title']}"
    if st.button(btn_label, key=f"article_btn_{i}"):
        # カテゴリ選択＆更新
        sim.select(article["category"])

        # 明示的に状態を上書き（これがないと Streamlit の rerun 後に反映されない）
        st.session_state.simulator = sim
        st.session_state.last_read = article
        st.session_state.articles.append(article)

        # ✅ 新しい記事リストを削除して次回更新
        del st.session_state.article_list

        # 再実行でグラフ描画とリスト更新を反映
        st.rerun()


# --- 自動実行 ---
st.subheader("🧪 自動シミュレーション")
output_area = st.empty()


def display_in_streamlit(iteration, articles):
    with output_area.container():
        st.write(f"### 🔄 Iteration {iteration}")
        for _, a in enumerate(articles):
            st.markdown(f"- [{a['category']}] {a['title']}")


if st.button("自動で5ステップ実行する"):
    sim.run_simulation(num_iterations=5, auto=True)
    st.session_state.simulator = sim
    st.rerun()


# --- リセット ---
st.subheader("🧼 リセット")
if st.button("セッションをリセット"):
    for key in ["simulator", "articles", "last_read", "read_trigger"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
