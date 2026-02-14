import streamlit as st
import plotly.graph_objects as go

def run_perfect_diagnostic():
    # --- 1. 質問データ (計32問：MBTI 24問 + 恋愛 8問) ---
    questions = [
        # [MBTI: E-I] 
        ("初対面の人が多い場所でも、自分から進んで会話を楽しむ", "E-I", 1),
        ("週末は外に出かけるよりも、家でゆっくり一人で過ごす方が回復する", "E-I", -1),
        ("グループの中心で注目を浴びることに抵抗がない", "E-I", 1),
        ("考えをまとめる時は、話しながらよりも書き出しながらの方が捗る", "E-I", -1),
        # [MBTI: S-N]
        ("抽象的な概念よりも、目に見える具体的な事実を重視する", "S-N", 1),
        ("想像力を働かせるよりも、現実的なデータに基づいて判断したい", "S-N", 1),
        ("物事の「なぜ」よりも「どのように機能するか」に興味がある", "S-N", 1),
        ("直感やインスピレーションを信じて行動することが多い", "S-N", -1),
        # [MBTI: T-F]
        ("議論では感情に流されず、論理的に正しいかどうかを優先する", "T-F", 1),
        ("人の悩みを聞く時は、アドバイスよりもまず共感することを心がけている", "T-F", -1),
        ("客観的な真実よりも、人間関係の調和を守ることの方が大切だと思う", "T-F", -1),
        ("誰かが間違っていたら、場の空気を壊してでも訂正すべきだと思う", "T-F", 1),
        # [MBTI: J-P]
        ("やるべきことはリスト化して、一つずつ消していくのが好きだ", "J-P", 1),
        ("旅行に行くときは、予定を細かく決めずに動きたい", "J-P", -1),
        ("整理整頓が得意で、身の回りは常に整っている方だ", "J-P", 1),
        ("ギリギリまで選択肢を残しておきたいタイプだ", "J-P", -1),
        # [MBTI: A-T]
        ("人からどう見られているか、あまり気にならない", "A-T", 1),
        ("失敗すると長く落ち込みやすく、自分を責めてしまう", "A-T", -1),
        ("自分の能力や決断に自信を持っている", "A-T", 1),
        ("周囲の環境変化に対して、敏感にストレスを感じやすい", "A-T", -1),
        # [MBTI: 補完4問]
        ("マニュアルよりも自分の経験を信じる", "S-N", 1),
        ("感情を表に出すのは苦手な方だ", "T-F", 1),
        ("予期せぬトラブルにも臨機応変に対応するのが得意だ", "J-P", -1),
        ("一人でいると寂しさを感じ、誰かと繋がっていたい", "E-I", 1),
        
        # --- [恋愛4軸: LCROプロファイル 8問] ---
        ("デートの計画は、自分がリードするより相手に任せたい", "L-F", -1), # Lead(L) / Follow(F)
        ("自分の生活ペースを乱されるのはストレスを感じる", "L-F", 1),
        ("恋人には甘えられるよりも、自分から甘えたい", "C-A", 1),    # Cuddly(C) / Accept(A)
        ("頼りにされるよりも、守られている実感がある方が幸せだ", "C-A", 1),
        ("恋愛においても、経済力や生活能力などの現実面を重視する", "R-P", 1), # Realistic(R) / Passionate(P)
        ("一度恋に落ちたら、周囲の声が届かないほど情熱的になる", "R-P", -1),
        ("恋愛は深刻になりすぎず、お互いに自由で気楽な関係がいい", "O-E", 1), # Optimistic(O) / Earnest(E)
        ("交際するなら将来を見据えた、誠実な付き合いが絶対条件だ", "O-E", -1),
    ]

    # --- 2. 16タイプ完全紐付けマスターテーブル ---
    mbti_db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "best_match": "ENTP（キツネ）"},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "best_match": "ENTJ（ワシ）"},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "best_match": "INTP（チンパンジー）"},
        "ENTP": {"name": "討論者", "animal": "キツネ", "best_match": "INTJ（トラ）"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "best_match": "ENFJ（ライオン）"},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "best_match": "ENFP（カワウソ）"},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "best_match": "INFJ（フクロウ）"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "best_match": "INFP（ウサギ）"},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "best_match": "ESFJ（ゾウ）"},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "best_match": "ESTJ（番犬）"},
        "ESTJ": {"name": "幹部", "animal": "番犬", "best_match": "ISFJ（シカ）"},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "best_match": "ISTJ（ビーバー）"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "best_match": "ESTP（チーター）"},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "best_match": "ESFP（レッサーパンダ）"},
        "ESTP": {"name": "起業家", "animal": "チーター", "best_match": "ISTP（サメ）"},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "best_match": "ISFP（ネコ）"},
    }

    # A/T別性格補足データ
    at_db = {
        "A": "【自己主張型】自信を持って決断し、ストレス耐性が高く、前向きに目標へ進みます。",
        "T": "【慎重型】感受性が豊かで、細かな変化に気づき、より良い結果を求めて努力を惜しみません。"
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("精密性格・動物・恋愛LCRO 統合診断アプリ")
        
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(answered_count / len(questions))
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")

        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "当てはまらない", 2: "やや当てはまらない", 3: "中立", 4: "やや当てはまる", 5: "当てはまる"}[x],
                    key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")

        if st.button("診断結果を表示", use_container_width=True):
            if answered_count < len(questions):
                st.warning("すべての質問に回答してください。")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 3. 計算ロジック ---
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        # MBTI 16タイプ
        m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        at_suffix = "A" if scores["A-T"] >= 0 else "T"
        m_type = f"{m_core}-{at_suffix}"

        # 恋愛コード LCRO
        l_code = "L" if scores["L-F"] >= 0 else "F"
        c_code = "C" if scores["C-A"] >= 0 else "A"
        r_code = "R" if scores["R-P"] >= 0 else "P"
        o_code = "O" if scores["O-E"] >= 0 else "E"
        love_profile = f"{l_code}{c_code}{r_code}{o_code}"

        # DBから情報取得 (バグ回避のため辞書から直接取得)
        res_data = mbti_db.get(m_core)
        at_text = at_db.get(at_suffix)

        # --- 4. 結果表示 ---
        st.header(f"判定タイプ：{m_type}")
        st.subheader(f"恋愛コード：【 {love_profile} 型 】")
        st.markdown(f"### 動物タイプ：{res_data['animal']} ({res_data['name']})")
        st.info(f"**{at_text}**")

        # 特性レーダーチャート
        categories = ['外向(E)', '直感(N)', '感情(F)', '計画(J)', '主張(A)']
        plot_values = [scores["E-I"], -scores["S-N"], -scores["T-F"], scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=plot_values, theta=categories, fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-6, 6])), showlegend=False)
        st.plotly_chart(fig)

        tab1, tab2, tab3 = st.tabs(["🧬 性格・適職", "💖 恋愛LCROプロファイル", "🤝 相性"])
        
        with tab1:
            st.write(f"**{res_data['name']}の特性:** 事実に基づいた分析が得意で、責任感が強いタイプです。")
            st.write(f"**向いている環境:** 組織化された場、明確なルールがある仕事、リーダーシップを求められる場面。")
        
        with tab2:
            st.subheader(f"LCRO分析：{love_profile}")
            love_axes = [
                ("Lead / Follow", "相手に合わせたい (F)", "自分で決めたい (L)", "L-F"),
                ("Cuddly / Accept", "頼られたい (A)", "甘えたい (C)", "C-A"),
                ("Realistic / Passionate", "情熱的 (P)", "現実的 (R)", "R-P"),
                ("Optimistic / Earnest", "誠実重視 (E)", "自由重視 (O)", "O-E")
            ]
            for label, left, right, axis in love_axes:
                st.write(f"**{label}**")
                val = scores[axis]
                progress_val = (val + 4) / 8
                cols = st.columns([2, 6, 2])
                cols[0].write(left)
                cols[1].progress(min(max(progress_val, 0.0), 1.0))
                cols[2].write(right)

        with tab3:
            st.success(f"📌 **最高の相性：{res_data['best_match']}**")

        if st.button("もう一度診断する"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_perfect_diagnostic()
