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

    # --- 2. メンターデータ & MBTI DB (データ部分は長いので省略せず保持) ---
    mentor_data = {
        "ギャル先生": {"quote": "「おはよー！あんたの魅力、マジでバズり確定じゃん！✨」", "actions": ["「コンビニの新作スイーツ買って自分にご褒美あげちゃお！✨」", "「鏡の前で『今日も可愛いじゃん』って言ってみて？💖」", "「派手な色の小物を1つ身につけてみて！🌈」"]},
        "頼れるお姉さん": {"quote": "「一生懸命なところ、素敵よ。でもたまには肩の力を抜いて、私に甘えていいのよ？」", "actions": ["「5分だけデジタルデトックスをして温かい飲み物を。」", "「寝る前に頑張ったことを3つ思い出して自分を褒めて。」"]},
        "カサネ・イズミ：論理と不確定要素": {"quote": "「あなたのデータは極めて特異だ。その思考を最適化すれば、さらなる高みへ到達できる。」", "actions": ["「デスクの上を完全に片付けろ。」", "「今日学んだことを3行でメモしろ。」"]},
        "ツンデレな指導員": {"quote": "「ふん、あんたみたいなタイプは私が付いてないと危なっかしいわね。」", "actions": ["「姿勢を正しなさい！」", "「たまには自分を甘やかしなさいよね。」"]},
        "論理的なビジネスコーチ": {"quote": "「あなたの能力を最大限に活かすための戦略を練ろう。」", "actions": ["「今日一番の重要課題を1つ決めて集中しよう。」"]},
        "優しさに溢れるメンター (Default)": {"quote": "「あなたは今のままで十分素晴らしいですよ。」", "actions": ["「深呼吸をゆっくり3回しましょう。」"]}
    }

    mbti_db = {
        "ISTJ": {"name": "管理者", "animal": "勤勉なビーバー", "catchphrase": "「一歩ずつ、確実に。信頼を築き上げる職人」", "strength": "責任感の塊、精密な作業", "weakness": "変化への抵抗", "mentor": "論理的なビジネスコーチ", "details": {"work": "マニュアル重視", "love": "超誠実", "stress": "細かいミスに固執", "best_match": "お世話好きなゾウ（ESFJ）"}, "messages": {"ギャル先生": "ビーバーちゃん、マジメすぎ！✨"}},
        "ISFJ": {"name": "擁護者", "animal": "穏やかなシカ", "catchphrase": "「静かな優しさで、みんなの心に灯をともす」", "strength": "配慮、誠実", "weakness": "自己犠牲", "mentor": "優しさに溢れるメンター (Default)", "details": {"work": "最高のサポーター", "love": "献身的", "stress": "悲観的", "best_match": "誠実な番犬（ESTJ）"}, "messages": {"ギャル先生": "シカちゃん、今日はあんたが主役！💖"}},
        "INFJ": {"name": "提唱者", "animal": "思慮深いフクロウ", "catchphrase": "「夜の静寂の中で、未来の光を見通す賢者」", "strength": "洞察力、理想", "weakness": "感情疲労", "mentor": "頼れるお姉さん", "details": {"work": "静かなリーダー", "love": "深い繋がり", "stress": "感覚過敏", "best_match": "情熱的なライオン（ENFJ）"}, "messages": {"ギャル先生": "フクロウちゃん、リスペクト！🌈"}},
        "INTJ": {"name": "建築家", "animal": "孤高のトラ", "catchphrase": "「誰にも媚びず、己の知略で世界を再構築する」", "strength": "戦略的思考", "weakness": "感情への無関心", "mentor": "カサネ・イズミ：論理と不確定要素", "details": {"work": "軍師", "love": "知的刺激重視", "stress": "現実逃避", "best_match": "独創的なキツネ（ENTP）"}, "messages": {"ギャル先生": "トラさん、クールすぎ！🔥"}},
        "ISTP": {"name": "巨匠", "animal": "冷静なサメ", "catchphrase": "「乱世をクールに泳ぎ、一瞬の好機を逃さない」", "strength": "解決力", "weakness": "無関心", "mentor": "ツンデレな指導員", "details": {"work": "一匹狼のプロ", "love": "距離感大切", "stress": "感情爆発", "best_match": "勇敢なチーター（ESTP）"}, "messages": {"ギャル先生": "サメちゃん、自由で最高！✨"}},
        "ISFP": {"name": "冒険家", "animal": "自由なネコ", "catchphrase": "「自分の『好き』を呼吸するように生きる芸術家」", "strength": "美的センス", "weakness": "批判に弱い", "mentor": "ギャル先生", "details": {"work": "アーティスト", "love": "繊細さん", "stress": "自信喪失", "best_match": "陽気なレッサーパンダ（ESFP）"}, "messages": {"ギャル先生": "ネコちゃん、感性ヤバすぎ！🐾"}},
        "INFP": {"name": "仲介者", "animal": "理想を夢見るウサギ", "catchphrase": "「傷つくことを恐れず、愛と優しさを信じ続ける」", "strength": "表現力", "weakness": "実務放置", "mentor": "頼れるお姉さん", "details": {"work": "夢想家", "love": "ロマンチスト", "stress": "攻撃的に変貌", "best_match": "天真爛漫なカワウソ（ENFP）"}, "messages": {"ギャル先生": "ウサギちゃん、優しさ神！🐰"}},
        "INTP": {"name": "論理学者", "animal": "探求するチンパンジー", "catchphrase": "「常識を疑い、知の迷宮を楽しむ知的な探検家」", "strength": "分析力", "weakness": "実行の遅れ", "mentor": "カサネ・イズミ：論理と不確定要素", "details": {"work": "天才分析官", "love": "知的な会話", "stress": "感情漏洩", "best_match": "威風堂々なワシ（ENTJ）"}, "messages": {"ギャル先生": "パンジーくん、天才すぎ！🚀"}},
        "ESTP": {"name": "起業家", "animal": "勇敢なチーター", "catchphrase": "「考える前に跳べ。世界を遊び場に変える開拓者」", "strength": "エナジー", "weakness": "無神経", "mentor": "ツンデレな指導員", "details": {"work": "トラブルシューター", "love": "情熱的", "stress": "暴走", "best_match": "冷静なサメ（ISTP）"}, "messages": {"ギャル先生": "チーターくん、爆速すぎ！🐆"}},
        "ESFP": {"name": "エンターテイナー", "animal": "陽気なレッサーパンダ", "catchphrase": "「一瞬で場を彩る、愛されキャラの天才」", "strength": "ムードメーカー", "weakness": "孤独不安", "mentor": "ギャル先生", "details": {"work": "場の空気作り", "love": "楽しさ重視", "stress": "被害妄想", "best_match": "自由なネコ（ISFP）"}, "messages": {"ギャル先生": "パンダちゃん、最高！🐼"}},
        "ENFP": {"name": "広報運動家", "animal": "天真爛漫なカワウソ", "catchphrase": "「無限のワクワクを撒き散らす、愛の伝道師」", "strength": "クリエイター", "weakness": "中途半端", "mentor": "ギャル先生", "details": {"work": "アイディアマン", "love": "運命信じる", "stress": "強迫観念", "best_match": "理想を夢見るウサギ（INFP）"}, "messages": {"ギャル先生": "カワウソちゃん、全開！🦦"}},
        "ENTP": {"name": "討論者", "animal": "独創的なキツネ", "catchphrase": "「知的なイタズラで、退屈な世界に風穴を開ける」", "strength": "イノベーター", "weakness": "論破癖", "mentor": "ツンデレな指導員", "details": {"work": "常識破壊", "love": "駆け引き", "stress": "執着", "best_match": "孤高のトラ（INTJ）"}, "messages": {"ギャル先生": "キツネくん、天才！🦊"}},
        "ESTJ": {"name": "幹部", "animal": "誠実な番犬", "catchphrase": "「揺るぎない正義感で、秩序と平和を守り抜く」", "strength": "リーダーシップ", "weakness": "独断", "mentor": "論理的なビジネスコーチ", "details": {"work": "組織の司令塔", "love": "責任感強", "stress": "孤独感", "best_match": "穏やかなシカ（ISFJ）"}, "messages": {"ギャル先生": "ワンちゃん、リスペクト！🐕"}},
        "ESFJ": {"name": "領事", "animal": "お世話好きなゾウ", "catchphrase": "「大きな愛でみんなを包む、コミュニティの守護神」", "strength": "調和", "weakness": "お節介", "mentor": "優しさに溢れるメンター (Default)", "details": {"work": "守護者", "love": "愛情濃厚", "stress": "理屈批判", "best_match": "勤めるビーバー（ISTJ）"}, "messages": {"ギャル先生": "ゾウさん、優しさMAX！🐘"}},
        "ENFJ": {"name": "主人公", "animal": "情熱的なライオン", "catchphrase": "「みんなの可能性を信じ、光差す方へ導く太陽」", "strength": "カリスマ", "weakness": "自滅", "mentor": "頼れるお姉さん", "details": {"work": "導き手", "love": "理想追求", "stress": "自閉", "best_match": "思慮深いフクロウ（INFJ）"}, "messages": {"ギャル先生": "ライオンくん、情熱ヤバい！🦁"}},
        "ENTJ": {"name": "指揮官", "animal": "威風堂々なワシ", "catchphrase": "「高みから未来を見据え、勝利への最短距離を飛ぶ」", "strength": "決断力", "weakness": "容赦なさ", "mentor": "論理的なビジネスコーチ", "details": {"work": "指揮官", "love": "恋愛プロジェクト", "stress": "繊細化", "best_match": "探求するチンパンジー（INTP）"}, "messages": {"ギャル先生": "ワシさん、最強リーダー！🦅"}}
    }

    # --- 3. 画面の切り替え判定 ---
    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False

    # 【A】質問モード
    if not st.session_state["show_result"]:
        st.title("🐾 性格診断クエスト")
        
        # 進捗計算
        answered_count = 0
        for i in range(len(questions)):
            if f"q_{i}" in st.session_state:
                answered_count += 1
        
        with st.sidebar:
            st.header("📊 診断の進捗")
            progress = answered_count / len(questions)
            st.progress(progress)
            st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
            st.divider()
            if progress < 0.5: st.write("ギャル先生：「直感でポチポチいこー！✨」")
            elif progress < 1.0: st.write("ギャル先生：「いい感じ！あと少し！🔥」")
            else: st.write("ギャル先生：「完璧！ボタン押しちゃいな！💖」")

        user_answers = {}
        for i, (q_text, axis, weight) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            user_answers[i] = st.radio(
                f"radio_{i}", options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=2
            )
            st.write("---")
        
        if st.button("診断結果を詳しく見る ✨", use_container_width=True):
            if answered_count < len(questions):
                st.error(f"まだ回答していない質問があるよ！（残り {len(questions) - answered_count} 問）")
            else:
                st.session_state["show_result"] = True
                st.rerun()

    # 【B】結果モード
    else:
        st.balloons()
        # スコア計算
        scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0}
        for i, (_, axis, weight) in enumerate(questions):
            # ラジオボタンの値を直接取得
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3) * weight

        mbti_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                    ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        full_res = mbti_core + ("-A" if scores["A-T"] >= 0 else "-T")
        detail = mbti_db.get(mbti_core, mbti_db["ISTJ"])

        st.markdown(f"## 判定結果：{full_res}")
        st.markdown(f"### あなたを動物に例えると… 『 {detail['animal']} 』")
        st.info(f"**{detail['catchphrase']}**")

        tab1, tab2, tab3, tab4 = st.tabs(["💼 仕事・勉強", "💖 人間関係", "💀 裏の顔", "🤝 相性"])
        with tab1: st.write(f"**スタイル：**\n\n{detail['details']['work']}")
        with tab2: st.write(f"**傾向：**\n\n{detail['details']['love']}")
        with tab3: st.warning(f"**ストレス時：**\n\n{detail['details']['stress']}")
        with tab4: st.info(f"**最高の相性：**\n\n{detail['details']['best_match']}")

        # チャート表示
        categories = ['外向(E)', '感覚(S)', '思考(T)', '判断(J)', '自己主張(A)']
        values = [scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-12, 12])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # メンター
        st.markdown("### 🤝 今日のメンター")
        selected_mentor = st.selectbox("メンターを指名", options=list(mentor_data.keys()), index=0)
        m_info = mentor_data[selected_mentor]
        msg = detail["messages"].get(selected_mentor, m_info["quote"])
        st.chat_message("assistant").write(f"**{selected_mentor}**：「{msg}」")
        st.success(f"🎁 **ラッキーアクション**：{random.choice(m_info['actions'])}")

        # ダウンロード
        st.download_button("結果を保存 📥", f"結果: {full_res}\n動物: {detail['animal']}", file_name="result.txt", use_container_width=True)

        # 🔄 やり直しボタン (最強リセット)
        st.divider()
        if st.button("🔄 最初からやり直す", use_container_width=True):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_mbti_diagnostic()
