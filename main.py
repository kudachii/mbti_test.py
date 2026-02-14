import streamlit as st
import plotly.graph_objects as go

def run_integrated_diagnostic():
    # --- 1. 質問データ (計30問) ---
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
        # --- [恋愛診断軸: 6問] ---
        ("恋人の行動は、細かく把握しておきたい", "Love", 2),
        ("親しい間柄でも、礼儀や一定の距離感は必要だ", "Love", -1),
        ("相手の幸せが自分の幸せであり、何でもしてあげたい", "Love", 5),
        ("愛する人には、時には厳しい態度で接するのが愛だ", "Love", 1),
        ("恋人とは、精神的な深い部分で一体化したい", "Love", 3),
        ("恋愛において自分のプライドを傷つけられることは許せない", "Love", -1)
    ]

    # --- 2. 16タイプ・動物性格・恋愛 統合データベース ---
    mbti_db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "catchphrase": "孤高の戦略家", "traits": "論理的で疑い深く、独自の戦略で目標を達成します。高い独立心を持ちます。", "work": "戦略立案、システム設計、研究職、経営コンサルタント。", "love_basic": "知的な刺激を求め、信頼を段階的に築きます。長期的な視点を重視します。", "best_match": "ENTP（キツネ）"},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "catchphrase": "知的好奇心の探求者", "traits": "客観的な分析を好み、常に新しいアイデアや仕組みを模索します。", "work": "プログラマー、数学者、哲学者、データサイエンティスト。", "love_basic": "依存を嫌い、知的な対話を何より重視します。自由を必要とします。", "best_match": "ENTJ（ワシ）"},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "catchphrase": "不屈のリーダー", "traits": "強い意志と決断力で、周囲を目標へ導きます。効率と成果を最優先します。", "work": "経営者、プロジェクトマネージャー、弁護士、政治家。", "love_basic": "切磋琢磨し合える、対等で強いパートナーを好みます。", "best_match": "INTP（チンパンジー）"},
        "ENTP": {"name": "討論者", "animal": "キツネ", "catchphrase": "変幻自在のアイデアマン", "traits": "常識を疑い、議論を通じて本質を見極める知性派。好奇心が旺盛です。", "work": "起業家、コンサルタント、広告プランナー、ディレクター。", "love_basic": "退屈を嫌い、常に新鮮な驚きを共有できる相手を求めます。", "best_match": "INTJ（トラ）"},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "catchphrase": "静かな洞察者", "traits": "深い共感力と強い信念を持ち、理想を追求します。他者の成長を願います。", "work": "カウンセラー、作家、教育者、心理療法士。", "love_basic": "精神的な一体感を求め、一度心を許すと一生尽くす誠実さを持ちます。", "best_match": "ENFJ（ライオン）"},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "catchphrase": "優しき夢想家", "traits": "独自の価値観を持ち、感受性が豊かで利他的。自己表現を大切にします。", "work": "芸術家、心理士、NGO職員、クリエイター。", "love_basic": "ロマンチックで純粋な愛を信じ、お互いの感性を尊重し合いたいと考えます。", "best_match": "ENFP（カワウソ）"},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "catchphrase": "カリスマ的導き手", "traits": "他者の可能性を信じ、情熱的に周囲をサポート。高い社交性を持ちます。", "work": "コーチ、広報、非営利団体代表、人事担当。", "love_basic": "尽くすことに喜びを感じ、情緒的な調和のとれた関係を築きます。", "best_match": "INFJ（フクロウ）"},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "catchphrase": "自由奔放な冒険家", "traits": "社交的で楽観的、新しい可能性を見つける天才。人々を鼓舞します。", "work": "マーケター、イベント企画、ジャーナリスト、デザイナー。", "love_basic": "運命的な出会いを信じ、熱く情熱的に愛を伝えます。", "best_match": "INFP（ウサギ）"},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "catchphrase": "信頼の守護者", "traits": "実用的で事実に基づき行動。義務を忠実に果たし、秩序を重んじます。", "work": "公務員、会計士、エンジニア、法執行官。", "love_basic": "安定感抜群。誠実で、長く続く家庭的な愛を育みます。", "best_match": "ESFJ（ゾウ）"},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "catchphrase": "献身的なサポーター", "traits": "周囲を温かく見守り、細やかな配慮で和を保ちます。責任感が強いです。", "work": "看護師、事務職、司書、ソーシャルワーカー。", "love_basic": "相手のニーズを察するのが得意。一途で献身的な愛を捧げます。", "best_match": "ESTJ（番犬）"},
        "ESTJ": {"name": "幹部", "animal": "番犬", "catchphrase": "秩序の司令塔", "traits": "現実的で組織をまとめる力が強く、公正さと伝統を重んじます。", "work": "警察官、財務担当、管理職、軍関係者。", "love_basic": "ルールと義務を大切にし、堅実な未来を共に歩む関係を好みます。", "best_match": "ISFJ（シカ）"},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "catchphrase": "心優しき世話役", "traits": "社交的で協調性が高く、他者のために積極的に行動。調和を愛します。", "work": "接客業、福祉、小学校教師、営業職。", "love_basic": "周囲からも祝福されるような、正統派で安定した愛を求めます。", "best_match": "ISTJ（ビーバー）"},
        "ISTP": {"name": "巨匠", "animal": "サメ", "catchphrase": "冷静な実務家", "traits": "手先の器用さや技術を好み、危機に際しても冷静に解決策を導きます。", "work": "整備士、パイロット、アスリート、システムエンジニア。", "love_basic": "自由を好み、束縛を嫌います。行動で愛情を示すタイプです。", "best_match": "ESTP（チーター）"},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "catchphrase": "感性の芸術家", "traits": "美的センスに優れ、今この瞬間を自由に生きる。柔軟な感性を持ちます。", "work": "デザイナー、職人、音楽家、イラストレーター。", "love_basic": "言葉より感性。お互いの自由を尊重し合える関係が理想です。", "best_match": "ESFP（レッサーパンダ）"},
        "ESTP": {"name": "起業家", "animal": "チーター", "catchphrase": "スリルを愛する行動派", "traits": "エネルギッシュで、目の前の問題に即座に対応。常に動き回っています。", "work": "起業家、営業職、消防士、株式トレーダー。", "love_basic": "刺激と楽しさが最優先。飽きさせないダイナミックな関係を好みます。", "best_match": "ISTP（サメ）"},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "catchphrase": "人生を楽しむ達人", "traits": "社交的で人を喜ばせるのが大好き。常に周囲に活力を与え、場を盛り上げます。", "work": "俳優、添乗員、営業スタッフ、広報職。", "love_basic": "今を楽しもう！サプライズやイベントを好む情熱的なタイプです。", "best_match": "ISFP（ネコ）"},
    }

    # --- 3. セッション管理 ---
    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 4. 診断画面 ---
    if not st.session_state["show_result"]:
        st.title("性格・動物・恋愛 統合診断 🐾")
        
        answered_count = sum(1 for i in range(len(questions)) if st.session_state.get(f"q_{i}") is not None)
        progress = answered_count / len(questions)

        # サイドバー進捗
        with st.sidebar:
            st.header("📊 診断の進捗")
            st.progress(progress)
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
            st.divider()
            if answered_count == len(questions):
                st.success("全ての質問に回答しました！")
            else:
                st.info("直感で回答を進めてください。")

        # 質問表示
        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                    key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
            st.write("---")

        if st.button("診断結果を算出する", use_container_width=True):
            if answered_count < len(questions):
                st.warning(f"まだ未回答の質問があります。（残り {len(questions) - answered_count} 問）")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    else:
        # --- 5. 結果表示 ---
        scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0, "Love": 0}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        m_type = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        
        # 恋愛タイプ
        l_score = scores["Love"]
        if l_score >= 5: l_mode, l_name = "「真」人格者の愛", "自己犠牲を厭わない深い慈愛。相手を包み込み、共に成長するタイプ。"
        elif l_score <= -1: l_mode, l_name = "「表」高貴な愛", "プライドと品格を重んじる。理想が高く、自律した関係を好むタイプ。"
        else: l_mode, l_name = "「裏」情熱の愛", "独占欲や執着が愛の証。相手と濃密に深く関わりたいタイプ。"

        detail = mbti_db.get(m_type)
        
        st.header(f"判定タイプ：{m_type} ({detail['name']})")
        st.subheader(f"動物タイプ：{detail['animal']}")
        st.info(f"**{detail['catchphrase']}**")

        # レーダーチャート
        categories = ['外向性(E)', '直感性(N)', '感情型(F)', '柔軟性(P)', '自己主張(A)']
        # 反転軸を考慮して可視化用の値を調整
        plot_values = [scores["E-I"], -scores["S-N"], -scores["T-F"], -scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=plot_values, theta=categories, fill='toself', name='特性スコア'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-10, 10])), showlegend=False, title="性格特性レーダーチャート")
        st.plotly_chart(fig, use_container_width=True)

        tab1, tab2, tab3 = st.tabs(["🧬 性格・適職分析", "💖 恋愛深層診断", "🤝 相性アドバイス"])
        
        with tab1:
            st.markdown(f"**【特性】**\n{detail['traits']}")
            st.markdown(f"**【適職の傾向】**\n{detail['work']}")
        
        with tab2:
            st.markdown(f"**あなたのラブタイプ：{l_mode}**")
            st.write(l_name)
            st.divider()
            st.write(f"**{detail['name']}としての恋愛傾向:** {detail['love_basic']}")
        
        with tab3:
            st.success(f"📌 **最高の相性：{detail['best_match']}**")
            st.write("このタイプとは、価値観や行動パターンが互いを補完し合い、非常にスムーズな関係を築きやすいでしょう。")

        if st.button("最初からやり直す", use_container_width=True):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_integrated_diagnostic()
