import streamlit as st
import plotly.graph_objects as go
import random

def run_mbti_diagnostic():
    # --- 1. 質問データ (合計30問) ---
    # MBTI 24問 + ラブタイプ(L) 6問
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
        # --- ラブタイプ質問 (女王セレスティアの判別用) ---
        ("恋人には自分の全てを知っていてほしいし、相手の全てを把握したい", "L", 2), # 裏：支配・情熱
        ("パートナーとの間でも、礼儀や気高さは保つべきだと思う", "L", -1),        # 表：高貴・プライド
        ("愛する人のためなら、自分を犠牲にして尽くすことに喜びを感じる", "L", 5), # 真：慈愛
        ("束縛されるくらいなら、一人でいる方が自由でマシだ", "L", -2),          # 表（自律寄り）
        ("恋人が自分を蔑ろにしたら、相応の報い（言葉や態度）を与えるべきだ", "L", 2), # 裏：罵声・鞭
        ("最後はどんな過ちも、深い愛で包み込み許したいと思う", "L", 5)           # 真：人格者
    ]

    # --- 2. メンターデータ ---
    mentor_data = {
        "女王セレスティア": {
            "quote": "「私の前に跪きなさい。あなたの魂の形、私が直々に審判を下してあげるわ。」",
            "actions": ["「高貴な一服を楽しみなさい。安物は許さないわよ。」", "「私への献上金（寄付）の準備はできていて？誰かのためになる行為こそが真の気高さよ。」", "「今日は自分を律しなさい。堕落は私の前では罪よ。」"]
        },
        "ギャル先生": {
            "quote": "「おはよー！あんたの魅力、マジでバズり確定じゃん！✨ その調子で今日もハピネスに、自分軸でブチ上げてこー！💖」",
            "actions": ["「コンビニの新作スイーツ買って自分にご褒美あげちゃお！✨」", "「鏡の前で『今日も可愛いじゃん』って言ってみて？💖」", "「派手な色の小物を1つ身につけてみて！🌈」"]
        },
        "頼れるお姉さん": { "quote": "「一生懸命なところ、素敵よ。でもたまには甘えていいのよ？」", "actions": ["「5分だけデジタルデトックスをしてね。」"] },
        "カサネ・イズミ：論理と不確定要素": { "quote": "「あなたのデータは極めて特異だ。思考を最適化しろ。」", "actions": ["「デスクの上を片付けろ。視覚的なノイズを排除しろ。」"] }
    }

    # MBTI DB (中略...基本構造は維持) 
    # ※ detail['messages'] に "女王セレスティア" のセリフを追加したものと想定
    mbti_db = {
        "INFJ": {
            "name": "提唱者", "animal": "フクロウ", "catchphrase": "「夜の静寂の中で、未来の光を見通す賢者」",
            "strengths": "洞察力、深い共感、理想主義。", "weaknesses": "完璧主義、燃え尽きやすい。",
            "details": {"work": "本質を見抜くリーダー", "love": "精神的な深い繋がりを重視", "stress": "感覚過敏になり引きこもる", "best_match": "ENFJ（ライオン）"},
            "messages": {
                "女王セレスティア": "フクロウ、あなたのその深い洞察力...私の側近にふさわしいわ。光栄に思いなさい。",
                "ギャル先生": "フクロウちゃん、世界観エグい！その感性マジで尊いよ！🌈"
            }
        },
        # (他の15タイプも同様に拡張可能)
    }

    # --- 4. セッション管理 ---
    if "show_result" not in st.session_state: st.session_state["show_result"] = False
    if "run_count" not in st.session_state: st.session_state["run_count"] = 0

    # --- 5. 画面表示 ---
    if not st.session_state["show_result"]:
        st.title("帝国性格診断クエスト 🏰")
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}_{st.session_state['run_count']}") is not None)
        
        with st.sidebar:
            st.header("📊 帝国の検問進捗")
            st.progress(answered_count / len(questions))
            st.write(f"**{answered_count} / {len(questions)} 問** 通過")
            st.divider()
            if answered_count == len(questions): st.success("「完璧！あんたマジ最高！💖」（ギャル先生）")

        for i, (q_text, axis, weight) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                    key=f"q_{i}_{st.session_state['run_count']}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")

        if st.button("審判を仰ぐ（診断結果を見る） ✨", use_container_width=True):
            if answered_count < len(questions):
                st.error(f"まだ回答が足りないわよ！（残り {len(questions) - answered_count} 問）")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 結果計算 ---
        if "final_detail" not in st.session_state:
            st.balloons()
            scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0, "L": 0}
            for i, (_, axis, _) in enumerate(questions):
                val = st.session_state.get(f"q_{i}_{st.session_state['run_count']}", 3)
                scores[axis] += (val - 3) 

            m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                     ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
            
            # ラブタイプ判定（女王セレスティアの3モード）
            l_score = scores["L"]
            if l_score >= 6: 
                l_mode, l_name = "真", "【慈愛の女神】思いやりと愛で包み込む人格者"
            elif l_score <= -2: 
                l_mode, l_name = "表", "【高貴な君主】プライドが高く理想を求める"
            else: 
                l_mode, l_name = "裏", "【情熱の支配者】鞭を振るい罵声を浴びせる"

            st.session_state["final_full_res"] = m_core + ("-A" if scores["A-T"] >= 0 else "-T")
            st.session_state["final_detail"] = mbti_db.get(m_core, mbti_db.get("INFJ")) # Default to INFJ for safety
            st.session_state["final_scores"] = scores
            st.session_state["love_mode"] = (l_mode, l_name)

        detail = st.session_state["final_detail"]
        l_mode, l_name = st.session_state["love_mode"]

        st.markdown(f"## 判定結果：{st.session_state['final_full_res']}")
        st.markdown(f"### 動物タイプ：『 {detail['animal']} 』")
        st.info(f"**{detail['catchphrase']}**")

        tab1, tab2, tab3, tab4 = st.tabs(["📊 特性分析", "💖 ラブタイプ", "🤝 メンター", "💰 帝国の慈愛"])

        with tab1:
            st.markdown(f"✅ **強み**: {detail['strengths']}")
            st.markdown(f"⚠️ **弱み**: {detail['weaknesses']}")
            # レーダーチャート表示 (省略せず実装を推奨)

        with tab2:
            st.subheader(f"👑 セレスティア・モード：{l_mode}")
            st.markdown(f"**称号：{l_name}**")
            st.write(detail['details']['love'])
            st.caption("※このラブタイプは、あなたの心の深層にある『女王の二面性』を示しています。")

        with tab3:
            selected_mentor = st.selectbox("メンターを指名", options=list(mentor_data.keys()))
            msg = detail["messages"].get(selected_mentor, mentor_data[selected_mentor]["quote"])
            st.chat_message("assistant").write(f"**{selected_mentor}**：「{msg}」")
            st.success(f"🎁 **アクション**：{random.choice(mentor_data[selected_mentor]['actions'])}")

        with tab4:
            st.write("### 🌍 帝国の社会貢献")
            st.write("このブログ「帝国」では、収益の一部を基金や育英会に寄付しています。")
            st.markdown("> **現在の野望：収益化を達成し、累計寄付額の証拠をアップすること。**")
            st.write("あなたの診断結果が、いつか誰かの未来に繋がるかもしれません。")

        if st.button("🔄 帝国の門を再び叩く", use_container_width=True):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_mbti_diagnostic()
