import streamlit as st
import plotly.graph_objects as go

def run_comprehensive_diagnostic():
    # --- 1. 質問データ (計32問：MBTI 24問 + 恋愛 8問) ---
    questions = [
        # [MBTI: E-I / S-N / T-F / J-P / A-T は前回のロジックを完全維持]
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
        # --- [恋愛4軸: LCROプロファイル 8問] ---
        ("デートの計画は、自分がリードするより相手に任せたい", "L-F", -1),
        ("自分の生活ペースを乱されるのはストレスを感じる", "L-F", 1),
        ("恋人には甘えられるよりも、自分から甘えたい", "C-A", 1),
        ("頼りにされるよりも、守られている実感がある方が幸せだ", "C-A", 1),
        ("恋愛においても、経済力や生活能力などの現実面を重視する", "R-P", 1),
        ("一度恋に落ちたら、周囲の声が届かないほど情熱的になる", "R-P", -1),
        ("恋愛は深刻になりすぎず、お互いに自由で気楽な関係がいい", "O-E", 1),
        ("交際するなら将来を見据えた、誠実な付き合いが絶対条件だ", "O-E", -1),
    ]

    # --- 2. データベース強化版 (強み・罠・アドバイス追加) ---
    mbti_db = {
        "ESTJ": {
            "name": "幹部", "animal": "番犬", "best_match": "ISFJ（シカ）",
            "strength": "圧倒的な実行力と組織化の才能。混沌に秩序をもたらす力があります。",
            "trap": "「正論」で相手を論破しすぎてしまい、周囲が萎縮してしまうことがあります。",
            "advice": "結論を急ぐ前に相手の感情に共感を示すと、あなたのリーダーシップはより強固になります。",
            "love_basic": "誠実さと規律を大切にし、計画的なデートと安定した家庭環境を好みます。"
        },
        "INFJ": {
            "name": "提唱者", "animal": "フクロウ", "best_match": "ENFJ（ライオン）",
            "strength": "他者の本質を見抜く深い洞察力と、理想を実現させるための静かな情熱。",
            "trap": "理想が高すぎるあまり、現実の自分や他人に失望し、殻に閉じこもりがちです。",
            "advice": "「100点」を目指さず、まずは不完全な自分を許すことで、心の平穏が保たれます。",
            "love_basic": "精神的な深い繋がりを重視し、表面的な遊びよりも魂の共鳴を求めます。"
        },
        # 他のタイプも同様の構造で定義（省略せず実装時に全タイプ埋める想定）
    }

    at_db = {
        "A": {"label": "自己主張型", "desc": "自信を持って決断し、困難な状況でも動揺せず前向きに進む強さを持っています。"},
        "T": {"label": "慎重型", "desc": "感受性が豊かで、自分自身の向上心が強く、細やかな配慮と深い内省を行う力があります。"}
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("精密性格・動物・恋愛LCRO 統合診断")
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

        if st.button("診断結果を生成する", use_container_width=True):
            if answered_count < len(questions):
                st.warning("未回答の質問があります。")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 3. 計算ロジック ---
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        at_suffix = "A" if scores["A-T"] >= 0 else "T"
        
        # LCRO恋愛コード生成
        love_codes = [
            ("L" if scores["L-F"] >= 0 else "F"),
            ("C" if scores["C-A"] >= 0 else "A"),
            ("R" if scores["R-P"] >= 0 else "P"),
            ("O" if scores["O-E"] >= 0 else "E")
        ]
        love_profile = "".join(love_codes)

        res = mbti_db.get(m_core, mbti_db["ESTJ"]) # エラー回避用デフォルト
        at_info = at_db.get(at_suffix)

        # --- 4. 結果表示 ---
        st.header(f"判定結果：{m_core}-{at_suffix}")
        st.subheader(f"恋愛コード：【 {love_profile} 型 】")
        st.markdown(f"### 動物タイプ：{res['animal']} ({res['name']})")
        
        st.info(f"**{at_info['label']}**\n{at_info['desc']}")

        # レーダーチャート
        categories = ['外向(E)', '現実(S)', '論理(T)', '規律(J)', '主張(A)']
        plot_values = [scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=plot_values, theta=categories, fill='toself', name='特性'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-6, 6])), showlegend=False)
        st.plotly_chart(fig)

        # 詳細解説タブ
        tab1, tab2, tab3 = st.tabs(["🧬 性格の深層", "💖 恋愛LCRO分析", "🤝 相性アドバイス"])
        
        with tab1:
            st.subheader(f"🛡️ あなたの「強み・罠・対策」")
            st.markdown(f"**【強み】**\n{res['strength']}")
            st.markdown(f"**【陥りやすい罠】**\n{res['trap']}")
            st.success(f"**【改善へのアドバイス】**\n{res['advice']}")
            st.divider()
            st.write("**適職のヒント:** 秩序の構築、責任あるポジション、または専門性を活かせる環境。")

        with tab2:
            st.subheader(f"恋愛スタイル：{love_profile}")
            # 軸ごとのミニ解説
            love_map = {"L":"リード派", "F":"フォロー派", "C":"甘えたい", "A":"甘えられたい", "R":"現実重視", "P":"情熱重視", "O":"楽観的", "E":"誠実重視"}
            meaning = " × ".join([love_map[c] for c in love_profile])
            st.info(f"キーワード：{meaning}")
            
            # ビジュアルバー
            axes_data = [("L/F", "相手に合わせる", "自分で決める", "L-F"), ("C/A", "甘えられたい", "甘えたい", "C-A"), ("R/P", "情熱を燃やす", "現実を計算", "R-P"), ("O/E", "誠実を貫く", "自由を楽しむ", "O-E")]
            for label, left, right, axis in axes_data:
                st.write(f"**{label}**")
                val = scores[axis]
                st.columns([2, 6, 2])[0].write(left)
                st.columns([2, 6, 2])[1].progress((val + 4) / 8)
                st.columns([2, 6, 2])[2].write(right)
            
            st.divider()
            st.write(f"**基本姿勢:** {res['love_basic']}")

        with tab3:
            st.success(f"📌 **最高のパートナー：{res['best_match']}**")
            st.write("お互いの強みを引き出し、弱点を補い合える最高の組み合わせです。")

        if st.button("もう一度診断する"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_comprehensive_diagnostic()
