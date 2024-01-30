import streamlit as st
import openai
import json


# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    initial_content = str(st.secrets.AppSettings.chatbot_setting)
    st.session_state["messages"] = [
        {"role": "system", "content": initial_content}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=messages
        )

        bot_message_content = response["choices"][0]["message"]["content"] if "content" in response["choices"][0]["message"] else response["choices"][0]["message"]
        bot_message = {"role": "assistant", "content": bot_message_content}
        messages.append(bot_message)

    except Exception as e:
        st.error(f"APIリクエストでエラーが発生しました: {e}")
        st.write("エラー時のメッセージ履歴:")
        st.json(messages)  # エラー時のメッセージ履歴を表示
        return

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("QUICKFIT BOT")
st.write("Quick fitに関するQ&A AIBOT")

# メッセージ表示用のコンテナ
messages_container = st.container()

if st.session_state.get("messages"):
    messages = st.session_state["messages"]

    for message in messages:
        # システムメッセージはスキップする
        if message["role"] == "system":
            continue

        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"

        content = message["content"]
        if not isinstance(content, str):
            content = str(content)

        messages_container.write(speaker + ": " + content)

# メッセージ表示用のコンテナ
messages_container = st.container()
with messages_container:
    for message in reversed(st.session_state["messages"]):
        if message["role"] == "system":
            continue
        speaker = "🙂" if message["role"] == "user" else "🤖"
        content = message["content"]
        st.text_area("", value=content, disabled=True, height=70)

# 下へスクロールするためのボタン
st.markdown("""
    <a class="scrollToBottom" href="javascript:void(0);" onclick="window.scrollTo(0,document.body.scrollHeight);">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path d="M24 22h-24l12-20z"/>
        </svg>
    </a>
    <style>
        .scrollToBottom {
            position: fixed;
            bottom: 20px;
            right: 20px;
            cursor: pointer;
        }
        .scrollToBottom svg {
            fill: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)

# メッセージ入力
user_input = st.text_input("メッセージを入力してください。", key="user_input")

# 送信ボタン
if st.button('送信'):
    communicate(user_input)
    st.session_state["user_input"] = ""  # 入力欄を消去

# 最新のメッセージに自動スクロールするJavaScript
st.markdown("""
    <script>
        const messagesContainer = document.querySelector('.element-container:last-child');
        if(messagesContainer) {
            messagesContainer.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    </script>
""", unsafe_allow_html=True)