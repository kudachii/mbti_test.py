import streamlit as st
import plotly.graph_objects as go
import random # ← ランダム選択のために追加！

def run_mbti_diagnostic():
    st.set_page_config(page_title="MBTI性格診断 Pro", page_icon="🧠", layout="wide")

    st.markdown('<h3 style="font-size: 26px; font-weight: bold; color: #4A90E2;">🧠 性格タイプ診断 Pro (ラッキーアクション版)</h3>', unsafe_allow_html=True)

    # 質問データ（24問）
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

    # --- 進捗管理 ---
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

    # --- 質問表示 ---
    user_answers = {}
    for i, (q_text, axis, weight) in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q_text}**")
        user_answers[i] = st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5], 
                                   format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                                   key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
        st.write("---")

    # --- 診断実行 ---
    if st.button("診断結果を詳しく見る ✨", use_container_width=True):
        if answered_count < len(questions):
            st.error(f"まだ未回答の質問があるよ！（残り {len(questions) - answered_count} 問）")
        else:
            st.balloons()
            
            # スコア計算
            scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0, "A-T": 0}
            for i, (q_text, axis, weight) in enumerate(questions):
                scores[axis] += (user_answers[i] - 3) * weight

            mbti_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                        ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
            identity = "-A" if scores["A-T"] >= 0 else "-T"
            full_res = mbti_core + identity

            # メンター・詳細データ
            mbti_details = {
                "ISTJ": {"name": "管理者", "mentor": "論理的なビジネスコーチ"},
                "ISFJ": {"name": "擁護者", "mentor": "優しさに溢れるメンター (Default)"},
                "INFJ": {"name": "提唱者", "mentor": "頼れるお姉さん"},
                "INTJ": {"name": "建築家", "mentor": "カサネ・イズミ：論理と不確定要素"},
                "ISTP": {"name": "巨匠", "mentor": "ツンデレな指導員"},
                "ISFP": {"name": "冒険家", "mentor": "ギャル先生"},
                "INFP": {"name": "仲介者", "mentor": "頼れるお姉さん"},
                "INTP": {"name": "論理学者", "mentor": "カサネ・イズミ：論理と不確定要素"},
                "ESTP": {"name": "起業家", "mentor": "ツンデレな指導員"},
                "ESFP": {"name": "エンターテイナー", "mentor": "ギャル先生"},
                "ENFP": {"name": "広報運動家", "mentor": "ギャル先生"},
                "ENTP": {"name": "討論者", "mentor": "ツンデレな指導員"},
                "ESTJ": {"name": "幹部", "mentor": "論理的なビジネスコーチ"},
                "ESFJ": {"name": "領事", "mentor": "優しさに溢れるメンター (Default)"},
                "ENFJ": {"name": "主人公", "mentor": "頼れるお姉さん"},
                "ENTJ": {"name": "指揮官", "mentor": "論理的なビジネスコーチ"}
            }

            # --- ラッキーアクション用データ ---
            lucky_actions = {
                "ギャル先生": [
                    "「今日はコンビニの新作スイーツ買って、自分にご褒美あげちゃお！マジでお疲れ！✨」",
                    "「鏡の前で自分に『今日も可愛いじゃん』って言ってみて？セルフラブ大事だよ！💖」",
                    "「お気に入りの曲を爆音（イヤホンねｗ）で聴いて、テンションぶち上げてこ！🚀」"
                ],
                "頼れるお姉さん": [
                    "「今日は5分だけ、デジタルデトックスをして温かい飲み物を飲んでみて。心の充電が必要よ。」",
                    "「寝る前に、今日頑張ったことを3つ思い出してみて？あなたは十分素敵よ。」",
                    "「少し高めの入浴剤を使って、お風呂でゆっくりしてね。自分をいたわってあげて。」"
                ],
                "カサネ・イズミ：論理と不確定要素": [
                    "「散らかったデスクを整理しろ。外部環境の最適化は、思考の最適化に直結する。」",
                    "「新しい技術や知識を15分だけ調べろ。その積み重ねがあなたの価値を形成する。」",
                    "「カフェインを摂取し、タスクの優先順位を再構築しろ。効率がすべてだ。」"
                ],
                "ツンデレな指導員": [
                    "「ちょっと！姿勢が悪いわよ。背筋を伸ばしなさい！シャキッとするでしょ？」",
                    "「あんた、たまには遠くの景色でも見なさいよね。ずっと画面見てると目に悪いでしょ…心配してないわよ！」",
                    "「今日はいつもより10分早く行動しなさい。余裕のないあんたなんて見たくないんだからね。」"
                ],
                "論理的なビジネスコーチ": [
                    "「今日一番重要なタスクを1つだけ選んで、午前中に完了させよう。成果は集中力に比例する。」",
                    "「靴を磨け。細部へのこだわりが、他者からの信頼を生む。」",
                    "「会いたい人に連絡を取り、情報交換の場をセットしよう。人脈は資産だ。」"
                ],
                "優しさに溢れるメンター (Default)": [
                    "「深呼吸を3回しましょう。空気が体に入るのを感じるだけで、心は落ち着きますよ。」",
                    "「道端に咲いている花に目を向けてみてください。小さな幸せがあなたを待っています。」",
                    "「大切な人に、ありがとうと伝えてみませんか？言葉は魔法になります。」"
                ]
            }

            detail = mbti_details.get(mbti_core)
            mentor_name = detail["mentor"]
            
            # 結果表示
            st.divider()
            st.markdown(f"## 判定結果：{full_res}（{detail['name']}）")

            # チャート表示
            categories = ['外向(E)', '感覚(S)', '思考(T)', '判断(J)', '自己主張(A)']
            values = [scores["E-I"], scores["S-N"], scores["T-F"], scores["J-P"], scores["A-T"]]
            fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-12, 12])), showlegend=False)
            st.plotly_chart(fig)

            # --- ラッキーアクション表示エリア ---
            action = random.choice(lucky_actions.get(mentor_name, ["今日はゆっくり休んでね。"]))
            st.markdown(f"### 🎁 {mentor_name} からのラッキーアクション")
            st.warning(f"**{action}**")
            
            st.info(f"💡 **あなたのタイプ診断**\n\n判定タイプ: {full_res}\nこの結果をもとに、今日は少しだけ特別なアクションを試してみてね！")

if __name__ == "__main__":
    run_mbti_diagnostic()
