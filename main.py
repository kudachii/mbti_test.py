import streamlit as st
import plotly.graph_objects as go
import random

def run_imperial_complete_app():
    # --- 1. 質問データ (32問) ---
    questions = [
        ("初対面の人が多い場所でも、自分から進んで会話を楽しむ", "E-I", 1),
        ("週末は外に出かけるよりも、家で一人で過ごす方が回復する", "E-I", -1),
        ("グループの中心で注目を浴びることに抵抗がない", "E-I", 1),
        ("考えをまとめる時は、書き出しながらの方が捗る", "E-I", -1),
        ("具体的な事実やデータを重視する", "S-N", 1),
        ("直感やインスピレーションを信じる", "S-N", -1),
        ("物事の仕組みや論理に興味がある", "S-N", 1),
        ("物語や象徴的なイメージが好きだ", "S-N", -1),
        ("論理的に正しいかどうかを優先する", "T-F", 1),
        ("人の感情や調和を優先する", "T-F", -1),
        ("客観的な真実が大切だと思う", "T-F", 1),
        ("相手の気持ちに寄り添いたい", "T-F", -1),
        ("予定を立てて行動するのが好きだ", "J-P", 1),
        ("その場の流れに任せるのが好きだ", "J-P", -1),
        ("整理整頓されていると安心する", "J-P", 1),
        ("自由な状態でいたい", "J-P", -1),
        ("自分に自信がある", "A-T", 1),
        ("周囲の目が気になりやすい", "A-T", -1),
        ("ストレスに強い方だ", "A-T", 1),
        ("完璧主義で自分を責めやすい", "A-T", -1),
        ("マニュアルよりも経験を重視する", "S-N", 1),
        ("感情を出すのは苦手だ", "T-F", 1),
        ("臨機応変な対応が得意だ", "J-P", -1),
        ("誰かと繋がっていたい", "E-I", 1),
        # 恋愛8問
        ("デートは自分がリードしたい", "L-F", 1),
        ("相手のペースに合わせるのが楽だ", "L-F", -1),
        ("恋人には全力で甘えたい", "C-A", 1),
        ("恋人を守り、包容力を発揮したい", "C-A", -1),
        ("恋愛でも相手の経済力や現実面を重視する", "R-P", 1),
        ("恋には情熱的にのめり込むタイプだ", "R-P", -1),
        ("束縛のない自由で気楽な関係がいい", "O-E", 1),
        ("誠実で結婚を見据えた付き合いがいい", "O-E", -1),
    ]

    # --- 2. データベース ---
    mbti_db = {
        "ESTJ": {
            "name": "幹部", "animal": "番犬", "best_match": "ISFJ",
            "strength": "圧倒的な責任感と組織化の才能。物事を最短距離で達成する力。",
            "trap": "正論で人を追い詰めやすく、周囲の感情的な疲弊に気づきにくい点。",
            "advice": "「正しいかどうか」の前に「相手がどう感じているか」を確認する余裕を。",
            "lucky_pool": ["筋トレで汗を流す", "ToDoリストを全部消す", "早寝早起きを徹底する", "靴をピカピカに磨く"],
            "love_basic": "誠実さと規律を大切にし、計画的なデートと安定した家庭環境を好みます。"
        },
        "INFJ": {
            "name": "提唱者", "animal": "フクロウ", "best_match": "ENFJ",
            "strength": "深い洞察力と強い信念。他者の本質を見抜き、理想を形にする力。",
            "trap": "理想と現実のギャップに悩み、自分を責めて殻に閉じこもりがちな点。",
            "advice": "100点を目指さず、不完全な自分を許す時間を大切にしてください。",
            "lucky_pool": ["キャンドルを灯して瞑想", "日記を書く", "ハーブティーを飲む", "自然の中を歩く"],
            "love_basic": "精神的な一体感を求め、一度心を許すと一生尽くす誠実さを持ちます。"
        },
        # 他のタイプも同様の構造で定義
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 3. 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("性格(32種) × 動物 × 恋愛LCRO 統合診断")
        
        # 【復活】サイドバーの進捗表示
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(answered_count / len(questions))
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")

        # 質問ループ
        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            # 【復活】ラジオボタンの選択肢（1:不一致〜5:一致）
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "不一致", 2: "やや不一致", 3: "中立", 4: "やや一致", 5: "一致"}[x],
                    key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")
        
        if st.button("診断結果を生成", use_container_width=True):
            if answered_count < len(questions):
                st.warning("すべての質問に回答してください。")
            else:
                st.session_state["show_result"] = True
                st.rerun()
    else:
        # スコア計算
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        at_suffix = "A" if scores["A-T"] >= 0 else "T"
        love_profile = ("L" if scores["L-F"] >= 0 else "F") + ("C" if scores["C-A"] >= 0 else "A") + \
                       ("R" if scores["R-P"] >= 0 else "P") + ("O" if scores["O-E"] >= 0 else "E")

        res = mbti_db.get(m_core, mbti_db["ESTJ"])
        if "lucky_action" not in st.session_state:
            st.session_state["lucky_action"] = random.choice(res["lucky_pool"])

        # --- 結果表示 ---
        st.header(f"判定タイプ：{m_core}-{at_suffix}")
        st.subheader(f"恋愛コード：【 {love_profile} 型 】")
        st.markdown(f"### 動物タイプ：{res['animal']} ({res['name']})")
        
        st.success(f"🌟 **今週のラッキーアクション**\n\n「 {st.session_state['lucky_action']} 」")

        # 【復活】レーダーチャート
        st.divider()
        st.markdown("### 📊 特性チャート")
        categories = ['外向(E)', '現実(S)', '論理(T)', '規律(J)', '主張(A)']
        plot_values = [scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=plot_values, theta=categories, fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-6, 6])), showlegend=False)
        st.plotly_chart(fig)

        tab1, tab2, tab3 = st.tabs(["🧬 性格の深層", "💖 恋愛分析", "🤝 相性"])
        with tab1:
            st.markdown(f"**【あなたの強み】**\n{res['strength']}")
            st.markdown(f"**【陥りやすい罠】**\n{res['trap']}")
            st.info(f"**【アドバイス】**\n{res['advice']}")
        with tab2:
            st.write(f"**恋愛キーワード:** {love_profile}")
            st.write(f"**基本姿勢:** {res['love_basic']}")
        with tab3:
            st.success(f"📌 **最高の相性：{res['best_match']}**")

        if st.button("再診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_imperial_complete_app()
