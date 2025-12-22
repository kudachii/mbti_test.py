import streamlit as st
import plotly.graph_objects as go
import random

def run_mbti_diagnostic():
    st.set_page_config(page_title="MBTI性格診断 Pro", page_icon="🧠", layout="wide")

    st.markdown('<h3 style="font-size: 26px; font-weight: bold; color: #4A90E2;">🧠 性格タイプ診断 Pro (完全レスポンシブVer.)</h3>', unsafe_allow_html=True)
    st.caption("2025年12月23日 06:57：PCとスマホ、両方の視認性を最大化しました。")

    # (中略: 質問データ 24問)
    # --- 1. 質問データ ---
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

    # --- 2. メンターデータ (省略) ---
    mentor_data = {
        "ギャル先生": {"quote": "「おはよー！あんたの魅力、バズり確定じゃん！✨」", "actions": ["「自分にご褒美あげちゃお！✨」"]},
        "頼れるお姉さん": {"quote": "「一生懸命なところ、素敵よ。甘えていいのよ？」", "actions": ["「5分だけデジタルデトックスして。」"]},
        "カサネ・イズミ": {"quote": "「あなたのデータは特異だ。思考を最適化しろ。」", "actions": ["「デスクを整理しろ。」"]},
        "ツンデレな指導員": {"quote": "「しっかりしなさいよ！危なっかしいわね。」", "actions": ["「姿勢を正しなさい！」"]},
        "ビジネスコーチ": {"quote": "「戦略を練ろう。まずは現状分析だ。」", "actions": ["「重要課題を1つ決めて集中しよう。」"]},
        "優しいメンター": {"quote": "「あなたは今のままで十分素晴らしいですよ。」", "actions": ["「深呼吸をゆっくり3回しましょう。」"]}
    }

    # --- 3. 性格タイプ詳細DB (16タイプ具体版 - 前回の内容を継承) ---
    # (コードが長くなりすぎるため、ここでは主要データのみ記述)
    mbti_db = {
        "INFJ": {"name": "提唱者", "strength": "洞察力、理想主義、深い共感", "weakness": "完璧主義、燃え尽きやすい", "mentor": "頼れるお姉さん"},
        "ENFP": {"name": "広報運動家", "strength": "情熱、コミュ力、可能性の発見", "weakness": "集中力の分散、事務が苦手", "mentor": "ギャル先生"},
        # ... 他の14タイプも実際にはここに含まれます
    }

    # --- 4. 進捗管理：【ダブル表示システム】 ---
    answered_count = 0
    for i in range(len(questions)):
        if f"q_{i}" in st.session_state and st.session_state[f"q_{i}"] is not None:
            answered_count += 1
    
    progress_per = answered_count / len(questions)

    # A. サイドバー (PC用：スクロールしても固定)
    with st.sidebar:
        st.header("📊 PC用進捗")
        st.progress(progress_per)
        st.write(f"**{answered_count} / {len(questions)} 問** 回答済み")
        st.divider()
        st.markdown("**ギャル先生からの応援**")
        if progress_per < 0.5: st.write("「まずは直感でポチポチいこー！✨」")
        elif progress_per < 1.0: st.write("「いい感じ！半分超えたよ！🔥」")
        else: st.write("「完璧！ボタン押しちゃいな！💖」")

    # B. メイン上部 (スマホ用：サイドバーが隠れても見失わない)
    st.markdown(f"**📊 現在の進捗: {answered_count} / {len(questions)} 問**")
    st.progress(progress_per)
    st.write("---")

    # --- 5. 質問表示 ---
    for i, (q_text, axis, weight) in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q_text}**")
        st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5], 
                 format_func=lambda x: {1: "全く違う", 2: "違う", 3: "中立", 4: "そう思う", 5: "強くそう思う"}[x],
                 key=f"q_{i}", label_visibility="collapsed", horizontal=True, index=None)
        st.write("---")

    # (以下、診断実行・結果表示・保存機能は前回と同じ)
    if st.button("診断結果を詳しく見る ✨", use_container_width=True):
        if answered_count < len(questions):
            st.error(f"まだ回答していない質問があるよ！（残り {len(questions) - answered_count} 問）")
        else:
            st.session_state["show_result"] = True
    
    # ... (結果表示ロジックは前回通り)

if __name__ == "__main__":
    if "show_result" not in st.session_state:
        st.session_state["show_result"] = False
    run_mbti_diagnostic()
