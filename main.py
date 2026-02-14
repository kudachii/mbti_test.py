import streamlit as st
import plotly.graph_objects as go
import random

def run_perfect_imperial_diagnostic():
    # --- 1. 質問データ (32問) ---
    questions = [
        # [性格 24問 / 恋愛 8問]
        ("初対面の人が多い場所でも、自分から進んで会話を楽しむ", "E-I", 1),
        ("週末は外に出かけるよりも、家でゆっくり一人で過ごす方が回復する", "E-I", -1),
        ("グループの中心で注目を浴びることに抵抗がない", "E-I", 1),
        ("考えをまとめる時は、話しながらよりも書き出しながらの方が捗る", "E-I", -1),
        ("具体的な事実やデータを重視する", "S-N", 1),
        ("直感やインスピレーションを信じる", "S-N", -1),
        ("物事の仕組みや論理に興味がある", "S-N", 1),
        ("物語や象徴的なイメージが好きだ", "S-N", -1),
        ("論理的に正しいかどうかを優先する", "T-F", 1),
        ("人の感情や調和を優先する", "T-F", -1),
        ("客観的な真実が大切だと思う", "T-F", 1),
        ("相手の気持ちに寄り添いたい", "T-F", -1),
        ("予定を立てて行動するのが好きだ", "J-P", 1),
        ("その場の流れに任せるのが好きだ", "J-P", -1),
        ("整理整頓されていると安心する", "J-P", 1),
        ("自由な状態でいたい", "J-P", -1),
        ("自分に自信がある", "A-T", 1),
        ("周囲の目が気になりやすい", "A-T", -1),
        ("ストレスに強い方だ", "A-T", 1),
        ("完璧主義で自分を責めやすい", "A-T", -1),
        ("経験を重視する", "S-N", 1),
        ("感情を出すのは苦手だ", "T-F", 1),
        ("臨機応変な対応が得意だ", "J-P", -1),
        ("誰かと繋がっていたい", "E-I", 1),
        # [恋愛 8問]
        ("デートは自分がリードしたい", "L-F", 1),
        ("相手のペースに合わせるのが楽だ", "L-F", -1),
        ("恋人には甘えたい", "C-A", 1),
        ("恋人を守り、尽くしたい", "C-A", -1),
        ("恋愛でも経済力を重視する", "R-P", 1),
        ("恋には情熱的にのめり込む", "R-P", -1),
        ("束縛のない自由な関係がいい", "O-E", 1),
        ("結婚を見据えた誠実な付き合いがいい", "O-E", -1),
    ]

    # --- 2. 16タイプ別・完全データベース ---
    mbti_db = {
        "INTJ": {"name": "建築家", "animal": "トラ", "best_match": "ENTP", "lucky_pool": ["戦略的なゲームで遊ぶ", "未読の本を1章だけ読む", "中長期の貯金計画を立てる", "あえて無駄な散歩をする"]},
        "INTP": {"name": "論理学者", "animal": "チンパンジー", "best_match": "ENTJ", "lucky_pool": ["パズルや謎解きに挑戦する", "新しいガジェットを調べる", "積読本を1冊片付ける", "独り言で思考を整理する"]},
        "ENTJ": {"name": "指揮官", "animal": "ワシ", "best_match": "INTP", "lucky_pool": ["高い場所から景色を眺める", "誰かに仕事を任せてみる", "新しい目標を紙に書き出す", "靴をピカピカに磨く"]},
        "ENTP": {"name": "討論者", "animal": "キツネ", "best_match": "INTJ", "lucky_pool": ["新しいカフェを開拓する", "あえて反対意見を聞いてみる", "アイデアをノートに書き殴る", "知らない駅で降りてみる"]},
        "INFJ": {"name": "提唱者", "animal": "フクロウ", "best_match": "ENFJ", "lucky_pool": ["キャンドルを灯して瞑想する", "誰にも見せない日記を書く", "ハーブティーを飲む", "自然豊かな公園を歩く"]},
        "INFP": {"name": "仲介者", "animal": "ウサギ", "best_match": "ENFP", "lucky_pool": ["詩や小説の1節を書き写す", "空の写真を撮る", "懐かしい映画を観る", "一人の世界に没頭する"]},
        "ENFJ": {"name": "主人公", "animal": "ライオン", "best_match": "INFJ", "lucky_pool": ["友人に手紙やLINEを送る", "ボランティアや手助けをする", "明るい色の服を着る", "鏡の中の自分を褒める"]},
        "ENFP": {"name": "広報運動家", "animal": "カワウソ", "best_match": "INFP", "lucky_pool": ["カラオケで大声を出す", "派手な文房具を買う", "新しいコミュニティに参加する", "直感で夕食を決める"]},
        "ISTJ": {"name": "管理者", "animal": "ビーバー", "best_match": "ESFJ", "lucky_pool": ["デスクの引き出しを掃除する", "ルーチンを完璧にこなす", "時計の時間を合わせる", "和食を丁寧に食べる"]},
        "ISFJ": {"name": "擁護者", "animal": "シカ", "best_match": "ESTJ", "lucky_pool": ["家族や友人に料理を作る", "花を飾る", "リネン類を洗濯する", "人の話を聞き役に徹する"]},
        "ESTJ": {"name": "幹部", "animal": "番犬", "best_match": "ISFJ", "lucky_pool": ["筋トレで汗を流す", "リーダーシップを発揮する", "ToDoリストを全部消す", "早寝早起きを徹底する"]},
        "ESFJ": {"name": "領事", "animal": "ゾウ", "best_match": "ISTJ", "lucky_pool": ["手土産を持って誰かを訪ねる", "地域のイベントを調べる", "誰かの相談に乗る", "部屋にアロマを焚く"]},
        "ISTP": {"name": "巨匠", "animal": "サメ", "best_match": "ESTP", "lucky_pool": ["工具を使って何か直す", "一人でドライブやツーリング", "ソロキャンプの計画を立てる", "激辛料理を食べる"]},
        "ISFP": {"name": "冒険家", "animal": "ネコ", "best_match": "ESFP", "lucky_pool": ["美術館に行く", "お気に入りの香水をつける", "楽器やアートに触れる", "猫の動画を見て癒やされる"]},
        "ESTP": {"name": "起業家", "animal": "チーター", "best_match": "ISTP", "lucky_pool": ["スポーツ観戦で盛り上がる", "新しいビジネスを空想する", "知らない人に挨拶する", "エナジードリンクを飲む"]},
        "ESFP": {"name": "エンターテイナー", "animal": "レッサーパンダ", "best_match": "ISFP", "lucky_pool": ["賑やかな場所に出かける", "ダンスやストレッチをする", "新作のスイーツを食べる", "SNSで楽しい投稿をする"]},
    }

    # A/T別補足
    at_db = {"A": "自己主張型：前向きでストレスに強い", "T": "慎重型：繊細で向上心が強い"}

    if "show_result" not in st.session_state: st.session_state["show_result"] = False

    # --- 画面描画 ---
    if not st.session_state["show_result"]:
        st.title("精密性格・恋愛LCRO 統合診断")
        # 質問ループ (一部省略、実際は全問表示)
        for i, (q_text, axis, _) in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q_text}**")
            st.radio(f"radio_{i}", options=[1, 2, 3, 4, 5], key=f"q_{i}", horizontal=True, index=None)
        
        if st.button("結果を表示"):
            st.session_state["show_result"] = True
            st.rerun()
    else:
        # スコア計算
        scores = {ax: 0 for ax in ["E-I", "S-N", "T-F", "J-P", "A-T", "L-F", "C-A", "R-P", "O-E"]}
        for i, (_, axis, _) in enumerate(questions):
            val = st.session_state.get(f"q_{i}", 3)
            scores[axis] += (val - 3)

        m_core = ("E" if scores["E-I"] >= 0 else "I") + ("S" if scores["S-N"] >= 0 else "N") + \
                 ("T" if scores["T-F"] >= 0 else "F") + ("J" if scores["J-P"] >= 0 else "P")
        at_suffix = "A" if scores["A-T"] >= 0 else "T"
        
        res = mbti_db.get(m_core)
        
        # 【重要】ラッキーアクションのランダム選出
        if "final_lucky" not in st.session_state:
            st.session_state["final_lucky"] = random.choice(res["lucky_pool"])

        st.header(f"判定：{m_core}-{at_suffix}")
        st.markdown(f"### 動物：{res['animal']} ({res['name']})")
        
        # 表示！
        st.success(f"🌟 **今週のラッキーアクション**\n\n「 {st.session_state['final_lucky']} 」")
        st.info(at_db[at_suffix])

        if st.button("再診断"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    run_perfect_imperial_diagnostic()
