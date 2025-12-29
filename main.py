import streamlit as st
import plotly.graph_objects as go
import random

def run_mbti_diagnostic():
    # --- 1. 質問データ (24問) ---
    questions = [
        ("多人数で集まるイベントに参加すると元気が出る", "E-I", 1),
        ("自分の考えを整理するときは、誰かに話すより一人で考えたい", "E-I", -1),
        ("知らない人にも自分から話しかけるのは苦ではない", "E-I", 1),
        ("活動的な一日の後は、一人で静かに過ごす時間が必要だ", "E-I", -1),
        ("新しいアイデアより、すでに証明されているやり方を信頼する", "S-N", 1),
        ("空想より、現実的な問題解決に興味がある", "S-N", 1),
        ("物事の裏に隠された「意味」について考えるのが好きだ", "S-N", -1),
        ("詳細データより、インスピレーションを信じることが多い", "S-N", -1),
        ("決断を下す際、論理や効率を最も重視する", "T-F", 1),
        ("悩みを聞くとき、解決策を提示するよりまず気持ちに寄り添いたい", "T-F", -1),
        ("正論でも、誰かを傷つける可能性があるなら言葉を選ぶべきだ", "T-F", -1),
        ("誰かが間違っていたら、場の空気を壊してでも訂正すべきだと思う", "T-F", 1),
        ("やるべきことはリスト化して、一つずつ消していくのが好きだ", "J-P", 1),
        ("旅行に行くときは、予定を細かく決めずに動きたい", "J-P", -1),
        ("仕事や勉強は、締め切りギリギリにならないと本気が出ない", "J-P", -1),
        ("決まったルールやルーティンを守ることに安心感を覚える", "J-P", 1),
        ("注目を浴びる立場になることは、どちらかといえば好きだ", "E-I", 1),
        ("マニュアルがある場合、それを忠実に守る方だ", "S-N", 1),
        ("人から「共感力が高い」と言われるより「頭が良い」と言われたい", "T-F", 1),
        ("予期せぬトラブルにも臨機応変に対応することを楽しめる", "J-P", -1),
        ("ストレスを感じる状況でも、比較的冷静でいられる", "A-T", 1),
        ("過去の失敗をいつまでも悔やんでしまうことがある", "A-T", -1),
        ("自分の能力や決断に自信を持っている", "A-T", 1),
        ("他人の目が気になり、自分を過小評価してしまうことがある", "A-T", -1),
    ]

    # --- 2. メンターデータ ---
    mentor_data = {
        "ギャル先生": {
            "quote": "「おはよー！あんたの魅力、マジでバズり確定じゃん！✨ その調子で今日もハピネスに、自分軸でブチ上げてこー！💖」",
            "actions": ["「コンビニの新作スイーツ買って自分にご褒美あげちゃお！✨」", "「鏡の前で『今日も可愛いじゃん』って言ってみて？💖」", "「派手な色の小物を1つ身につけてみて！🌈」"]
        },
        "頼れるお姉さん": {
            "quote": "「一生懸命なところ、素敵よ。でもたまには肩の力を抜いて、私に甘えていいのよ？」",
            "actions": ["「5分だけデジタルデトックスをして温かい飲み物を。心の充電が必要よ。」", "「寝る前に頑張ったことを3つ思い出して自分を褒めてあげてね。」", "「ゆっくりお風呂に浸かって、好きな香りの入浴剤を楽しんでみて。」"]
        },
        "カサネ・イズミ：論理と不確定要素": {
            "quote": "「あなたのデータは極めて特異だ。その思考を最適化すれば、さらなる高みへ到達できる。」",
            "actions": ["「デスクの上を完全に片付けろ。視覚的なノイズを排除しろ。」", "「今日学んだことを3行でメモしろ。知識の定着こそが力だ。」", "「タスクの優先順位を見直し、重要度の低いものを1つ捨てろ。」"]
        },
        "ツンデレな指導員": {
            "quote": "「ふん、あんたみたいなタイプは私が付いてないと危なっかしいわね。しっかりしなさいよ！」",
            "actions": ["「姿勢を正しなさい！背筋を伸ばしなさい！それだけで印象が変わるんだから。」", "「たまには自分を甘やかしなさいよね。ずっと頑張りすぎなのよ…心配してないわよ！」", "「今日は10分早く寝なさい。明日寝坊して困るのはあんたなんだからね！」"]
        },
        "論理的なビジネスコーチ": {
            "quote": "「あなたの能力を最大限に活かすための戦略を練ろう。まずは現状の分析からだ。」",
            "actions": ["「今日一番の重要課題を1つ決めて、それに集中しよう。」", "「明日のスケジュールを今夜のうちに10分で見直しておこう。」", "「身の回りのものを1つだけ新調してみよう。小さな変化が刺激になる。」"]
        },
        "優しさに溢れるメンター (Default)": {
            "quote": "「あなたは今のままで十分素晴らしいですよ。一緒に、一歩ずつ進んでいきましょうね。」",
            "actions": ["「深呼吸をゆっくり3回しましょう。」", "「重要な決断は明日の朝にしましょう。」", "「散歩をしながら空を眺めてみてください。」"]
        }
    }

    # --- 3. MBTI DB ---
    mbti_db = {
        "ISTJ": {"name": "管理者", "animal": "勤勉なビーバー", "catchphrase": "「一歩ずつ、確実に。信頼を築き上げる職人」", "strength": "責任感、精密な作業", "weakness": "変化への抵抗", "mentor": "論理的なビジネスコーチ", "details": {"work": "マニュアル遵守", "love": "誠実一途", "stress": "細かいミスに固執", "best_match": "お世話好きなゾウ（ESFJ）"}, "messages": {"ギャル先生": "ビーバーちゃん、マジメすぎ！たまには羽目外そ！✨"}},
        "ISFJ": {"name": "擁護者", "animal": "穏やかなシカ", "catchphrase": "「静かな優しさで、みんなの心に灯をともす」", "strength": "神配慮、誠実", "weakness": "自己犠牲", "mentor": "優しさに溢れるメンター (Default)", "details": {"work": "サポーター", "love": "献身的", "stress": "過度な悲観", "best_match": "誠実な番犬（ESTJ）"}, "messages": {"ギャル先生": "シカちゃん、今日はあんたが主役だよ！💖"}},
        "INFJ": {"name": "提唱者", "animal": "思慮深いフクロウ", "catchphrase": "「夜の静寂の中で、未来の光を見通す賢者」", "strength": "洞察力、カリスマ性", "weakness": "理想への絶望", "mentor": "頼れるお姉さん", "details": {"work": "リーダー", "love": "深い精神的繋がり", "stress": "感覚過敏", "best_match": "情熱的なライオン（ENFJ）"}, "messages": {"ギャル先生": "フクロウちゃん、リスペクト！🌈"}},
        "INTJ": {"name": "建築家", "animal": "孤高のトラ", "catchphrase": "「誰にも媚びず、己の知略で世界を再構築する」", "strength": "戦略的思考、実行力", "weakness": "感情への無関心", "mentor": "カサネ・イズミ：論理と不確定要素", "details": {"work": "軍師", "love": "知的な刺激", "stress": "現実逃避", "best_match": "独創的なキツネ（ENTP）"}, "messages": {"ギャル先生": "トラさん、クールすぎ！その最強頭脳で世界回そ！🔥"}},
        "ISTP": {"name": "巨匠", "animal": "冷静なサメ", "catchphrase": "「乱世をクールに泳ぎ、一瞬の好機を逃さない」", "strength": "解決力、適応力", "weakness": "無関心", "mentor": "ツンデレな指導員", "details": {"work": "一匹狼プロ", "love": "距離感重視", "stress": "感情爆発", "best_match": "勇敢なチーター（ESTP）"}, "messages": {"ギャル先生": "サメちゃん、自由で最高！センス神！✨"}},
        "ISFP": {"name": "冒険家", "animal": "自由なネコ", "catchphrase": "「自分の『好き』を呼吸するように生きる芸術家」", "strength": "美的センス、寛容", "weakness": "批判に弱い", "mentor": "ギャル先生", "details": {"work": "感性重視", "love": "雰囲気重視", "stress": "自信喪失", "best_match": "陽気なレッサーパンダ（ESFP）"}, "messages": {"ギャル先生": "ネコちゃん、感性ヤバすぎ！貫いちゃえ！🐾"}},
        "INFP": {"name": "仲介者", "animal": "理想を夢見るウサギ", "catchphrase": "「傷つくことを恐れず、愛と優しさを信じ続ける」", "strength": "表現力、誠実", "weakness": "実務放置", "mentor": "頼れるお姉さん", "details": {"work": "独自の価値観", "love": "ロマンチック", "stress": "現実への攻撃", "best_match": "天真爛漫なカワウソ（ENFP）"}, "messages": {"ギャル先生": "ウサギちゃん、優しさ神！応援してるよ！🐰"}},
        "INTP": {"name": "論理学者", "animal": "探求するチンパンジー", "catchphrase": "「常識を疑い、知の迷宮を楽しむ知的な探検家」", "strength": "抽象化、真理探究", "weakness": "実行の遅れ", "mentor": "カサネ・イズミ：論理と不確定要素", "details": {"work": "天才分析官", "love": "知的パートナー", "stress": "感情オーバーフロー", "best_match": "威風堂々なワシ（ENTJ）"}, "messages": {"ギャル先生": "パンジーくん、天才すぎ！バズるよ！🚀"}},
        "ESTP": {"name": "起業家", "animal": "勇敢なチーター", "catchphrase": "「考える前に跳べ。世界を遊び場に変える開拓者」", "strength": "スピード、突破力", "weakness": "スリル依存", "mentor": "ツンデレな指導員", "details": {"work": "トラブルシューター", "love": "情熱的", "stress": "無謀な暴走", "best_match": "冷静なサメ（ISTP）"}, "messages": {"ギャル先生": "チーターくん、爆速すぎ！ブチ上げてこー！🐆✨"}},
        "ESFP": {"name": "エンターテイナー", "animal": "陽気なレッサーパンダ", "catchphrase": "「一瞬で場を彩る、愛されキャラの天才」", "strength": "空間作り、好奇心", "weakness": "孤独への不安", "mentor": "ギャル先生", "details": {"work": "ムードメーカー", "love": "楽しさ最優先", "stress": "被害妄想", "best_match": "自由なネコ（ISFP）"}, "messages": {"ギャル先生": "パンダちゃん、最高にハッピー！アゲてこ！🐼💖"}},
        "ENFP": {"name": "広報運動家", "animal": "天真爛漫なカワウソ", "catchphrase": "「無限のワクワクを撒き散らす、愛の伝道師」", "strength": "コミュ力、レジリエンス", "weakness": "中途半端", "mentor": "ギャル先生", "details": {"work": "クリエイター", "love": "運命派", "stress": "強迫観念", "best_match": "理想を夢見るウサギ（INFP）"}, "messages": {"ギャル先生": "カワウソちゃん、ワクワク全開！冒険しよ！🦦"}},
        "ENTP": {"name": "討論者", "animal": "独創的なキツネ", "catchphrase": "「知的なイタズラで、退屈な世界に風穴を開ける」", "strength": "交渉術、逆境に強い", "weakness": "論破摩擦", "mentor": "ツンデレな指導員", "details": {"work": "イノベーター", "love": "知的駆け引き", "stress": "些細な執着", "best_match": "孤高のトラ（INTJ）"}, "messages": {"ギャル先生": "キツネくん、天才！常識ブチ壊そ！🦊🔥"}},
        "ESTJ": {"name": "幹部", "animal": "誠実な番犬", "catchphrase": "「揺るぎない正義感で、秩序と平和を守り抜く」", "strength": "規律、司令塔", "weakness": "独断的否定", "mentor": "論理的なビジネスコーチ", "details": {"work": "完璧リーダー", "love": "将来設計", "stress": "孤独涙もろい", "best_match": "穏やかなシカ（ISFJ）"}, "messages": {"ギャル先生": "ワンちゃん、リーダーシップマジリスペクト！🐕"}},
        "ESFJ": {"name": "領事", "animal": "お世話好きなゾウ", "catchphrase": "「大きな愛でみんなを包む、コミュニティの守護神」", "strength": "場作り、献身", "weakness": "お節介", "mentor": "優しさに溢れるメンター (Default)", "details": {"work": "守護者", "love": "家庭的", "stress": "理屈批判", "best_match": "勤勉なビーバー（ISTJ）"}, "messages": {"ギャル先生": "ゾウさん、優しさMAX！いつもありがと！🐘💖"}},
        "ENFJ": {"name": "主人公", "animal": "情熱的なライオン", "catchphrase": "「みんなの可能性を信じ、光差す方へ導く太陽」", "strength": "才能開花、火付け役", "weakness": "過度な責任感", "mentor": "頼れるお姉さん", "details": {"work": "導き手", "love": "理想のペア", "stress": "批判に沈む", "best_match": "思慮深いフクロウ（INFJ）"}, "messages": {"ギャル先生": "ライオンくん、情熱ヤバい！救われるよ！🦁✨"}},
        "ENTJ": {"name": "指揮官", "animal": "威風堂々なワシ", "catchphrase": "「高みから未来を見据え、勝利への最短距離を飛ぶ」", "strength": "決断力、目標達成", "weakness": "成果なき者への容赦", "mentor": "論理的なビジネスコーチ", "details": {"work": "指揮官", "love": "切磋琢磨", "stress": "情緒不安定", "best_match": "探求するチンパンジー（INTP）"}, "messages": {"ギャル先生": "ワシさん、最強リーダー！世界征服しよー！🦅🔥"}}
    }

    # --- 4. セッション状態の管理 ---
    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False
    if "run_count" not in st.session_state:
        st.session_state["run_count"] = 0

    # --- 5. 画面切り替え ---

    # 【A】質問モード
    if not st.session_state["show_result"]:
        st.title("性格診断クエスト 🐾")
        
        # 進捗計算
        answered_count = 0
        for i in range(len(questions)):
            if f"q_{i}_{st.session_state['run_count']}" in st.session_state:
                answered_count += 1
        
        with st.sidebar:
            st.header("📊 診断の進捗")
            progress = answered_count / len(questions)
            st.progress(progress)
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
            st.divider()
            st.markdown("**ギャル先生からの応援**")
            if progress < 0.5: st.write("「まずは直感でポチポチいこー！✨」")
            elif progress < 1.0: st.write("「いい感じ！半分超えたよ！🔥」")
            else: st.write("「完璧！あんたマジ最高！💖」")

        # 質問を表示（コンテナで囲んでリセット対応）
        with st.container():
            for i, (q_text, axis, weight) in enumerate(questions):
                st.markdown(f"**Q{i+1}. {q_text}**")
                st.radio(
                    f"radio_{i}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                    key=f"q_{i}_{st.session_state['run_count']}", 
                    label_visibility="collapsed", horizontal=True, index=2
                )
                st.write("---")

        if st.button("診断結果を詳しく見る ✨", use_container_width=True):
            if answered_count < len(questions):
                st.error(f"まだ回答していない質問があるよ！（残り {len(questions) - answered_count} 問）")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    # 【B】結果表示モード
    else:
        st.balloons()
        
        # スコア計算
        scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0}
        for i, (_, axis, weight) in enumerate(questions):
            val = st.session_state.get(f"q_{i}_{st.session_state['run_count']}", 3)
            scores[axis] += (val - 3) * weight

        # タイプ判定
        m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        full_res = m_core + ("-A" if scores["A-T"] >= 0 else "-T")
        detail = mbti_db.get(m_core, mbti_db["ISTJ"])

        st.markdown(f"## 判定結果：{full_res}")
        st.markdown(f"### あなたを動物に例えると… 『 {detail['animal']} 』")
        st.info(f"**{detail['catchphrase']}**")

        tab1, tab2, tab3, tab4 = st.tabs(["💼 仕事・勉強", "💖 人間関係", "💀 裏の顔", "🤝 相性"])
        with tab1: st.write(f"**スタイル：**\n\n{detail['details']['work']}")
        with tab2: st.write(f"**コミュニケーション：**\n\n{detail['details']['love']}")
        with tab3: st.warning(f"**ストレス時：**\n\n{detail['details']['stress']}")
        with tab4: st.info(f"**最高の相性：**\n\n{detail['details']['best_match']}")

        # チャート
        st.divider()
        categories = ['外向(E)', '感覚(S)', '思考(T)', '判断(J)', '自己主張(A)']
        values = [scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-12, 12])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # メンターセクション
        st.markdown("### 🤝 今日のメンターを指名")
        selected_mentor = st.selectbox("指名する", options=list(mentor_data.keys()), index=0)
        m_info = mentor_data[selected_mentor]
        msg = detail["messages"].get(selected_mentor, m_info["quote"])
        st.chat_message("assistant").write(f"**{selected_mentor}**：「{msg}」")
        st.success(f"🎁 **今日のラッキーアクション**：{random.choice(m_info['actions'])}")

        # 保存機能
        report = f"判定結果: {full_res}\n動物: {detail['animal']}\nキャッチフレーズ: {detail['catchphrase']}"
        st.download_button("診断結果をダウンロード 📥", report, file_name=f"MBTI_{full_res}.txt", use_container_width=True)

        # 🔄 やり直しボタン（ここでリセット）
        st.divider()
        if st.button("🔄 最初からやり直す", use_container_width=True):
            # すべて消して最初に戻る
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_mbti_diagnostic()
