import streamlit as st
import plotly.graph_objects as go
import random

def run_balanced_diagnostic():
    # --- 1. 質問データ (逆転項目を導入してバイアスを排除) ---
    # 第3引数の 1 は「一致=右の文字」、-1 は「一致=左の文字」を意味します
    questions = [
        # [E-I]
        ("初対面の人との会話でエネルギーをもらう", "E-I", 1), # 一致ならE
        ("一人の時間がないと、精神的に疲弊してしまう", "E-I", -1), # 一致ならI
        # [S-N]
        ("具体的な事実やデータこそが最も信頼できる", "S-N", 1),  # 一致ならS
        ("物事の裏に隠された意味や可能性を想像するのが好きだ", "S-N", -1), # 一致ならN
        # [T-F]
        ("感情よりも、論理的に正しいかどうかを優先する", "T-F", 1),  # 一致ならT
        ("他人の感情に共感し、調和を保つことが何より大切だ", "T-F", -1), # 一致ならF
        # [J-P]
        ("予定は事前に細かく決めておきたい", "J-P", 1),  # 一致ならJ
        ("その場の気分で予定を変えることにワクワクする", "J-P", -1), # 一致ならP
        # [A-T]
        ("批判されてもあまり動揺せず、すぐに立ち直れる", "A-T", 1),  # 一致ならA
        ("ささいな失敗でも、後で一人で反省して落ち込みやすい", "A-T", -1), # 一致ならT
        # --- 追加の「揺さぶり」質問 ---
        ("直感よりも経験を信じる", "S-N", 1),
        ("結論を急ぐよりも、多くの選択肢を検討し続けたい", "J-P", -1),
        ("人から「優しい」と言われるより「有能だ」と言われたい", "T-F", 1),
        ("一晩寝れば嫌なことはだいたい忘れられる", "A-T", 1),
    ]

    # --- 2. データベース (全16タイプ 完備) ---
    # ※前回の辞書データをそのまま使用
    mbti_db = {
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "best_match": "ENFJ", "strength": "深い洞察力と強い信念。", "trap": "自分を犠牲にしすぎる。", "advice": "自分を許す時間を。", "lucky_pool": ["日記を書く", "ハーブティーを飲む"]},
        "ESTJ": {"name": "幹部", "animal": "番犬", "best_match": "ISFJ", "strength": "圧倒的な実行力。", "trap": "正論で追い詰める。", "advice": "共感の確認を。", "lucky_pool": ["靴を磨く", "ToDoリスト消化"]},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "best_match": "ENFP", "strength": "豊かな感性と優しさ。", "trap": "理想に溺れる。", "advice": "現実をキャンバスに。", "lucky_pool": ["空を撮る", "お気に入りの曲"]},
        # 他、全16タイプを網羅（実装時は全キーが必要）
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 3. 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("精密MBTI・動物・恋愛診断")
        
        # サイドバー進捗
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(answered_count / len(questions))
            st.write(f"**{answered_count} / {len(questions)} 問**")

        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "不一致", 2: "やや不一致", 3: "中立", 4: "やや一致", 5: "一致"}[x],
                    key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")
        
        if st.button("診断結果を生成"):
            if answered_count < len(questions):
                st.warning("すべて回答してください。")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 4. 計算ロジック (バイアス修正版) ---
        raw_scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T"]}
        for i, (_, axis, weight) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            # (選択肢 1-5) - 3 = (-2, -1, 0, 1, 2) 
            # これに weight (1 or -1) を掛ける
            raw_scores[axis] += (val - 3) * weight

        # 判定関数
        def judge(score, pos_char, neg_char):
            if score > 0: return pos_char
            elif score < 0: return neg_char
            else: return random.choice([pos_char, neg_char]) # 0の場合はランダム

        m_core = judge(raw_scores["E-I"], "E", "I") + \
                 judge(raw_scores["S-N"], "S", "N") + \
                 judge(raw_scores["T-F"], "T", "F") + \
                 judge(raw_scores["J-P"], "J", "P")
        at_suffix = judge(raw_scores["A-T"], "A", "T")

        res = mbti_db.get(m_core, {"name": "不明", "animal": "？", "lucky_pool": ["深呼吸する"]})
        
        # --- 5. 表示 (チャート復活) ---
        st.header(f"判定：{m_core}-{at_suffix}")
        st.subheader(f"動物タイプ：{res['animal']} ({res['name']})")
        
        # レーダーチャート
        categories = ['外向(E)', '現実(S)', '論理(T)', '規律(J)', '主張(A)']
        # スコアを正規化してチャートに反映
        fig = go.Figure(data=go.Scatterpolar(
            r=[raw_scores["E-I"], raw_scores["S-N"], raw_scores["T-F"], raw_scores["J-P"], raw_scores["A-T"]],
            theta=categories, fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-6, 6])), showlegend=False)
        st.plotly_chart(fig)

        st.success(f"🌟 ラッキーアクション: {random.choice(res['lucky_pool'])}")

        if st.button("もう一度診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_balanced_diagnostic()
