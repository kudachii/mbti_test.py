import streamlit as st
import plotly.graph_objects as go

def run_integrated_diagnostic():
    # --- 1. 質問データ (30問) ---
    # ※前回の30問ロジックを維持
    questions = [
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
        # --- 恋愛診断 6問 ---
        ("恋人の行動は、細かく把握しておきたい", "Love", 2),
        ("親しい間柄でも、礼儀や一定の距離感は必要だ", "Love", -1),
        ("相手の幸せが自分の幸せであり、何でもしてあげたい", "Love", 5),
        ("愛する人には、時には厳しい態度で接するのが愛だ", "Love", 1),
        ("恋人とは、精神的な深い部分で一体化したい", "Love", 3),
        ("恋愛において自分のプライドを傷つけられることは許せない", "Love", -1)
    ]

    # --- 2. 全16タイプ・完全データベース ---
    mbti_db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "catchphrase": "孤高の戦略家", "traits": "論理的で疑い深く、独自の戦略で目標を達成します。", "work": "戦略立案、システム設計、研究職。", "love_basic": "知的な刺激を求め、信頼を段階的に築きます。", "best_match": "ENTP（キツネ）"},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "catchphrase": "知的好奇心の探求者", "traits": "客観的な分析を好み、常に新しいアイデアを模索します。", "work": "プログラマー、数学者、哲学者。", "love_basic": "依存を嫌い、知的な対話を何より重視します。", "best_match": "ENTJ（ワシ）"},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "catchphrase": "不屈のリーダー", "traits": "強い意志と決断力で、周囲を目標へ導きます。", "work": "経営者、プロジェクトマネージャー、弁護士。", "love_basic": "切磋琢磨し合える、対等で強いパートナーを好みます。", "best_match": "INTP（チンパンジー）"},
        "ENTP": {"name": "討論者", "animal": "キツネ", "catchphrase": "変幻自在のアイデアマン", "traits": "常識を疑い、議論を通じて本質を見極める知性派です。", "work": "起業家、コンサルタント、広告プランナー。", "love_basic": "退屈を嫌い、常に新鮮な驚きを共有できる相手を求めます。", "best_match": "INTJ（トラ）"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "catchphrase": "静かな洞察者", "traits": "深い共感力と強い信念を持ち、理想を追求します。", "work": "カウンセラー、作家、教育者。", "love_basic": "精神的な一体感を求め、一度心を許すと一生尽くします。", "best_match": "ENFJ（ライオン）"},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "catchphrase": "優しき夢想家", "traits": "独自の価値観を持ち、感受性が豊かで利他的な性格です。", "work": "芸術家、心理士、NGO職員。", "love_basic": "ロマンチックで純粋な愛を信じ、理想の王子・王女を待ちます。", "best_match": "ENFP（カワウソ）"},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "catchphrase": "カリスマ的導き手", "traits": "他者の可能性を信じ、情熱的に周囲をサポートします。", "work": "コーチ、広報、非営利団体代表。", "love_basic": "尽くすことに喜びを感じ、調和のとれた関係を築きます。", "best_match": "INFJ（フクロウ）"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "catchphrase": "自由奔放な冒険家", "traits": "社交的で楽観的、新しい可能性を見つける天才です。", "work": "マーケター、イベント企画、ジャーナリスト。", "love_basic": "運命的な出会いを信じ、熱く情熱的に愛を伝えます。", "best_match": "INFP（ウサギ）"},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "catchphrase": "信頼の守護者", "traits": "実用的で事実に基づき行動し、義務を忠実に果たします。", "work": "公務員、会計士、エンジニア。", "love_basic": "安定感抜群。誠実で、長く続く家庭的な愛を育みます。", "best_match": "ESFJ（ゾウ）"},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "catchphrase": "献身的なサポーター", "traits": "周囲を温かく見守り、細やかな配慮で和を保ちます。", "work": "看護師、事務職、司書。", "love_basic": "相手のニーズを察するのが得意。一途で家庭的な愛を捧げます。", "best_match": "ESTJ（番犬）"},
        "ESTJ": {"name": "幹部", "animal": "番犬", "catchphrase": "秩序の司令塔", "traits": "現実的で組織をまとめる力が強く、公正さを重んじます。", "work": "警察官、財務担当、管理職。", "love_basic": "ルールと義務を大切にし、堅実な未来を共に歩む関係を好みます。", "best_match": "ISFJ（シカ）"},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "catchphrase": "心優しき世話役", "traits": "社交的で協調性が高く、他者のために積極的に行動します。", "work": "接客業、福祉、小学校教師。", "love_basic": "周囲からも祝福されるような、正統派で安定した愛を求めます。", "best_match": "ISTJ（ビーバー）"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "catchphrase": "冷静な実務家", "traits": "手先の器用さや技術を好み、危機に際しても冷静です。", "work": "整備士、パイロット、アスリート。", "love_basic": "自由を好み、束縛を嫌います。行動で愛情を示すタイプです。", "best_match": "ESTP（チーター）"},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "catchphrase": "感性の芸術家", "traits": "美的センスに優れ、今この瞬間を自由に生きることを好みます。", "work": "デザイナー、職人、音楽家。", "love_basic": "言葉より感性。お互いの自由を尊重し合える関係が理想です。", "best_match": "ESFP（レッサーパンダ）"},
        "ESTP": {"name": "起業家", "animal": "チーター", "catchphrase": "スリルを愛する行動派", "traits": "エネルギッシュで、目の前の問題に即座に対応します。", "work": "起業家、営業職、消防士。", "love_basic": "刺激と楽しさが最優先。飽きさせないダイナミックな関係を好みます。", "best_match": "ISTP（サメ）"},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "catchphrase": "人生を楽しむ達人", "traits": "社交的で人を喜ばせるのが大好き。常に周囲に活力を与えます。", "work": "俳優、添乗員、営業スタッフ。", "love_basic": "今を楽しもう！サプライズやイベントを好む情熱的なタイプです。", "best_match": "ISFP（ネコ）"},
    }

    # --- 3. メイン処理・UI ---
    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    if not st.session_state["show_result"]:
        st.title("性格・動物・恋愛 統合診断アプリ")
        st.write("全16タイプから、あなたの本質を精密に分析します。")
        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5], format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x], key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
        if st.button("診断結果を見る"):
            st.session_state["show_result"] = True
            st.rerun()
    else:
        # スコア集計
        scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0, "Love": 0}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        m_type = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        
        # 恋愛タイプ判定
        l_score = scores["Love"]
        if l_score >= 5: l_mode, l_name = "「真」の愛", "慈愛と包容力の人格者タイプ"
        elif l_score <= -1: l_mode, l_name = "「表」の愛", "気品と自律の高貴タイプ"
        else: l_mode, l_name = "「裏」の愛", "情熱と支配の情熱タイプ"

        detail = mbti_db.get(m_type)
        
        st.header(f"判定結果：{m_type} ({detail['name']})")
        st.subheader(f"動物タイプ：{detail['animal']}")
        st.info(f"**{detail['catchphrase']}**")

        tab1, tab2 = st.tabs(["基本性格分析", "恋愛深層診断"])
        with tab1:
            st.write(f"**特徴:** {detail['traits']}")
            st.write(f"**適職:** {detail['work']}")
        with tab2:
            st.write(f"**あなたの恋愛スタイル:** {l_mode}")
            st.markdown(f"**傾向:** {l_name}")
            st.write(f"**{detail['animal']}型の傾向:** {detail['love_basic']}")
            st.success(f"📌 **最高の相性:** {detail['best_match']}")

        if st.button("もう一度診断する"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_integrated_diagnostic()
