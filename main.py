import streamlit as st
import plotly.graph_objects as go

def run_mbti_diagnostic():
    st.set_page_config(page_title="MBTI性格診断 Pro", page_icon="🧠", layout="wide")

    # タイトル
    st.markdown('<h3 style="font-size: 26px; font-weight: bold; color: #4A90E2;">🧠 性格タイプ診断 Pro (完全未選択スタート版)</h3>', unsafe_allow_html=True)
    st.caption("24個の質問に答えて、あなたの性格タイプとメンターを判定します。最初は未選択の状態です。")

    # 質問データ
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

    # --- 進捗の計算 (session_stateに値があるかチェック) ---
    answered_count = 0
    for i in range(len(questions)):
        key = f"q_{i}"
        # 値が None（未選択）でない場合のみカウント
        if key in st.session_state and st.session_state[key] is not None:
            answered_count += 1
    
    # --- サイドバーに進捗バーを表示 ---
    with st.sidebar:
        st.header("📊 診断の進捗")
        progress_per = answered_count / len(questions)
        st.progress(progress_per)
        st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
        
        if answered_count == len(questions):
            st.success("✨ 全問回答完了！結果を見よう！ ✨")
        else:
            st.info("質問をポチッと選ぶとバーが伸びるよ！")
        
        st.divider()
        # メンターからの応援メッセージ（サイドバー版）
        st.markdown("**ギャル先生からのひと言**")
        if progress_per < 0.5:
            st.write("「まずは直感でポチポチいこー！✨」")
        elif progress_per < 1.0:
            st.write("「いい感じ！半分超えたよ、あと少し！🔥」")
        else:
            st.write("「完璧！あんたマジ最高！診断ボタン押しちゃいな！💖」")

    # --- 質問表示エリア ---
    user_answers = {}
    for i, (q_text, axis, weight) in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q_text}**")
        # index=None にすることで初期選択を解除
        user_answers[i] = st.radio(
            f"radio_{i}", 
            options=[1, 2, 3, 4, 5], 
            format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
            key=f"q_{i}", 
            label_visibility="collapsed", 
            horizontal=True,
            index=None  # ← ここが重要！
        )
        st.write("---")

    # --- 診断実行ボタン ---
    if st.button("診断結果を詳しく見る ✨", use_container_width=True):
        if answered_count < len(questions):
            st.error(f"まだ回答していない質問があるよ！（残り {len(questions) - answered_count} 問）")
        else:
            st.balloons()
            
            # スコア計算
            current_scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0}
            for i, (q_text, axis, weight) in enumerate(questions):
                current_scores[axis] += (user_answers[i] - 3) * weight

            # 判定ロジック・メンター・チャート表示 (前回のコードを継承)
            mbti_core = ("E" if current_scores["E-I"] >= 0 else "I") + \
                        ("S" if current_scores["S-N"] >= 0 else "N") + \
                        ("T" if current_scores["T-F"] >= 0 else "F") + \
                        ("J" if current_scores["J-P"] >= 0 else "P")
            identity = "-A" if current_scores["A-T"] >= 0 else "-T"
            full_res = mbti_core + identity

            # メンターデータ
            mbti_details = {
                "ISTJ": {"name": "管理者", "desc": "真面目で実用的。秩序とルールを重んじる誠実な人です。", "mentor": "論理的なビジネスコーチ"},
                "ISFJ": {"name": "擁護者", "desc": "献身的で温かい。周囲の人を静かに支える守護者です。", "mentor": "優しさに溢れるメンター (Default)"},
                "INFJ": {"name": "提唱者", "desc": "理想主義で洞察力が鋭い。静かながら強い信念を持っています。", "mentor": "頼れるお姉さん"},
                "INTJ": {"name": "建築家", "desc": "戦略的で完璧主義。常に知識と論理で最適解を求めます。", "mentor": "カサネ・イズミ：論理と不確定要素"},
                "ISTP": {"name": "巨匠", "desc": "冷静で器用。観察力が鋭く、トラブル解決が得意です。", "mentor": "ツンデレな指導員"},
                "ISFP": {"name": "冒険家", "desc": "感性豊かで自由を愛する。自分らしく生きるアーティストです。", "mentor": "ギャル先生"},
                "INFP": {"name": "仲介者", "desc": "繊細で理想家。自分の価値観を大切にする心優しい人です。", "mentor": "頼れるお姉さん"},
                "INTP": {"name": "論理学者", "desc": "独創的な理論家。知的好奇心が強く、分析が大好きです。", "mentor": "カサネ・イズミ：論理と不確定要素"},
                "ESTP": {"name": "起業家", "desc": "行動的でエネルギッシュ。スリルと変化を好む挑戦者です。", "mentor": "ツンデレな指導員"},
                "ESFP": {"name": "エンターテイナー", "desc": "明るく友好的。周囲を楽しませるムードメーカーです。", "mentor": "ギャル先生"},
                "ENFP": {"name": "広報運動家", "desc": "情熱的で自由奔放。可能性を見つける天才です。", "mentor": "ギャル先生"},
                "ENTP": {"name": "討論者", "desc": "知的で好奇心旺盛。新しいアイデアで常識を疑う発明家です。", "mentor": "ツンデレな指導員"},
                "ESTJ": {"name": "幹部", "desc": "組織的で現実的。物事を効率よく進めるリーダーです。", "mentor": "論理的なビジネスコーチ"},
                "ESFJ": {"name": "領事", "desc": "社交的で世話好き。調和を大切にする、皆のまとめ役です。", "mentor": "優しさに溢れるメンター (Default)"},
                "ENFJ": {"name": "主人公", "desc": "カリスマ性があり共感的。人々を導き、励ますリーダーです。", "mentor": "頼れるお姉さん"},
                "ENTJ": {"name": "指揮官", "desc": "大胆で意志が強い。目標達成のために道を切り拓く戦略家です。", "mentor": "論理的なビジネスコーチ"}
            }
            
            mentor_quotes = {
                "カサネ・イズミ：論理と不確定要素": "「あなたのデータは極めて特異だ。その思考を最適化すれば、さらなる高みへ到達できる。」",
                "論理的なビジネスコーチ": "「あなたの能力を最大限に活かすための戦略を練ろう。まずは現状の分析からだ。」",
                "頼れるお姉さん": "「一生懸命なところ、素敵よ。でもたまには肩の力を抜いて、私に甘えていいのよ？」",
                "優しさに溢れるメンター (Default)": "「あなたは今のままで十分素晴らしいですよ。一緒に、一歩ずつ進んでいきましょうね。」",
                "ツンデレな指導員": "「ふん、あんたみたいなタイプは私が付いてないと危なっかしいわね。しっかりしなさいよ！」",
                "ギャル先生": "「おはよー！あんたの魅力、マジでバズり確定じゃん！✨ その調子で今日もハピネスに、自分軸でブチ上げてこー！💖」"
            }

            detail = mbti_details.get(mbti_core)

            # 結果表示
            st.divider()
            st.markdown(f"## 判定結果：{full_res}（{detail['name']}）")

            # レーダーチャート
            categories = ['外向(E)', '感覚(S)', '思考(T)', '判断(J)', '自己主張(A)']
            values = [current_scores["E-I"], current_scores["S-N"], current_scores["T-F"], current_scores["J-P"], current_scores["A-T"]]
            fig = go.Figure(data=go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                line_color='#4A90E2',
                fillcolor='rgba(74, 144, 226, 0.3)'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-12, 12])), showlegend=False, title="📊 性格バランスチャート")
            st.plotly_chart(fig, use_container_width=True)

            # メッセージ
            st.info(f"💡 **あなたの特徴 ({identity})**\n\n{detail['desc']}\n\n" + 
                    ("あなたは自信に満ち、ストレス下でも安定を保てるタイプです。" if identity == "-A" else "あなたは向上心が強く、自分を磨き続ける繊細な努力家です。"))
            st.success(f"📌 **おすすめメンター：{detail['mentor']}**")
            st.warning(f"💬 **メンターからのメッセージ**\n\n*{mentor_quotes.get(detail['mentor'])}*")

if __name__ == "__main__":
    run_mbti_diagnostic()
