import streamlit as st
import plotly.graph_objects as go
import random

def run_mbti_diagnostic():
    st.set_page_config(page_title="MBTI性格診断 Pro", page_icon="🧠", layout="wide")

    st.markdown('<h3 style="font-size: 26px; font-weight: bold; color: #4A90E2;">🧠 性格タイプ診断 Pro (究極フルセット版)</h3>', unsafe_allow_html=True)
    st.caption("2025年12月23日 05:50：保存機能と全メンター機能を完全搭載しました。")

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

    # --- 2. メンター詳細データ (全6名) ---
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
            "actions": ["「姿勢を正しなさい！背筋を伸ばしなさい！それだけで印象が変わるんだから。」", "「たまには自分を甘やかしなさいよね。心配してないわよ！」", "「今日は10分早く寝なさい。明日寝坊して困るのはあんたなんだから。」"]
        },
        "論理的なビジネスコーチ": {
            "quote": "「あなたの能力を最大限に活かすための戦略を練ろう。まずは現状の分析からだ。」",
            "actions": ["「今日一番の重要課題を1つ決めて、それに集中しよう。」", "「明日のスケジュールを今夜のうちに10分で見直しておこう。」", "「身の回りのものを1つだけ新調してみよう。小さな変化が刺激になる。」"]
        },
        "優しさに溢れるメンター (Default)": {
            "quote": "「あなたは今のままで十分素晴らしいですよ。一緒に、一歩ずつ進んでいきましょうね。」",
            "actions": ["「深呼吸をゆっくり3回しましょう。」", "「大切な人に短い感謝のメッセージを送ってみませんか？」", "「散歩をしながら、空の色を眺めてみてください。」"]
        }
    }

    # --- 3. 性格タイプ詳細DB (全16タイプ網羅) ---
    mbti_db = {
        "ISTJ": {"name": "管理者", "strength": "誠実、責任感、正確な実務", "weakness": "頑固、変化への抵抗", "mentor": "論理的なビジネスコーチ"},
        "ISFJ": {"name": "擁護者", "strength": "献身的、忍耐強い、サポート力", "weakness": "自分を後回しにする、変化を恐れる", "mentor": "優しさに溢れるメンター (Default)"},
        "INFJ": {"name": "提唱者", "strength": "洞察力、理想主義、深い共感", "weakness": "完璧主義、燃え尽きやすい", "mentor": "頼れるお姉さん"},
        "INTJ": {"name": "建築家", "strength": "戦略的思考、独創性、高い合理性", "weakness": "批判的、人間関係を軽視しがち", "mentor": "カサネ・イズミ：論理と不確定要素"},
        "ISTP": {"name": "巨匠", "strength": "適応力、技術的センス、冷静沈着", "weakness": "飽き性、孤立しやすい", "mentor": "ツンデレな指導員"},
        "ISFP": {"name": "冒険家", "strength": "芸術的センス、柔軟性、調和", "weakness": "計画不足、ストレス耐性が低い", "mentor": "ギャル先生"},
        "INFP": {"name": "仲介者", "strength": "深い思いやり、独創性、誠実さ", "weakness": "理想が高すぎる、傷つきやすい", "mentor": "頼れるお姉さん"},
        "INTP": {"name": "論理学者", "strength": "客観的な分析、好奇心、斬新な発想", "weakness": "理屈っぽい、実行力が不足しがち", "mentor": "カサネ・イズミ：論理と不確定要素"},
        "ESTP": {"name": "起業家", "strength": "行動力、即断即決、社交的", "weakness": "リスクを取りすぎる、忍耐不足", "mentor": "ツンデレな指導員"},
        "ESFP": {"name": "エンターテイナー", "strength": "社交的、楽天家、今を楽しむ力", "weakness": "飽き性、深い思考を避けがち", "mentor": "ギャル先生"},
        "ENFP": {"name": "広報運動家", "strength": "情熱、高い共感力、人脈作り", "weakness": "集中力の分散、事務作業が苦手", "mentor": "ギャル先生"},
        "ENTP": {"name": "討論者", "strength": "機転が利く、独創的、知識欲", "weakness": "議論好きすぎる、ルール無視", "mentor": "ツンデレな指導員"},
        "ESTJ": {"name": "幹部", "strength": "組織化、リーダーシップ、強い意志", "weakness": "融通が利かない、高圧的になりがち", "mentor": "論理的なビジネスコーチ"},
        "ESFJ": {"name": "領事", "strength": "協力的、親切、実務的な管理", "weakness": "他人の目を気にしすぎる", "mentor": "優しさに溢れるメンター (Default)"},
        "ENFJ": {"name": "主人公", "strength": "カリスマ性、献身的、説得力", "weakness": "おせっかい、理想の押し付け", "mentor": "頼れるお姉さん"},
        "ENTJ": {"name": "指揮官", "strength": "強い意志、効率性、自信", "weakness": "冷徹に見える、短気な面がある", "mentor": "論理的なビジネスコーチ"}
    }

    # --- 4. 進捗管理 ---
    answered_count = 0
    for i in range(len(questions)):
        key = f"q_{i}"
        if key in st.session_state and st.session_state[key] is not None:
            answered_count += 1
    
    with st.sidebar:
        st.header("📊 診断の進捗")
        progress_per = answered_count / len(questions)
        st.progress(progress_per)
        st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
        st.divider()
        st.markdown("**ギャル先生からの応援**")
        if progress_per < 0.5: st.write("「まずは直感でポチポチいこー！✨」")
        elif progress_per < 1.0: st.write("「いい感じ！半分超えたよ、あと少し！🔥」")
        else: st.write("「完璧！あんたマジ最高！ボタン押しちゃいな！💖」")

    # --- 5. 質問表示 ---
    user_answers = {}
    for i, (q_text, axis, weight) in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q_text}**")
        user_answers[i] = st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5], 
                                   format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                                   key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
        st.write("---")

    # --- 6. 診断実行 ---
    if st.button("診断結果を詳しく見る ✨", use_container_width=True):
        if answered_count < len(questions):
            st.error(f"まだ回答していない質問があるよ！（残り {len(questions) - answered_count} 問）")
        else:
            st.session_state["show_result"] = True

    if st.session_state.get("show_result"):
        st.balloons()
        scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0}
        for i, (q_text, axis, weight) in enumerate(questions):
            scores[axis] += (st.session_state[f"q_{i}"] - 3) * weight

        mbti_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                    ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        identity = "-A" if scores["A-T"] >= 0 else "-T"
        full_res = mbti_core + identity

        detail = mbti_db.get(mbti_core)

        st.divider()
        st.markdown(f"## 判定結果：{full_res}（{detail['name']}）")

        # レーダーチャート
        categories = ['外向(E)', '感覚(S)', '思考(T)', '判断(J)', '自己主張(A)']
        values = [scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]]
        fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#4A90E2', fillcolor='rgba(74, 144, 226, 0.3)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-12, 12])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # 具体的解説
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"✨ **ここがあなたの武器（強み）**\n\n{detail['strength']}")
        with col2:
            st.warning(f"⚠️ **ここに注意（気をつけたい点）**\n\n{detail['weakness']}")

        st.divider()

        # 🤝 メンター指名セクション
        st.markdown("### 🤝 今日のメンターを指名する")
        selected_mentor = st.selectbox(
            "今の気分に合わせてメンターを選んでね！",
            options=list(mentor_data.keys()),
            index=list(mentor_data.keys()).index(detail["mentor"]) if detail["mentor"] in mentor_data else 5
        )

        m_info = mentor_data[selected_mentor]
        st.chat_message("assistant").write(f"**{selected_mentor}**：「{m_info['quote']}」")
        
        current_action = random.choice(m_info['actions'])
        st.success(f"🎁 **今日のラッキーアクション**：{current_action}")

        # --- 7. 保存機能 ---
        report_text = f"""【MBTI性格診断 Pro レポート】
日時: 2025年12月23日 05:50
判定結果: {full_res}（{detail['name']}）

■ あなたの強み: {detail['strength']}
■ 注意点: {detail['weakness']}

■ メンター: {selected_mentor}
■ ラッキーアクション: {current_action}
"""
        st.divider()
        st.download_button(
            label="診断結果をテキストでダウンロード 📥",
            data=report_text,
            file_name=f"MBTI_Result_{full_res}.txt",
            mime="text/plain",
            use_container_width=True
        )

if __name__ == "__main__":
    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False
    run_mbti_diagnostic()
