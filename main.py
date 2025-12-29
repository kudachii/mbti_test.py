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
        "ISTJ": {
            "name": "管理者", "animal": "勤勉なビーバー", 
            "catchphrase": "「一歩ずつ、確実に。信頼を築き上げる職人」",
            "mentor": "論理的なビジネスコーチ",
            "details": {
                "work": "マニュアルや手順を完璧に守り、ミスなく成果を出す『組織の柱』。締め切りは絶対守る派。",
                "love": "超誠実で一途。記念日を忘れず、安定した関係を築くけど、変化やサプライズはちょっと苦手。",
                "stress": "普段の冷静さを失い、細かいミスに固執してパニックに。自分を責めすぎて負のループへ。",
                "best_match": "お世話好きなゾウ（ESFJ）"
            },
            "messages": {"ギャル先生": "ビーバーちゃん、マジメすぎ！たまには羽目外そ！✨"}
        },
        "ISFJ": {
            "name": "擁護者", "animal": "穏やかなシカ", 
            "catchphrase": "「静かな優しさで、みんなの心に灯をともす」",
            "mentor": "優しさに溢れるメンター (Default)",
            "details": {
                "work": "他人のニーズを察して先回りする『最高のサポーター』。縁の下の力持ちとして評価されるわ。",
                "love": "献身的に尽くすタイプ。相手の喜びが自分の喜びだけど、不満を溜め込みすぎて爆発することも。",
                "stress": "『自分なんて必要ないんだ』と思い込み、過剰に悲観的に。体調にもすぐ出ちゃうから注意！",
                "best_match": "誠実な番犬（ESTJ）"
            },
            "messages": {"ギャル先生": "シカちゃん、今日はあんたが主役だよ！💖"}
        },
        "INFJ": {
            "name": "提唱者", "animal": "思慮深いフクロウ", 
            "catchphrase": "「夜の静寂の中で、未来の光を見通す賢者」",
            "mentor": "頼れるお姉さん",
            "details": {
                "work": "直感で本質を掴み、理想を形にする『静かなリーダー』。意味のないルーチンワークは魂が削れるわ。",
                "love": "精神的な深い繋がりを求める。理想が高いけど、一度心を許すと一生モノの絆を築くわよ。",
                "stress": "感覚が過敏になり、暴飲暴食や衝動買いに走るか、完全に引きこもって音信不通になるわ。",
                "best_match": "情熱的なライオン（ENFJ）"
            },
            "messages": {"ギャル先生": "フクロウちゃん、リスペクト！🌈"}
        },
        "INTJ": {
            "name": "建築家", "animal": "孤高のトラ", 
            "catchphrase": "「誰にも媚びず、己の知略で世界を再構築する」",
            "mentor": "カサネ・イズミ：論理と不確定要素",
            "details": {
                "work": "長期的な戦略を立てて効率的に目標を達成する『軍師』。無能な慣習には容赦なくNOを突きつけるわ。",
                "love": "感情表現は苦手だけど、知的な刺激を重視する。信頼した相手には超論理的に尽くすタイプ。",
                "stress": "普段の戦略性が消え、ジャンクな刺激（ドカ食いやゲーム等）に没頭して現実逃避しちゃうわよ。",
                "best_match": "独創的なキツネ（ENTP）"
            },
            "messages": {"ギャル先生": "トラさん、クールすぎ！その最強頭脳で世界回そ！🔥"}
        },
        "ISTP": {
            "name": "巨匠", "animal": "冷静なサメ", 
            "catchphrase": "「乱世をクールに泳ぎ、一瞬の好機を逃さない」",
            "mentor": "ツンデレな指導員",
            "details": {
                "work": "現場で手を動かして問題を即解決する『一匹狼のプロ』。束縛されるのが大嫌いで自由を愛するわ。",
                "love": "付かず離れずの距離感を大切にする。束縛されると逃げるけど、ピンチの時には必ず助けに来るわよ。",
                "stress": "感情が制御不能になって爆発するか、周りに対して極端に攻撃的・批判的な態度をとっちゃう。",
                "best_match": "勇敢なチーター（ESTP）"
            },
            "messages": {"ギャル先生": "サメちゃん、自由で最高！センス神！✨"}
        },
        "ISFP": {
            "name": "冒険家", "animal": "自由なネコ", 
            "catchphrase": "「自分の『好き』を呼吸するように生きる芸術家」",
            "mentor": "ギャル先生",
            "details": {
                "work": "自分の感性を形にする『アーティスト』。競争よりも、自分が納得できる『心地よさ』を最優先するわ。",
                "love": "言葉よりも行動や雰囲気で愛情を示す。自由奔放に見えて、実は相手の顔色をすごく伺ってる繊細さん。",
                "stress": "自信を完全に喪失して『自分には何の才能もない』と絶望。殻に閉じこもって誰の言葉も届かなくなる。",
                "best_match": "陽気なレッサーパンダ（ESFP）"
            },
            "messages": {"ギャル先生": "ネコちゃん、感性ヤバすぎ！貫いちゃえ！🐾"}
        },
        "INFP": {
            "name": "仲介者", "animal": "理想を夢見るウサギ", 
            "catchphrase": "「傷つくことを恐れず、愛と優しさを信じ続ける」",
            "mentor": "頼れるお姉さん",
            "details": {
                "work": "独自の価値観で世界を彩る『夢想家』。お金や名誉より、自分の魂が震えるかどうかが全ての基準。",
                "love": "ロマンチックで深い愛情の持ち主。相手を理想化しすぎて、現実にガッカリしちゃうこともあるけど純粋。",
                "stress": "急に超現実的で攻撃的な性格に変貌。他人の欠点を理詰めで攻撃して、後で猛烈に後悔するわ。",
                "best_match": "天真爛漫なカワウソ（ENFP）"
            },
            "messages": {"ギャル先生": "ウサギちゃん、優しさ神！応援してるよ！🐰"}
        },
        "INTP": {
            "name": "論理学者", "animal": "探求するチンパンジー", 
            "catchphrase": "「常識を疑い、知の迷宮を楽しむ知的な探検家」",
            "mentor": "カサネ・イズミ：論理と不確定要素",
            "details": {
                "work": "複雑な仕組みを解明する『天才分析官』。興味のあることへの集中力はエグいけど、事務作業は放置気味。",
                "love": "知的な会話ができる相手が大好き。好き避けしがちだけど、心の中では相手を細かく分析して理解しようとする。",
                "stress": "感情がオーバーフローして、急に泣き出したり、周囲に対して過剰に感情的・理不尽な怒りをぶつける。",
                "best_match": "威風堂々なワシ（ENTJ）"
            },
            "messages": {"ギャル先生": "パンジーくん、天才すぎ！バズるよ！🚀"}
        },
        mbti_db = {
        "ISTJ": {
            "name": "管理者", "animal": "勤勉なビーバー", 
            "catchphrase": "「一歩ずつ、確実に。信頼を築き上げる職人」",
            "mentor": "論理的なビジネスコーチ",
            "details": {
                "work": "マニュアルや手順を完璧に守り、ミスなく成果を出す『組織の柱』。締め切りは絶対守る派。",
                "love": "超誠実で一途。記念日を忘れず、安定した関係を築くけど、変化やサプライズはちょっと苦手。",
                "stress": "普段の冷静さを失い、細かいミスに固執してパニックに。自分を責めすぎて負のループへ。",
                "best_match": "お世話好きなゾウ（ESFJ）"
            },
            "messages": {"ギャル先生": "ビーバーちゃん、マジメすぎ！たまには羽目外そ！✨"}
        },
        "ISFJ": {
            "name": "擁護者", "animal": "穏やかなシカ", 
            "catchphrase": "「静かな優しさで、みんなの心に灯をともす」",
            "mentor": "優しさに溢れるメンター (Default)",
            "details": {
                "work": "他人のニーズを察して先回りする『最高のサポーター』。縁の下の力持ちとして評価されるわ。",
                "love": "献身的に尽くすタイプ。相手の喜びが自分の喜びだけど、不満を溜め込みすぎて爆発することも。",
                "stress": "『自分なんて必要ないんだ』と思い込み、過剰に悲観的に。体調にもすぐ出ちゃうから注意！",
                "best_match": "誠実な番犬（ESTJ）"
            },
            "messages": {"ギャル先生": "シカちゃん、今日はあんたが主役だよ！💖"}
        },
        "INFJ": {
            "name": "提唱者", "animal": "思慮深いフクロウ", 
            "catchphrase": "「夜の静寂の中で、未来の光を見通す賢者」",
            "mentor": "頼れるお姉さん",
            "details": {
                "work": "直感で本質を掴み、理想を形にする『静かなリーダー』。意味のないルーチンワークは魂が削れるわ。",
                "love": "精神的な深い繋がりを求める。理想が高いけど、一度心を許すと一生モノの絆を築くわよ。",
                "stress": "感覚が過敏になり、暴飲暴食や衝動買いに走るか、完全に引きこもって音信不通になるわ。",
                "best_match": "情熱的なライオン（ENFJ）"
            },
            "messages": {"ギャル先生": "フクロウちゃん、リスペクト！🌈"}
        },
        "INTJ": {
            "name": "建築家", "animal": "孤高のトラ", 
            "catchphrase": "「誰にも媚びず、己の知略で世界を再構築する」",
            "mentor": "カサネ・イズミ：論理と不確定要素",
            "details": {
                "work": "長期的な戦略を立てて効率的に目標を達成する『軍師』。無能な慣習には容赦なくNOを突きつけるわ。",
                "love": "感情表現は苦手だけど、知的な刺激を重視する。信頼した相手には超論理的に尽くすタイプ。",
                "stress": "普段の戦略性が消え、ジャンクな刺激（ドカ食いやゲーム等）に没頭して現実逃避しちゃうわよ。",
                "best_match": "独創的なキツネ（ENTP）"
            },
            "messages": {"ギャル先生": "トラさん、クールすぎ！その最強頭脳で世界回そ！🔥"}
        },
        "ISTP": {
            "name": "巨匠", "animal": "冷静なサメ", 
            "catchphrase": "「乱世をクールに泳ぎ、一瞬の好機を逃さない」",
            "mentor": "ツンデレな指導員",
            "details": {
                "work": "現場で手を動かして問題を即解決する『一匹狼のプロ』。束縛されるのが大嫌いで自由を愛するわ。",
                "love": "付かず離れずの距離感を大切にする。束縛されると逃げるけど、ピンチの時には必ず助けに来るわよ。",
                "stress": "感情が制御不能になって爆発するか、周りに対して極端に攻撃的・批判的な態度をとっちゃう。",
                "best_match": "勇敢なチーター（ESTP）"
            },
            "messages": {"ギャル先生": "サメちゃん、自由で最高！センス神！✨"}
        },
        "ISFP": {
            "name": "冒険家", "animal": "自由なネコ", 
            "catchphrase": "「自分の『好き』を呼吸するように生きる芸術家」",
            "mentor": "ギャル先生",
            "details": {
                "work": "自分の感性を形にする『アーティスト』。競争よりも、自分が納得できる『心地よさ』を最優先するわ。",
                "love": "言葉よりも行動や雰囲気で愛情を示す。自由奔放に見えて、実は相手の顔色をすごく伺ってる繊細さん。",
                "stress": "自信を完全に喪失して『自分には何の才能もない』と絶望。殻に閉じこもって誰の言葉も届かなくなる。",
                "best_match": "陽気なレッサーパンダ（ESFP）"
            },
            "messages": {"ギャル先生": "ネコちゃん、感性ヤバすぎ！貫いちゃえ！🐾"}
        },
        "INFP": {
            "name": "仲介者", "animal": "理想を夢見るウサギ", 
            "catchphrase": "「傷つくことを恐れず、愛と優しさを信じ続ける」",
            "mentor": "頼れるお姉さん",
            "details": {
                "work": "独自の価値観で世界を彩る『夢想家』。お金や名誉より、自分の魂が震えるかどうかが全ての基準。",
                "love": "ロマンチックで深い愛情の持ち主。相手を理想化しすぎて、現実にガッカリしちゃうこともあるけど純粋。",
                "stress": "急に超現実的で攻撃的な性格に変貌。他人の欠点を理詰めで攻撃して、後で猛烈に後悔するわ。",
                "best_match": "天真爛漫なカワウソ（ENFP）"
            },
            "messages": {"ギャル先生": "ウサギちゃん、優しさ神！応援してるよ！🐰"}
        },
        "INTP": {
            "name": "論理学者", "animal": "探求するチンパンジー", 
            "catchphrase": "「常識を疑い、知の迷宮を楽しむ知的な探検家」",
            "mentor": "カサネ・イズミ：論理と不確定要素",
            "details": {
                "work": "複雑な仕組みを解明する『天才分析官』。興味のあることへの集中力はエグいけど、事務作業は放置気味。",
                "love": "知的な会話ができる相手が大好き。好き避けしがちだけど、心の中では相手を細かく分析して理解しようとする。",
                "stress": "感情がオーバーフローして、急に泣き出したり、周囲に対して過剰に感情的・理不尽な怒りをぶつける。",
                "best_match": "威風堂々なワシ（ENTJ）"
            },
            "messages": {"ギャル先生": "パンジーくん、天才すぎ！バズるよ！🚀"}
        },
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
