import streamlit as st
import plotly.graph_objects as go
import random

def run_imperial_integrated_diagnostic():
    # --- 1. 質問データ (32問：性格24問 + 恋愛8問) ---
    # ネット標準の「一致＝左側の文字に加点」というシンプルなロジックです
    questions = [
        # MBTI 24問
        ("知らない人と話すのは刺激的で楽しい", "E-I"),
        ("注目を浴びることに抵抗がない", "E-I"),
        ("週末は誰かと会って過ごしたい", "E-I"),
        ("一人の時間よりも、賑やかな場所にいたい", "E-I"),
        ("現実的で具体的な事実を重視する", "S-N"),
        ("経験に基づいた確かな方法を好む", "S-N"),
        ("空想よりも目の前の作業に集中する", "S-N"),
        ("マニュアルがある方が安心する", "S-N"),
        ("論理的に正しいかどうかで判断する", "T-F"),
        ("感情よりも効率や正論を優先する", "T-F"),
        ("客観的な真実が大切だと思う", "T-F"),
        ("議論では納得感のある理屈を求める", "T-F"),
        ("予定を立てて、その通りに進めたい", "J-P"),
        ("決まり事はきっちり守る方だ", "J-P"),
        ("部屋やデスクは整理整頓されている", "J-P"),
        ("物事を早く決着させてスッキリしたい", "J-P"),
        ("自分に自信があり、あまり物怖じしない", "A-T"),
        ("ストレスに強く、すぐ立ち直れる", "A-T"),
        ("他人の目はあまり気にならない", "A-T"),
        ("自分の決断に迷うことは少ない", "A-T"),
        ("行動する前に悩むより、まず動く", "E-I"), # 追加分
        ("細かい数字やデータのチェックが得意だ", "S-N"),
        ("公平な評価をすることが得意だ", "T-F"),
        ("時間厳守は社会人の基本だと思う", "J-P"),
        # 恋愛LCRO 8問
        ("デートのプランは自分がリードして決めたい", "L-F"),
        ("パートナーには甘えたり頼ったりしたい", "C-A"),
        ("相手の経済力や安定性は結婚に必須だ", "R-P"),
        ("束縛のない自由な関係が理想だ", "O-E"),
        ("恋人をリードする方が自分らしい", "L-F"),
        ("包容力よりも、可愛がられたい欲求が強い", "C-A"),
        ("愛があればお金は二の次とは言えない", "R-P"),
        ("交際中も一人の時間を絶対に確保したい", "O-E"),
    ]

    # --- 2. データベース (3つの要素を紐付け) ---
    # ネットの標準的な性格・動物・恋愛傾向を統合
    db = {
        "ESTJ": {"name": "幹部", "animal": "番犬", "match": "ISFJ", "strength": "圧倒的実行力", "trap": "独断専行", "love": "計画的で誠実な愛"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "match": "ENFJ", "strength": "深い洞察力", "trap": "自己犠牲", "love": "精神的な深い絆"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "match": "INFP", "strength": "自由な創造性", "trap": "集中力欠如", "love": "ドラマチックな恋"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "match": "ESTP", "strength": "冷静な分析力", "trap": "孤立しがち", "love": "干渉しない自立した恋"},
        # ※本来は全16タイプ分を記述
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 3. 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("性格 × 動物 × 恋愛 帝国統合診断")
        
        # サイドバー：進捗バー
        answered = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(answered / len(questions))
            st.write(f"**{answered} / {len(questions)} 問**")

        for i, (q_text, axis) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", ["不一致", "やや不一致", "中立", "やや一致", "一致"], 
                     key=f"q_{i}", horizontal=True, index=2, label_visibility="collapsed")
            st.write("---")
        
        if st.button("診断結果を生成", use_container_width=True):
            st.session_state["show_result"] = True
            st.rerun()

    else:
        # --- 4. スコア計算 (ネット標準：3を中心に加点) ---
        mapping = {"不一致": 1, "やや不一致": 2, "中立": 3, "やや一致": 4, "一致": 5}
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        
        for i, (_, axis) in enumerate(questions):
            val = mapping[st.session_state[f"q_{i}"]]
            scores[axis] += (val - 3)

        # 判定ロジック
        mbti = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
               ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        at = "A" if scores["A-T"] >= 0 else "T"
        lcro = ("L" if scores["L-F"] >= 0 else "F") + ("C" if scores["C-A"] >= 0 else "A") + \
               ("R" if scores["R-P"] >= 0 else "P") + ("O" if scores["O-E"] >= 0 else "E")

        res = db.get(mbti, db["ESTJ"]) # 未登録分はESTJを仮出力

        # --- 5. 結果表示 (3要素を網羅) ---
        st.header(f"判定タイプ：{mbti}-{at}")
        st.subheader(f"動物：{res['animal']} ／ 恋愛：{lcro}型")
        
        st.success(f"🌟 **今週のラッキーアクション**\n\n「 {res.get('name')}らしい休息をとる 」")

        # レーダーチャート
        st.divider()
        st.markdown("### 📊 特性チャート")
        fig = go.Figure(data=go.Scatterpolar(
            r=[scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]],
            theta=['外向(E)', '現実(S)', '論理(T)', '規律(J)', '自信(A)'], fill='toself'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-10, 10])), showlegend=False)
        st.plotly_chart(fig)

        # 詳細タブ
        t1, t2, t3 = st.tabs(["🧬 性格分析", "💖 恋愛傾向", "🤝 相性"])
        with t1:
            st.write(f"**強み:** {res['strength']}")
            st.write(f"**注意点:** {res['trap']}")
        with t2:
            st.write(f"**恋愛タイプ:** {lcro}")
            st.write(f"**傾向:** {res['love']}")
        with t3:
            st.write(f"**ベストパートナー:** {res['match']}")

        if st.button("再診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_imperial_integrated_diagnostic()
