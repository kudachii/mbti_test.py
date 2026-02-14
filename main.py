import streamlit as st
import plotly.graph_objects as go

def run_integrated_diagnostic():
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
        ("効率が悪くても、全員が納得するまで話し合うべきだ", "T-F", -1),
        ("締め切りや予定は厳守し、計画通りに進むと安心する", "J-P", 1),
        ("その場の状況に合わせて柔軟に予定を変える方が好きだ", "J-P", -1),
        ("整理整頓が得意で、身の回りは常に整っている方だ", "J-P", 1),
        ("ギリギリまで選択肢を残しておきたいタイプだ", "J-P", -1),
        ("人からどう見られているか、あまり気にならない", "A-T", 1),
        ("失敗すると長く落ち込みやすく、自分を責めてしまう", "A-T", -1),
        ("自分自身の能力に自信を持っており、将来を楽観視している", "A-T", 1),
        ("周囲の環境変化に対して、敏感にストレスを感じやすい", "A-T", -1),
        ("マニュアルよりも自分の経験を信じる", "S-N", 1),
        ("感情を表に出すのは苦手な方だ", "T-F", 1),
        ("予期せぬトラブルには臨機応変に対応するのが得意だ", "J-P", -1),
        ("一人でいると寂しさを感じ、誰かと繋がっていたい", "E-I", 1),
        # --- [恋愛4軸プロファイル: 8問] ---
        ("デートの計画やリードは、相手に任せたい", "L-F", -1), # Lead / Follow
        ("自分の生活ペースを乱されるのはストレスを感じる", "L-F", 1),
        ("恋人には自分から甘えるよりも、甘えられたり頼られたりしたい", "C-A", -1), # Cuddly / Accept
        ("信頼できるパートナーには、とことん甘やかしてほしい", "C-A", 1),
        ("恋愛においても、経済力や生活能力などの現実面をシビアにチェックする", "R-P", 1), # Realistic / Passionate
        ("一度恋に落ちたら、周囲の声が届かないほど情熱的にのめり込む", "R-P", -1),
        ("お互いに束縛せず、自由でライトな関係性を好む", "O-E", 1), # Optimistic / Earnest
        ("交際するなら結婚や将来を視野に入れた、誠実な付き合いが当然だ", "O-E", -1),
    ]

    # --- 2. 16タイプ完全データベース ---
    mbti_db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "catchphrase": "孤高の戦略家", "traits": "論理的で疑い深く、独自の戦略で目標を達成します。", "work": "戦略立案、システム設計、研究職。", "love_basic": "知的な刺激を求め、信頼を段階的に築きます。", "best_match": "ENTP（キツネ）"},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "catchphrase": "知的好奇心の探求者", "traits": "客観的な分析を好み、常に新しいアイデアを模索します。", "work": "プログラマー、数学者、データ分析。", "love_basic": "依存を嫌い、知的な対話を何より重視します。", "best_match": "ENTJ（ワシ）"},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "catchphrase": "不屈のリーダー", "traits": "強い意志と決断力で、周囲を目標へ導きます。", "work": "経営者、マネージャー、弁護士。", "love_basic": "切磋琢磨し合える、対等で強いパートナーを好みます。", "best_match": "INTP（チンパンジー）"},
        "ENTP": {"name": "討論者", "animal": "キツネ", "catchphrase": "変幻自在のアイデアマン", "traits": "常識を疑い、議論を通じて本質を見極める知性派です。", "work": "起業家、コンサルタント、広告プランナー。", "love_basic": "退屈を嫌い、常に新鮮な驚きを共有できる相手を求めます。", "best_match": "INTJ（トラ）"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "catchphrase": "静かな洞察者", "traits": "深い共感力と強い信念を持ち、理想を追求します。", "work": "カウンセラー、作家、心理療法士。", "love_basic": "精神的な一体感を求め、一度心を許すと一生尽くします。", "best_match": "ENFJ（ライオン）"},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "catchphrase": "優しき夢想家", "traits": "独自の価値観を持ち、感受性が豊かで利他的な性格です。", "work": "芸術家、心理士、クリエイター。", "love_basic": "純粋な愛を信じ、お互いの感性を尊重し合いたいと考えます。", "best_match": "ENFP（カワウソ）"},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "catchphrase": "カリスマ的導き手", "traits": "他者の可能性を信じ、情熱的に周囲をサポートします。", "work": "コーチ、広報、人事担当。", "love_basic": "尽くすことに喜びを感じ、情緒的な調和を築きます。", "best_match": "INFJ（フクロウ）"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "catchphrase": "自由奔放な冒険家", "traits": "社交的で楽観的、新しい可能性を見つける天才です。", "work": "マーケター、イベント企画、デザイナー。", "love_basic": "運命的な出会いを信じ、熱く情熱的に愛を伝えます。", "best_match": "INFP（ウサギ）"},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "catchphrase": "信頼の守護者", "traits": "実用的で事実に基づき行動し、義務を忠実に果たします。", "work": "公務員、会計士、エンジニア。", "love_basic": "誠実で、長く続く家庭的な愛を育みます。", "best_match": "ESFJ（ゾウ）"},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "catchphrase": "献身的なサポーター", "traits": "周囲を温かく見守り、細やかな配慮で和を保ちます。", "work": "看護師、事務職、司書。", "love_basic": "相手のニーズを察するのが得意。一途な愛を捧げます。", "best_match": "ESTJ（番犬）"},
        "ESTJ": {"name": "幹部", "animal": "番犬", "catchphrase": "秩序の司令塔", "traits": "現実的で組織をまとめる力が強く、公正さを重んじます。", "work": "管理職、警察官、財務担当。", "love_basic": "誠実さと規律を大切にし、堅実な未来を歩みます。", "best_match": "ISFJ（シカ）"},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "catchphrase": "心優しき世話役", "traits": "社交的で協調性が高く、他者のために積極的に行動します。", "work": "接客業、福祉、小学校教師。", "love_basic": "周囲からも祝福されるような、安定した愛を求めます。", "best_match": "ISTJ（ビーバー）"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "catchphrase": "冷静な実務家", "traits": "手先の器用さや技術を好み、危機に際しても冷静です。", "work": "整備士、パイロット、アスリート。", "love_basic": "自由を好み、束縛を嫌います。行動で愛情を示します。", "best_match": "ESTP（チーター）"},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "catchphrase": "感性の芸術家", "traits": "美的センスに優れ、今この瞬間を自由に生きることを好みます。", "work": "デザイナー、職人、音楽家。", "love_basic": "言葉より感性。お互いの自由を尊重する関係が理想です。", "best_match": "ESFP（レッサーパンダ）"},
        "ESTP": {"name": "起業家", "animal": "チーター", "catchphrase": "スリルを愛する行動派", "traits": "エネルギッシュで、目の前の問題に即座に対応します。", "work": "起業家、営業職、消防士。", "love_basic": "刺激と楽しさが最優先。ダイナミックな関係を好みます。", "best_match": "ISTP（サメ）"},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "catchphrase": "人生を楽しむ達人", "traits": "社交的で人を喜ばせるのが大好き。場を盛り上げます。", "work": "俳優、添乗員、営業スタッフ。", "love_basic": "サプライズやイベントを好む情熱的なタイプです。", "best_match": "ISFP（ネコ）"},
    }

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("性格・動物・恋愛 統合精密診断")
        
        # サイドバー進捗
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        progress = answered_count / len(questions)
        with st.sidebar:
            st.header("📊 診断進捗")
            st.progress(progress)
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")

        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                    key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")

        if st.button("診断結果を表示", use_container_width=True):
            if answered_count < len(questions):
                st.warning("すべての質問に回答してください。")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 結果表示 ---
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        m_type = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        
        detail = mbti_db.get(m_type)
        st.header(f"結果：{m_type} ({detail['name']})")
        st.subheader(f"動物タイプ：{detail['animal']}")
        st.info(f"**{detail['catchphrase']}**")

        # レーダーチャート
        categories = ['外向性(E)', '直感性(N)', '感情型(F)', '柔軟性(P)', '自己主張(A)']
        plot_values = [scores["E-I"], -scores["S-N"], -scores["T-F"], -scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=plot_values, theta=categories, fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-6, 6])), showlegend=False)
        st.plotly_chart(fig)

        tab1, tab2, tab3 = st.tabs(["🧬 性格・適職", "💖 恋愛プロファイル", "🤝 相性"])
        
        with tab1:
            st.write(f"**【特徴】**\n{detail['traits']}")
            st.write(f"**【適職】**\n{detail['work']}")

        with tab2:
            st.subheader("恋愛詳細プロファイル")
            love_axes = [
                ("Lead / Follow", "相手に合わせたい", "自分で進めたい", "L-F"),
                ("Cuddly / Accept", "甘えられたい", "甘えたい", "C-A"),
                ("Realistic / Passionate", "情熱的・直感的", "現実的・打算的", "R-P"),
                ("Optimistic / Earnest", "真面目・誠実", "自由・楽観的", "O-E")
            ]
            for label, left, right, axis in love_axes:
                st.write(f"**{label}**")
                val = scores[axis]
                # -4から4の範囲を0-100にスケーリング
                progress_val = (val + 4) / 8
                cols = st.columns([2, 6, 2])
                cols[0].write(left)
                cols[1].progress(min(max(progress_val, 0.0), 1.0))
                cols[2].write(right)
            st.divider()
            st.write(f"**{detail['name']}型の恋愛傾向:**\n{detail['love_basic']}")

        with tab3:
            st.success(f"📌 **最高の相性：{detail['best_match']}**")

        if st.button("再診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_integrated_diagnostic()
