import streamlit as st

def run_mbti_diagnostic():
    # タイトルを小さく、1行に収まるようにHTMLで指定
    st.markdown('<h3 style="font-size: 20px; font-weight: bold; margin-bottom: 5px;">🧠 性格タイプ診断 (MBTIプロトタイプ)</h3>', unsafe_allow_html=True)
    st.caption("20個の質問に答えて、あなたの性格タイプを判定します。")

    # 4つの指標のスコア
    scores = {"E-I": 0, "S-N": 0, "T-F": 0, "J-P": 0}

    # 質問データ定義
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
    ]

    # 回答フォーム
    with st.form("mbti_form"):
        for i, (q_text, axis, weight) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            ans = st.radio(
                f"q_{i}",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                label_visibility="collapsed",
                horizontal=True,
                index=2
            )
            scores[axis] += (ans - 3) * weight

        submit = st.form_submit_button("診断結果を出す ✨")

    if submit:
        # 判定ロジック
        mbti_type = ""
        mbti_type += "E" if scores["E-I"] > 0 else "I"
        mbti_type += "S" if scores["S-N"] > 0 else "N"
        mbti_type += "T" if scores["T-F"] > 0 else "F"
        mbti_type += "J" if scores["J-P"] > 0 else "P"

        # メンターとの紐付け設定
        mentor_mapping = {
            "T": "論理的なビジネスコーチ / カサネ・イズミ",
            "F": "優しさに溢れるメンター / 頼れるお姉さん",
            "TJ": "論理的なビジネスコーチ",
            "TP": "カサネ・イズミ",
            "FJ": "頼れるお姉さん",
            "FP": "優しさに溢れるメンター",
            "E": "ツンデレな指導員 (喝を入れてほしい場合)"
        }

        # 結果表示
        st.divider()
        st.balloons()
        st.subheader(f"あなたのタイプは: {mbti_type}")
        
        # 思考(T)か感情(F)かに基づいておすすめを表示
        key = mbti_type[2] # T or F
        recommended = mentor_mapping.get(key, "優しさに溢れるメンター")
        
        st.success(f"📌 あなたにピッタリのメンター: **{recommended}**")
        st.info("この結果を参考に、メインの日記アプリでメンターを切り替えてみてください。")

if __name__ == "__main__":
    run_mbti_diagnostic()
