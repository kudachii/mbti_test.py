import streamlit as st
import plotly.graph_objects as go
import random

def run_imperial_32type_app():
    # --- 1. 質問データ (32問フルセット) ---
    questions = [
        # 性格（E-I, S-N, T-F, J-P 各4問 = 16問）
        ("人と会うことでエネルギーを充電できる", "E-I"),
        ("注目を浴びることに抵抗がない", "E-I"),
        ("週末は外出して誰かと過ごしたい", "E-I"),
        ("グループの中でリーダーシップを取ることが多い", "E-I"),
        ("現実的で具体的な事実を何よりも重視する", "S-N"),
        ("経験に基づいた確かな方法を好む", "S-N"),
        ("空想よりも目の前の実務的な作業を優先する", "S-N"),
        ("マニュアルや手順が整っていると安心する", "S-N"),
        ("論理的に正しいかどうかで物事を判断する", "T-F"),
        ("感情よりも効率や客観的な正解を優先する", "T-F"),
        ("客観的な真実こそが最も大切だと思う", "T-F"),
        ("議論では理詰めで納得感のある説明を求める", "T-F"),
        ("予定を事前に立てて、その通りに進めるのが好きだ", "J-P"),
        ("決まり事はきっちり守るべきだと思う", "J-P"),
        ("整理整頓された環境にいると心が落ち着く", "J-P"),
        ("物事は早めに決着させてスッキリしたい", "J-P"),
        # アイデンティティ（A-T 軸 8問）
        ("自分に自信があり、堂々と振る舞える", "A-T"),
        ("ストレスに強く、嫌なことがあっても立ち直りが早い", "A-T"),
        ("他人の評価はあまり気にならない", "A-T"),
        ("自分の決断に迷いや後悔を感じることは少ない", "A-T"),
        ("人前で緊張することはほとんどない", "A-T"),
        ("困難な状況でも、自分の力で解決できると思う", "A-T"),
        ("過去の失敗を引きずることはない", "A-T"),
        ("周囲の期待に応えられているか不安になることはない", "A-T"),
        # 恋愛（L-F, C-A, R-P, O-E 各2問 = 8問）
        ("恋愛では自分が主導権を握ってリードしたい", "L-F"),
        ("パートナーの願いを叶えることに喜びを感じる", "L-F"), # 逆
        ("恋人には全力で甘えたい", "C-A"),
        ("恋人を包容力で守ってあげたい", "C-A"), # 逆
        ("相手には経済力や社会的な安定を求める", "R-P"),
        ("恋には情熱とロマンチックな展開を求める", "R-P"), # 逆
        ("恋人であっても一人の時間や自由が欲しい", "O-E"),
        ("誠実で結婚を見据えた交際を常に意識する", "O-E"), # 逆
    ]

    # --- 2. 16タイプ基本データベース (ここにA/Tのニュアンスが加わります) ---
    db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "match": "ENTP"},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "match": "ENTJ"},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "match": "INTP"},
        "ENTP": {"name": "討論者", "animal": "キツネ", "match": "INTJ"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "match": "ENFJ"},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "match": "ENFP"},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "match": "INFJ"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "match": "INFP"},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "match": "ESFJ"},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "match": "ESTJ"},
        "ESTJ": {"name": "幹部", "animal": "番犬", "match": "ISFJ"},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "match": "ISTJ"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "match": "ESTP"},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "match": "ESFP"},
        "ESTP": {"name": "起業家", "animal": "チーター", "match": "ISTP"},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "match": "ISFP"}
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 3. UI画面 ---
    if not st.session_state["show_result"]:
        st.title("性格32種 × 動物 × 恋愛LCRO 帝国診断")
        
        answered = sum(1 for i in range(len(questions)) if f"q_{i}" in st.session_state and st.session_state[f"q_{i}"] is not None)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(answered / len(questions))
            st.write(f"回答状況: {answered} / {len(questions)}")

        for i, (q_text, axis) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", ["不一致", "やや不一致", "中立", "やや一致", "一致"], 
                     key=f"q_{i}", horizontal=True, index=None, label_visibility="collapsed")
            st.divider()
        
        if st.button("診断結果を生成", use_container_width=True):
            if answered < len(questions):
                st.warning("未回答の質問があります。")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 4. 32タイプ判定ロジック ---
        mapping = {"不一致": 1, "やや不一致": 2, "中立": 3, "やや一致": 4, "一致": 5}
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        
        for i, (_, axis) in enumerate(questions):
            val = mapping.get(st.session_state.get(f"q_{i}"), 3)
            # 特定の質問（逆転項目）の調整
            if i in [25, 27, 29, 31]: 
                scores[axis] -= (val - 3)
            else:
                scores[axis] += (val - 3)

        # 判定：0以上なら積極的指標
        mbti_base = ("E" if scores["E-I"] >= 0 else "I") + \
                    ("S" if scores["S-N"] >= 0 else "N") + \
                    ("T" if scores["T-F"] >= 0 else "F") + \
                    ("J" if scores["J-P"] >= 0 else "P")
        
        identity = "A" if scores["A-T"] >= 0 else "T"
        full_type = f"{mbti_base}-{identity}"
        
        lcro = ("L" if scores["L-F"] >= 0 else "F") + ("C" if scores["C-A"] >= 0 else "A") + \
               ("R" if scores["R-P"] >= 0 else "P") + ("O" if scores["O-E"] >= 0 else "E")

        res = db.get(mbti_base)

        # --- 5. 結果表示 (端折らず、32タイプ・動物・恋愛を同時出力) ---
        st.header(f"判定タイプ：{full_type}")
        st.subheader(f"動物タイプ：{res['animal']} ({res['name']})")
        
        # 32タイプ解説の補足
        identity_desc = "（自己主張型：ストレスに強く前向き）" if identity == "A" else "（慎重型：感受性が強く完璧主義）"
        st.write(f"あなたは **{res['name']}** の中でも、特に **{identity_desc}** な資質を持っています。")

        # レーダーチャート
        
        st.divider()
        fig = go.Figure(data=go.Scatterpolar(
            r=[scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]],
            theta=['外向(E)', '現実(S)', '論理(T)', '規律(J)', '主張(A)'], fill='toself'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-10, 10])), showlegend=False)
        st.plotly_chart(fig)

        # タブ表示
        tab1, tab2 = st.tabs(["💖 恋愛コード分析", "🤝 ベストパートナー"])
        with tab1:
            st.markdown(f"**あなたの恋愛コード: 【 {lcro} 】**")
            st.write("このコードは、あなたの「リード力」「甘え方」「現実性」「開放性」を示しています。")
        with tab2:
            st.success(f"📌 **最高の相性：{res['match']} 型の人**")

        if st.button("再診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_imperial_32type_app()
