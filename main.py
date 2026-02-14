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
    "INTJ": {"name": "建築家", "animal": "トラ", "match": "ENTP",
             "desc_A": "揺るぎない自信を持つ戦略家。独自のビジョンを冷徹なまでに遂行し、効率的に目標を達成します。",
             "desc_T": "向上心の塊である完璧主義者。自分の理論が正しいか絶えず検証し、より高い知性を求めて内省します。"},
    "INTP": {"name": "論理学者", "animal": "チンパンジー", "match": "ENTJ",
             "desc_A": "客観的で知的な自由人。自分の知性に自信を持ち、周囲の評価を気にせず独創的な発想を楽しみます。",
             "desc_T": "真理を追究する思索家。自分の考えに不備がないか常に自問自答し、緻密な論理を組み立てる努力家です。"},
    "ENTJ": {"name": "指揮官", "animal": "ワシ", "match": "INTP",
             "desc_A": "圧倒的な威厳を持つリーダー。困難を恐れず、最短距離で勝利を掴み取る決断力と自信に満ちています。",
             "desc_T": "緻密な戦略を練る司令官。目標達成への情熱が強く、現状に満足せず常に改善の余地を模索し続けます。"},
    "ENTP": {"name": "討論者", "animal": "キツネ", "match": "INTJ",
             "desc_A": "恐れ知らずの革命児。議論を楽しみ、新しいアイデアを次々と形にする社交性と行動力を持っています。",
             "desc_T": "機知に富んだ探究者。自分のアイデアが万全か批判的に検討し、より洗練された解決策を追求します。"},
    "INFJ": {"name": "提唱者", "animal": "フクロウ", "match": "ENFJ",
             "desc_A": "自信に満ちた導き手。自分の信念に迷いがなく、理想の世界を実現するために静かに、力強く行動します。",
             "desc_T": "感受性豊かな提唱者。他者の心の機微を鋭く察知し、完璧な理想を求めて深く内省する精神性を持ちます。"},
    "INFP": {"name": "仲介者", "animal": "ウサギ", "match": "ENFP",
             "desc_A": "自分を肯定できる理想主義者。独自の価値観を大切にし、穏やかな自信を持って自分らしく生きる人です。",
             "desc_T": "心優しき完璧主義者。理想と現実のギャップに悩みつつも、それゆえに誰よりも深い共感と美学を持ちます。"},
    "ENFJ": {"name": "主人公", "animal": "ライオン", "match": "INFJ",
             "desc_A": "カリスマ的な導き手。周囲を元気づける才能に溢れ、自分の影響力を信じて皆を明るい未来へ導きます。",
             "desc_T": "献身的な平和主義者。他人の幸せを心から願い、自分が十分に役立っているかを常に気遣う優しい人です。"},
    "ENFP": {"name": "広報運動家", "animal": "カワウソ", "match": "INFP",
             "desc_A": "自由を愛する冒険家。自分の感性を信じ、新しい可能性に飛び込む明るさと楽観的なエネルギーがあります。",
             "desc_T": "共感力の高い表現者。周囲の反応に敏感で、皆が楽しめる場所を作るために細やかな配慮を欠かしません。"},
    "ISTJ": {"name": "管理者", "animal": "ビーバー", "match": "ESFJ",
             "desc_A": "揺るぎない実務家。伝統と秩序を重んじ、自分のやり方に自信を持って着実に責任を果たします。",
             "desc_T": "几帳面な仕事人。ミスがないか細部まで徹底的にチェックし、誠実さと正確さで周囲の信頼を勝ち取ります。"},
    "ISFJ": {"name": "擁護者", "animal": "シカ", "match": "ESTJ",
             "desc_A": "落ち着きのある守護者。周囲を支える自分の役割を誇りに思い、安定した包容力で場を整えます。",
             "desc_T": "細やかな配慮の達人。大切な人のために自分ができる最善を尽くし、常に改善点を探す謙虚な努力家です。"},
    "ESTJ": {"name": "幹部", "animal": "番犬", "match": "ISFJ",
             "desc_A": "堂々とした組織運営者。規律を重視し、迷いのない決断でチームを効率的に統率する力があります。",
             "desc_T": "責任感の塊。社会的な規範を完璧に守ろうと努め、細部まで行き届いた管理で組織を安定させます。"},
    "ESFJ": {"name": "領事", "animal": "ゾウ", "match": "ISTJ",
             "desc_A": "明るい社交界の主役。自分のサービス精神に自信を持ち、皆が心地よい環境を積極的に作り出します。",
             "desc_T": "おもてなしの専門家。周囲の期待に応えられているかを常に意識し、和を乱さないよう細心の注意を払います。"},
    "ISTP": {"name": "巨匠", "animal": "サメ", "match": "ESTP",
             "desc_A": "冷静沈着な技術者。自分のスキルを信頼し、どんなトラブルにも動じず即興で解決する強さがあります。",
             "desc_T": "技を磨く専門職。自分の分析が正確か常に検証し、より洗練された手法をストイックに追い求めます。"},
    "ISFP": {"name": "冒険家", "animal": "ネコ", "match": "ESFP",
             "
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
