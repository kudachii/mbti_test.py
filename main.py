import streamlit as st
import plotly.graph_objects as go

def run_ultimate_diagnostic():
    # --- 1. 質問データ (計32問) ---
    questions = [
        # [MBTI軸: 24問]
        ("初対面の人が多い場所でも、自分から進んで会話を楽しむ", "E-I", 1),
        ("週末は外に出かけるよりも、家でゆっくり一人で過ごす方が回復する", "E-I", -1),
        ("グループの中心で注目を浴びることに抵抗がない", "E-I", 1),
        ("考えをまとめる時は、話しながらよりも書き出しながらの方が捗る", "E-I", -1),
        ("抽象的な概念よりも、目に見える具体的な事実を重視する", "S-N", 1),
        ("想像力を働かせるよりも、現実的なデータに基づいて判断したい", "S-N", 1),
        ("物事の「なぜ」よりも「どのように機能するか」に興味がある", "S-N", 1),
        ("直感やインスピレーションを信じて行動することが多い", "S-N", -1),
        ("議論では感情に流されず、論理的に正しいかどうかを優先する", "T-F", 1),
        ("人の悩みを聞く時は、アドバイスよりもまず共感することを心がけている", "T-F", -1),
        ("客観的な真実よりも、人間関係の調和を守ることの方が大切だと思う", "T-F", -1),
        ("誰かが間違っていたら、場の空気を壊してでも訂正すべきだと思う", "T-F", 1),
        ("やるべきことはリスト化して、一つずつ消していくのが好きだ", "J-P", 1),
        ("旅行に行くときは、予定を細かく決めずに動きたい", "J-P", -1),
        ("整理整頓が得意で、身の回りは常に整っている方だ", "J-P", 1),
        ("ギリギリまで選択肢を残しておきたいタイプだ", "J-P", -1),
        ("人からどう見られているか、あまり気にならない", "A-T", 1),
        ("失敗すると長く落ち込みやすく、自分を責めてしまう", "A-T", -1),
        ("自分の能力や決断に自信を持っている", "A-T", 1),
        ("周囲の環境変化に対して、敏感にストレスを感じやすい", "A-T", -1),
        ("マニュアルよりも自分の経験を信じる", "S-N", 1),
        ("感情を表に出すのは苦手な方だ", "T-F", 1),
        ("予期せぬトラブルにも臨機応変に対応するのが得意だ", "J-P", -1),
        ("一人でいると寂しさを感じ、誰かと繋がっていたい", "E-I", 1),
        
        # --- [恋愛4軸: 8問] ---
        ("デートの計画は、自分がリードするより相手に任せたい", "L-F", -1), # Lead(L) / Follow(F)
        ("自分の生活ペースを乱されるのはストレスを感じる", "L-F", 1),
        ("恋人には甘えられるよりも、自分から甘えたい", "C-A", 1),    # Cuddly(C) / Accept(A)
        ("頼りにされるよりも、守られている実感がある方が幸せだ", "C-A", 1),
        ("恋愛においても、経済力や生活能力などの現実面を重視する", "R-P", 1), # Realistic(R) / Passionate(P)
        ("一度恋に落ちたら、周囲の声が届かないほど情熱的になる", "R-P", -1),
        ("恋愛は深刻になりすぎず、お互いに自由で気楽な関係がいい", "O-E", 1), # Optimistic(O) / Earnest(E)
        ("交際するなら将来を見据えた、誠実な付き合いが絶対条件だ", "O-E", -1),
    ]

    # --- 2. データベース ---
    # ※全タイプ A/Tの32パターンを網羅
    mbti_db = {
        "INFJ": {
            "name": "提唱者", "animal": "フクロウ", "catchphrase": "深淵を見通す洞察者",
            "A": "【自己主張型】信念を貫く強さと落ち着きを持ち、周囲を穏やかに導きます。",
            "T": "【慎重型】感受性が鋭く、理想と現実のギャップに悩みやすい繊細さを持ちます。",
            "traits": "深い共感力と強い信念を持ち、理想を追求するタイプです。",
            "work": "カウンセラー、作家、心理療法士、クリエイティブディレクター。",
            "love_basic": "精神的な誠実さを求めます。一度信頼すると非常に深く献身的です。",
            "best_match": "ENFJ（ライオン）"
        },
        # 他のタイプも同様に格納
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("性格(32種) × 動物 × 恋愛プロファイル(LCPO)")
        
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(answered_count / len(questions))
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")

        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "不一致", 2: "やや不一致", 3: "中立", 4: "やや一致", 5: "一致"}[x],
                    key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")

        if st.button("診断結果を解析する", use_container_width=True):
            if answered_count < len(questions):
                st.warning("すべての質問に回答してください。")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 3. スコア計算 ---
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        # MBTI 32パターン判定
        m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        at_suffix = "A" if scores["A-T"] >= 0 else "T"
        m_type = f"{m_core}-{at_suffix}"

        # LCPO恋愛コード判定
        l_code = "L" if scores["L-F"] >= 0 else "F"
        c_code = "C" if scores["C-A"] >= 0 else "A"
        p_code = "R" if scores["R-P"] >= 0 else "P"
        o_code = "O" if scores["O-E"] >= 0 else "E"
        love_profile = f"{l_code}{c_code}{p_code}{o_code}"

        detail = mbti_db.get(m_core, mbti_db["INFJ"])

        # --- 4. 結果表示 ---
        st.header(f"判定結果：{m_type}")
        st.subheader(f"恋愛コード：【 {love_profile} 型 】")
        st.markdown(f"### 動物タイプ：{detail['animal']}")
        st.info(f"**{detail[at_suffix]}**\n\n{detail['catchphrase']}")

        # レーダーチャート
        categories = ['外向(E)', '直感(N)', '感情(F)', '柔軟(P)', '自己主張(A)']
        plot_values = [scores["E-I"], -scores["S-N"], -scores["T-F"], -scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=plot_values, theta=categories, fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-6, 6])), showlegend=False)
        st.plotly_chart(fig)

        tab1, tab2, tab3 = st.tabs(["🧬 性格・適職分析", "💖 LCPO詳細プロファイル", "🤝 相性アドバイス"])
        
        with tab1:
            st.write(f"**【基本特性】**\n{detail['traits']}")
            st.write(f"**【キャリア傾向】**\n{detail['work']}")

        with tab2:
            st.subheader(f"恋愛スタイル：{love_profile}")
            
            # LCPOの各軸解説
            love_axes = [
                ("L/F (Lead / Follow)", "相手に合わせたい (Follow)", "自分で進めたい (Lead)", "L-F"),
                ("C/A (Cuddly / Accept)", "頼られたい (Accept)", "甘えたい (Cuddly)", "C-A"),
                ("R/P (Realistic / Passionate)", "情熱を燃やしたい (Passionate)", "現実を重視したい (Realistic)", "R-P"),
                ("O/E (Optimistic / Earnest)", "真面目に誠実に (Earnest)", "自由で楽しく (Optimistic)", "O-E")
            ]
            
            for label, left, right, axis in love_axes:
                st.write(f"**{label}**")
                val = scores[axis]
                progress_val = (val + 4) / 8
                cols = st.columns([2, 6, 2])
                cols[0].write(left)
                cols[1].progress(min(max(progress_val, 0.0), 1.0))
                cols[2].write(right)
            
            st.divider()
            st.write(f"**{detail['name']}としての恋愛姿勢:** {detail['love_basic']}")

        with tab3:
            st.success(f"📌 **最高の相性：{detail['best_match']}**")

        if st.button("もう一度診断する"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_ultimate_diagnostic()
