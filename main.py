import streamlit as st
import plotly.graph_objects as go
import random

def run_mbti_diagnostic():
    st.set_page_config(page_title="MBTI性格診断 Pro", page_icon="🧠", layout="wide")

    st.markdown('<h3 style="font-size: 26px; font-weight: bold; color: #4A90E2;">🧠 性格タイプ診断 Pro (究極のパーソナライズ版)</h3>', unsafe_allow_html=True)
    # [2025-12-18] のルールに基づき、時刻を表示
    st.caption("2025年12月23日 05:45：具体的アドバイスとメンター指名機能を統合しました。")

    # --- 質問データ (24問) ---
    questions = [
        ("多人数で集まるイベントに参加すると元気が出る", "E-I", 1),
        ("自分の考えを整理するときは、誰かに話すより一人で考えたい", "E-I", -1),
        ("知らない人にも自分から話しかけるのは苦ではない", "E-I", 1),
        ("活動的な一日の後は、一人で静かに過ごす時間が必要だ", "E-I", -1),
        ("新しいアイデアより、すでに証明されているやり方を信頼する", "S-N", 1),
        ("空想より、現実的な問題解決に興味がある", "S-N", 1),
        ("物事の裏に隠された「意味」について考えるのが好きだ", "S-N", -1),
        ("詳細データより、インスピレーションを信じることが多い", "S-N", -1),
        ("決断を下す際、論理や効率を最も重視する", "T-F", 1),
        ("悩みを聞くとき、解決策を提示するよりまず気持ちに寄り添いたい", "T-F", -1),
        ("正論でも、誰かを傷つける可能性があるなら言葉を選ぶべきだ", "T-F", -1),
        ("誰かが間違っていたら、場の空気を壊してでも訂正すべきだと思う", "T-F", 1),
        ("やるべきことはリスト化して、一つずつ消していくのが好きだ", "J-P", 1),
        ("旅行に行くときは、予定を細かく決めずに動きたい", "J-P", -1),
        ("仕事や勉強は、締め切りギリギリにならないと本気が出ない", "J-P", -1),
        ("決まったルールやルーティンを守ることに安心感を覚える", "J-P", 1),
        ("注目を浴びる立場になることは、どちらかといえば好きだ", "E-I", 1),
        ("マニュアルがある場合、それを忠実に守る方だ", "S-N", 1),
        ("人から「共感力が高い」と言われるより「頭が良い」と言われたい", "T-F", 1),
        ("予期せぬトラブルにも臨機応変に対応することを楽しめる", "J-P", -1),
        ("ストレスを感じる状況でも、比較的冷静でいられる", "A-T", 1),
        ("過去の失敗をいつまでも悔やんでしまうことがある", "A-T", -1),
        ("自分の能力や決断に自信を持っている", "A-T", 1),
        ("他人の目が気になり、自分を過小評価してしまうことがある", "A-T", -1),
    ]

    # --- メンターデータ ---
    mentor_data = {
        "ギャル先生": {
            "quote": "「おはよー！あんたの魅力、マジでバズり確定じゃん！✨ その調子で今日もハピネスに、自分軸でブチ上げてこー！💖」",
            "actions": ["「コンビニの新作スイーツ買って自分にご褒美あげちゃお！✨」", "「鏡の前で『今日も可愛いじゃん』って言ってみて！💖」"]
        },
        "頼れるお姉さん": {
            "quote": "「一生懸命なところ、素敵よ。でもたまには肩の力を抜いて、私に甘えていいのよ？」",
            "actions": ["「5分だけデジタルデトックスをして温かい飲み物を。心の充電が必要よ。」", "「寝る前に頑張ったことを3つ思い出して自分を褒めてあげてね。」"]
        },
        "カサネ・イズミ：論理と不確定要素": {
            "quote": "「あなたのデータは極めて特異だ。その思考を最適化すれば、さらなる高みへ到達できる。」",
            "actions": ["「デスクを整理しろ。視覚的ノイズを排除しろ。」", "「今日学んだことを3行でメモしろ。」"]
        },
        "ツンデレな指導員": {
            "quote": "「ふん、あんたみたいなタイプは私が付いてないと危なっかしいわね。しっかりしなさいよ！」",
            "actions": ["「姿勢を正しなさい！シャキッとするでしょ？」", "「たまには自分を甘やかしなさいよね。心配してないわよ！」"]
        }
    }

    # --- 進捗管理 ---
    answered_count = 0
    for i in range(len(questions)):
        key = f"q_{i}"
        if key in st.session_state and st.session_state[key] is not None:
            answered_count += 1
    
    with st.sidebar:
        st.header("📊 診断の進捗")
        progress_per = answered_count / len(questions)
        st.progress(progress_per)
        st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
        st.divider()
        st.markdown("**ギャル先生からの応援**")
        if progress_per < 0.5: st.write("「まずは直感でポチポチいこー！✨」")
        elif progress_per < 1.0: st.write("「いい感じ！半分超えたよ、あと少し！🔥」")
        else: st.write("「完璧！あんたマジ最高！ボタン押しちゃいな！💖」")

    # --- 質問表示 ---
    user_answers = {}
    for i, (q_text, axis, weight) in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q_text}**")
        user_answers[i] = st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5], 
                                   format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                                   key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
        st.write("---")

    # --- 診断実行 ---
    if st.button("診断結果を詳しく見る ✨", use_container_width=True):
        if answered_count < len(questions):
            st.error(f"まだ回答していない質問があるよ！（残り {len(questions) - answered_count} 問）")
        else:
            st.session_state["show_result"] = True

    if st.session_state.get("show_result"):
        st.balloons()
        scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0}
        for i, (q_text, axis, weight) in enumerate(questions):
            scores[axis] += (st.session_state[f"q_{i}"] - 3) * weight

        mbti_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                    ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        identity = "-A" if scores["A-T"] >= 0 else "-T"
        full_res = mbti_core + identity

        # --- 具体的なタイプ特徴DB (INFJの例) ---
        mbti_db = {
            "INFJ": {
                "name": "提唱者",
                "strength": "・複雑な人間関係や問題の本質を直感で見抜く力が抜群\n・強い倫理観を持ち、他人の成長を心から応援できる\n・静かな情熱を秘め、理想を現実に変えるための忍耐力がある",
                "weakness": "・完璧主義すぎて、自分や他人の小さなミスが許せなくなる\n・一人で考え込みすぎて、周囲から「何を考えているか不明」と思われがち\n・他人の感情を吸収しすぎ、突然心のエネルギーが切れてしまう",
                "mentor": "頼れるお姉さん"
            }
            # 他のタイプも同様に具体化...
        }
        
        detail = mbti_db.get(mbti_core, {"name": "未知の探求者", "strength": "未定義", "weakness": "未定義", "mentor": "ギャル先生"})

        st.divider()
        st.markdown(f"## 判定結果：{full_res}（{detail['name']}）")

        # 具体的解説
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"✨ **ここがあなたの武器（強み）**\n\n{detail['strength']}")
        with col2:
            st.warning(f"⚠️ **ここに注意（気をつけたい点）**\n\n{detail['weakness']}")

        st.divider()

        # 🤝 メンター指名セクション
        st.markdown("### 🤝 今日のメンターを指名する")
        selected_mentor = st.selectbox(
            "指名されたメンターから、今のあなたにピッタリな言葉を贈ります。",
            options=list(mentor_data.keys()),
            index=list(mentor_data.keys()).index(detail["mentor"]) if detail["mentor"] in mentor_data else 0
        )

        m_info = mentor_data[selected_mentor]
        st.chat_message("user").write(f"**{selected_mentor}**：「{m_info['quote']}」")
        st.success(f"🎁 **今日のラッキーアクション**：{random.choice(m_info['actions'])}")

if __name__ == "__main__":
    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False
    run_mbti_diagnostic()
