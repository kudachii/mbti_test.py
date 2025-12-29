import streamlit as st
import plotly.graph_objects as go
import random

def run_mbti_diagnostic():
    st.set_page_config(page_title="MBTI性格診断 Pro", page_icon="🧠", layout="wide")

    st.markdown('<h3 style="font-size: 26px; font-weight: bold; color: #4A90E2;">🧠 性格タイプ診断 Pro (超具体的アドバイス版)</h3>', unsafe_allow_html=True)
    st.caption("2025年12月23日 05:52：16タイプすべての解説を限界まで具体化しました。")

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

    # --- 2. メンターデータ (全6名) ---
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
            "actions": ["「深呼吸をゆっくり3回しましょう。」", "「大切な人に短い感謝のメッセージを送ってみませんか？」", "「散歩をしながら、空の色を眺めてみてください。」"]
        }
    }

    # --- 3. 性格タイプ詳細DB (全16タイプ・超具体版) ---
    # mbti_db を以下のようにアップデートしてみて！
mbti_db = {
    "ISTJ": {
        "name": "管理者",
        "animal": "勤勉なビーバー",
        "catchphrase": "「一歩ずつ、確実に。信頼を築き上げる職人」",
        "strength": "・一度引き受けた仕事は最後までやり遂げる責任感。\n・膨大なデータからミスを見つけ出す精密さ。\n・冷静な判断力。",
        "weakness": "・マニュアル外のことに弱い。\n・正論で相手を追い詰めがち。\n・SOSを出すのが苦手。",
        "mentor": "論理的なビジネスコーチ"
    },
    "ISFJ": {
        "name": "擁護者",
        "animal": "穏やかなシカ",
        "catchphrase": "「静かな優しさで、みんなの心に灯をともす」",
        "strength": "・他人の変化を察する神がかった配慮。\n・些細なことを覚えている誠実さ。\n・最高のサポート力。",
        "weakness": "・「いい人」を演じて疲れ果てる。\n・感謝されないと極端に凹む。\n・断るのが苦手。",
        "mentor": "優しさに溢れるメンター (Default)"
    },
    "INFJ": {
        "name": "提唱者",
        "animal": "思慮深いフクロウ",
        "catchphrase": "「夜の静寂の中で、未来の光を見通す賢者」",
        "strength": "・本質を見抜く圧倒的な洞察力。\n・高い理想で人を導くカリスマ性。\n・相手の才能を見つけ出すのが上手い。",
        "weakness": "・理想と現実のギャップに絶望しやすい。\n・自分を追い込みすぎる完璧主義。\n・他人の感情を吸い込みすぎて疲弊する。",
        "mentor": "頼れるお姉さん"
    },
    "INTJ": {
        "name": "建築家",
        "animal": "孤高のトラ",
        "catchphrase": "「誰にも媚びず、己の知略で世界を再構築する」",
        "strength": "・10手先まで読む戦略的思考。\n・事実を繋ぎ合わせる解決能力。\n・圧倒的な自己信頼と実行力。",
        "weakness": "・感情を非効率と切り捨てる冷徹さ。\n・他人の意見を即座に否定しがち。\n・弱みを見せられず孤立しやすい。",
        "mentor": "カサネ・イズミ：論理と不確定要素"
    },
    "ISTP": {
        "name": "巨匠",
        "animal": "冷静なサメ",
        "catchphrase": "「乱世をクールに泳ぎ、一瞬の好機を逃さない」",
        "strength": "・緊急事態でも笑って手を動かす解決力。\n・道具やITを使いこなす抜群のセンス。\n・適度な距離感で付き合える気楽さ。",
        "weakness": "・興味のないことに驚くほど無関心。\n・長期計画やルーティンが苦手。\n・感情的な問題を先延ばしにする。",
        "mentor": "ツンデレな指導員"
    },
    "ISFP": {
        "name": "冒険家",
        "animal": "自由なネコ",
        "catchphrase": "「自分の『好き』を呼吸するように生きる芸術家」",
        "strength": "・独自の美的センスと魅力。\n・どんな人でも受け入れる器の広さ。\n・今、この瞬間を全力で楽しむ才能。",
        "weakness": "・批判されると存在を否定されたと感じる。\n・気分で動くため約束を忘れがち。\n・突然シャッターを下ろす極端な行動。",
        "mentor": "ギャル先生"
    },
    "INFP": {
        "name": "仲介者",
        "animal": "理想を夢見るウサギ",
        "catchphrase": "「傷つくことを恐れず、愛と優しさを信じ続ける」",
        "strength": "・心の微細な動きを言葉にする表現力。\n・魂を売らない誠実さと信念。\n・損を承知で助けにいく深い慈愛。",
        "weakness": "・現実的な実務を放置しがち。\n・現実の自分とのギャップに自信を失う。\n・過去のトラウマを反芻して抜け出せない。",
        "mentor": "頼れるお姉さん"
    },
    "INTP": {
        "name": "論理学者",
        "animal": "探求するチンパンジー",
        "catchphrase": "「常識を疑い、知の迷宮を楽しむ知的な探検家」",
        "strength": "・誰も思いつかない斬新なアイデア。\n・複雑な事象をシンプルにする抽象化能力。\n・真理追求のためなら孤独も厭わない。",
        "weakness": "・考えるだけで実行が極端に遅い。\n・社会的なマナーを無視して変人扱い。\n・他人の悩みを論理分析して怒らせる。",
        "mentor": "カサネ・イズミ：論理と不確定要素"
    },
    "ESTP": {
        "name": "起業家",
        "animal": "勇敢なチーター",
        "catchphrase": "「考える前に跳べ。世界を遊び場に変える開拓者」",
        "strength": "・圧倒的なエネルギーと社交性。\n・即座に軌道修正するスピード感。\n・困難を「面白そう！」と笑い飛ばす力。",
        "weakness": "・不必要なリスクに首を突っ込む。\n・長期的な健康や約束を疎かにしがち。\n・繊細な悩みを一蹴して無神経と思われる。",
        "mentor": "ツンデレな指導員"
    },
    "ESFP": {
        "name": "エンターテイナー",
        "animal": "陽気なレッサーパンダ",
        "catchphrase": "「一瞬で場を彩る、愛されキャラの天才」",
        "strength": "・場を明るくする「歩く太陽」。\n・人々を喜ばせる空間作りのセンス。\n・流行を取り入れる好奇心と行動力。",
        "weakness": "・孤独を極端に嫌い不安になりやすい。\n・深刻な空気を冗談で逃げようとする。\n・衝動買いや無計画な行動で自爆する。",
        "mentor": "ギャル先生"
    },
    "ENFP": {
        "name": "広報運動家",
        "animal": "天真爛漫なカワウソ",
        "catchphrase": "「無限のワクワクを撒き散らす、愛の伝道師」",
        "strength": "・人の隠れた才能を見抜く力。\n・一瞬で打ち解ける圧倒的なコミュ力。\n・失敗を「経験」に変えるレジリエンス。",
        "weakness": "・多趣味すぎて全て中途半端に終わりがち。\n・他人の反応に一喜一憂しすぎる。\n・ルーティンワークへの耐性がゼロ。",
        "mentor": "ギャル先生"
    },
    "ENTP": {
        "name": "討論者",
        "animal": "独創的なキツネ",
        "catchphrase": "「知的なイタズラで、退屈な世界に風穴を開ける」",
        "strength": "・常識を疑い、新しい基準を作る力。\n・圧倒的な語彙力と交渉術。\n・トラブルが起きるほど燃える逆境力。",
        "weakness": "・つい論破して人間関係を壊す。\n・口だけで実務を丸投げしがち。\n・ルールに反抗して不要な摩擦を生む。",
        "mentor": "ツンデレな指導員"
    },
    "ESTJ": {
        "name": "幹部",
        "animal": "誠実な番犬",
        "catchphrase": "「揺るぎない正義感で、秩序と平和を守り抜く」",
        "strength": "・効率的に組織を回す司令塔。\n・ルールと伝統を守る安心感。\n・背中で語るリーダーシップ。",
        "weakness": "・自分のやり方が唯一の正解だと思いがち。\n・感情的フォローを「無駄」と切り捨てる。\n・柔軟な変化についていけない。",
        "mentor": "論理的なビジネスコーチ"
    },
    "ESFJ": {
        "name": "領事",
        "animal": "お世話好きなゾウ",
        "catchphrase": "「大きな愛でみんなを包む、コミュニティの守護神」",
        "strength": "・周囲の不満や困りごとを把握する力。\n・人と人を繋ぐ場作りの天才。\n・自分より「みんな」を優先する温かさ。",
        "weakness": "・人から嫌われるとパニックになる。\n・お節介がすぎて煙たがられる。\n・常識外の人を陰で批判しがち。",
        "mentor": "優しさに溢れるメンター (Default)"
    },
    "ENFJ": {
        "name": "主人公",
        "animal": "情熱的なライオン",
        "catchphrase": "「みんなの可能性を信じ、光差す方へ導く太陽」",
        "strength": "・他人の成長を自分以上に喜ぶ導き手。\n・周囲の心に火をつけるカリスマ性。\n・感情と論理の仲裁役としてのバランス。",
        "weakness": "・他人の問題を背負い込みすぎて自滅する。\n・嫌われるのを恐れて厳しいことが言えない。\n・期待に応えない人に密かに失望する。",
        "mentor": "頼れるお姉さん"
    },
    "ENTJ": {
        "name": "指揮官",
        "animal": "威風堂々なワシ",
        "catchphrase": "「高みから未来を見据え、勝利への最短距離を飛ぶ」",
        "strength": "・困難を力技で成功させる意志力。\n・ライバルを圧倒する努力量。\n・客観的で冷徹なまでの判断力。",
        "weakness": "・成果のない人を容赦なく切り捨てる。\n・独裁的な振る舞いになりがち。\n・プライベートを疎かにしすぎる。",
        "mentor": "論理的なビジネスコーチ"
    }
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

        # 具体的解説セクション
        st.markdown("### 🔍 あなたの詳しい性格分析")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"✨ **ここがあなたの武器（強み）**\n\n{detail['strength']}")
        with col2:
            st.warning(f"⚠️ **ここに注意（気をつけたい点）**\n\n{detail['weakness']}")

        st.divider()

        # 🤝 メンター指名セクション
        st.markdown("### 🤝 今日のメンターを指名する")
        selected_mentor = st.selectbox(
            "指名されたメンターから、今のあなたにピッタリなアドバイスを贈ります。",
            options=list(mentor_data.keys()),
            index=list(mentor_data.keys()).index(detail["mentor"]) if detail["mentor"] in mentor_data else 5
        )

        m_info = mentor_data[selected_mentor]
        st.chat_message("assistant").write(f"**{selected_mentor}**：「{m_info['quote']}」")
        
        current_action = random.choice(m_info['actions'])
        st.success(f"🎁 **今日のラッキーアクション**：{current_action}")

        # --- 7. 保存機能 ---
        report_text = f"""【MBTI性格診断 Pro レポート】
日時: 2025年12月23日 05:52
判定結果: {full_res}（{detail['name']}）

■ あなたの強み
{detail['strength']}

■ 注意点
{detail['weakness']}

■ メンター: {selected_mentor}
■ ラッキーアクション: {current_action}
"""
        st.download_button(
            label="診断結果をダウンロードして保存 📥",
            data=report_text,
            file_name=f"MBTI_Result_{full_res}.txt",
            mime="text/plain",
            use_container_width=True
        )

if __name__ == "__main__":
    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False
    run_mbti_diagnostic()
