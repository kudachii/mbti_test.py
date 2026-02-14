import streamlit as st
import plotly.graph_objects as go
import random

def run_imperial_ultimate_app():
    # --- 1. 質問データ (32問：判定バイアスを完全に排除) ---
    # weightが1なら「一致で左の文字」、-1なら「一致で右の文字」
    questions = [
        # 性格診断 24問
        ("パーティーなどの賑やかな場では、周りのエネルギーを吸収して元気になる", "E-I", 1),
        ("深い思索にふける一人の時間こそが、自分にとっての休息だ", "E-I", -1),
        ("具体的な事実や、実際に起こった出来事を何よりも信頼する", "S-N", 1),
        ("物事の裏に隠された意味や、将来の可能性を想像するのが好きだ", "S-N", -1),
        ("議論の場では情に流されず、論理的に正しい決断を下すべきだ", "T-F", 1),
        ("理屈よりも、相手の感情や場の調和を優先することが多い", "T-F", -1),
        ("計画を立て、スケジュール通りに物事を進めるのが得意だ", "J-P", 1),
        ("締め切り直前のスリルや、即興の対応に楽しさを感じる", "J-P", -1),
        ("自分の能力に自信があり、ストレスを感じても立ち直りが早い", "A-T", 1),
        ("ささいな失敗でも深く反省し、自分を責めてしまいやすい", "A-T", -1),
        ("初対面の人ともすぐに打ち解け、会話を盛り上げることができる", "E-I", 1),
        ("信頼できる少数の友人と、深い対話をする方を好む", "E-I", -1),
        ("マニュアルや過去の経験を重視し、着実に実行したい", "S-N", 1),
        ("独創的なアイデアや、誰も試していない方法に挑戦したい", "S-N", -1),
        ("物事を客観的に分析し、公平な判断を下すことが得意だ", "T-F", 1),
        ("他者の苦しみに共感し、力になりたいと強く思う", "T-F", -1),
        ("整理整頓された環境にいると、心が落ち着き集中できる", "J-P", 1),
        ("自由でいたいので、あまり厳格なルールには縛られたくない", "J-P", -1),
        ("人からどう見られているかより、自分がどうあるかを重視する", "A-T", 1),
        ("周囲の期待に応えられているか、常に気になってしまう", "A-T", -1),
        ("大人数の前で話すことになっても、あまり緊張しない", "E-I", 1),
        ("自分の考えを他人に伝える前に、頭の中でじっくり練る", "E-I", -1),
        ("細部まで正確に作業することに誇りを持っている", "S-N", 1),
        ("大局的な視点で物事のコンセプトを捉えるのが得意だ", "S-N", -1),
        # 恋愛LCRO 8問
        ("恋愛において、自分が主導権を握ってリードしたい", "L-F", 1),
        ("パートナーの意思を尊重し、寄り添うサポート役が落ち着く", "L-F", -1),
        ("恋人には存分に甘え、子供のような一面も見せたい", "C-A", 1),
        ("恋人を力強く守り、包容力で包み込んであげたい", "C-A", -1),
        ("将来の生活基盤や経済力など、現実的な条件を重視する", "R-P", 1),
        ("情熱的な愛の言葉や、ドラマチックな展開に憧れる", "R-P", -1),
        ("恋人であっても適度な距離を保ち、自由な関係でいたい", "O-E", 1),
        ("交際するなら結婚を前提とした、誠実な付き合いが絶対だ", "O-E", -1),
    ]

    # --- 2. データベース (全16タイプ・完全データ) ---
    mbti_db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "best_match": "ENTP", "strength": "戦略的思考と独創性。", "trap": "他人に厳しすぎる。", "advice": "感情もデータの一部です。", "lucky_pool": ["戦略ゲーム", "難解な読書"], "love_basic": "知的な自立関係を好む"},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "best_match": "ENTJ", "strength": "客観的分析と自由な発想。", "trap": "行動が伴わない。", "advice": "まず形にしてみましょう。", "lucky_pool": ["パズル", "新しい知識の習得"], "love_basic": "個人の時間を尊重し合う"},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "best_match": "INTP", "strength": "圧倒的な決断力と統率力。", "trap": "威圧的になりがち。", "advice": "仲間の士気を気遣って。", "lucky_pool": ["高い所へ行く", "靴磨き"], "love_basic": "共に成長できる相手を選ぶ"},
        "ENTP": {"name": "討論者", "animal": "キツネ", "best_match": "INTJ", "strength": "機転とイノベーション。", "trap": "飽きっぽく刺激依存。", "advice": "完遂する忍耐を持って。", "lucky_pool": ["知らない駅で降りる", "逆転の発想"], "love_basic": "退屈しない刺激的な関係"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "best_match": "ENFJ", "strength": "深い洞察と揺るがぬ信念。", "trap": "自己犠牲で燃え尽きる。", "advice": "世界よりまず自分を救って。", "lucky_pool": ["キャンドル瞑想", "内省日記"], "love_basic": "魂の繋がりを重視する"},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "best_match": "ENFP", "strength": "豊かな感性と高い共感力。", "trap": "批判で深く傷つく。", "advice": "現実は理想を叶える舞台です。", "lucky_pool": ["詩を書く", "空の撮影"], "love_basic": "ロマンチックな純愛"},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "best_match": "INFJ", "strength": "カリスマ性と献身性。", "trap": "お節介が行き過ぎる。", "advice": "相手の自立も信じて。", "lucky_pool": ["友人に連絡", "ボランティア"], "love_basic": "相手の可能性を信じ抜く"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "best_match": "INFP", "strength": "社交性と明るい好奇心。", "trap": "集中力が散漫になる。", "advice": "一つのことを深掘りして。", "lucky_pool": ["カラオケ", "新しい服"], "love_basic": "運命の出会いを信じる"},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "best_match": "ESFJ", "strength": "実務能力と誠実さ。", "trap": "変化を拒みすぎる。", "advice": "新しいやり方も試して。", "lucky_pool": ["整理整頓", "時計の調整"], "love_basic": "安定した家庭を築く"},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "best_match": "ESTJ", "strength": "細やかな配慮と記憶力。", "trap": "NOと言えず抱え込む。", "advice": "自分を後回しにしないで。", "lucky_pool": ["料理", "リネンの洗濯"], "love_basic": "感謝を伝え合う穏やかな愛"},
        "ESTJ": {"name": "幹部", "animal": "番犬", "best_match": "ISFJ", "strength": "強い責任感と実行力。", "trap": "正論を押し付ける。", "advice": "相手の背景も聞いて。", "lucky_pool": ["筋トレ", "タスク消化"], "love_basic": "誠実で計画的な恋愛"},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "best_match": "ISTJ", "strength": "抜群の社交性と調整力。", "trap": "他人の評価に依存する。", "advice": "自分の価値は自分で決めて。", "lucky_pool": ["手土産を選ぶ", "お茶会"], "love_basic": "伝統や記念日を大切にする"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "best_match": "ESTP", "strength": "冷静な分析と道具の操作。", "trap": "言葉足らずで冷たい。", "advice": "意図を口に出して伝えて。", "lucky_pool": ["機械いじり", "ソロキャンプ"], "love_basic": "自立した一人の時間を好む"},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "best_match": "ESFP", "strength": "独自の美学と柔軟な心。", "trap": "計画性がなく流される。", "advice": "未来の自分への投資を。", "lucky_pool": ["美術館", "香水"], "love_basic": "心地よさと自由を愛する"},
        "ESTP": {"name": "起業家", "animal": "チーター", "best_match": "ISTP", "strength": "即興の行動力と交渉術。", "trap": "リスクを軽視しがち。", "advice": "一度止まって全体を見て。", "lucky_pool": ["スポーツ", "交渉事"], "love_basic": "スリルのあるダイナミックな恋"},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "best_match": "ISFP", "strength": "周囲を笑顔にする魅力。", "trap": "深刻な話を避ける。", "advice": "成長のための苦労も必要。", "lucky_pool": ["スイーツ巡り", "SNS投稿"], "love_basic": "毎日がお祭りのような関係"}
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 3. 画面表示 (端折らず、完璧に) ---
    if not st.session_state["show_result"]:
        st.title("性格32種×動物×恋愛LCRO 帝国診断")
        
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
        
        if st.button("診断結果を生成", use_container_width=True):
            if answered_count < len(questions):
                st.warning("すべての質問に回答してください。")
            else:
                st.session_state["show_result"] = True
                st.rerun()
    else:
        # --- 4. 計算ロジック (逆転項目・バイアス完全除去) ---
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, weight) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3) * weight

        def judge(val, pos, neg):
            if val > 0: return pos
            elif val < 0: return neg
            else: return random.choice([pos, neg])

        m_core = judge(scores["E-I"], "E", "I") + judge(scores["S-N"], "S", "N") + \
                 judge(scores["T-F"], "T", "F") + judge(scores["J-P"], "J", "P")
        at_suffix = judge(scores["A-T"], "A", "T")
        love_profile = judge(scores["L-F"], "L", "F") + judge(scores["C-A"], "C", "A") + \
                       judge(scores["R-P"], "R", "P") + judge(scores["O-E"], "O", "E")

        res = mbti_db.get(m_core)
        if "lucky_action" not in st.session_state:
            st.session_state["lucky_action"] = random.choice(res["lucky_pool"])

        # --- 5. 結果表示 (リッチなUIで) ---
        st.header(f"判定タイプ：{m_core}-{at_suffix}")
        st.subheader(f"恋愛コード：【 {love_profile} 型 】")
        st.markdown(f"### 動物タイプ：{res['animal']} ({res['name']})")
        st.success(f"🌟 **今週のラッキーアクション**\n\n「 {st.session_state['lucky_action']} 」")

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
            love_map = {"L":"リード派", "F":"フォロー派", "C":"甘え派", "A":"包容派", "R":"現実重視", "P":"情熱重視", "O":"楽観的", "E":"誠実重視"}
            meaning = " × ".join([love_map[c] for c in love_profile])
            st.write(f"**分析結果:** {meaning}")
            st.write(f"**基本姿勢:** {res['love_basic']}")
        with tab3:
            st.success(f"📌 **最高の相性：{res['best_match']}**")

        if st.button("再診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_imperial_ultimate_app()
