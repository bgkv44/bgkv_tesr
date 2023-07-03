import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from gtts import gTTS

# Ваши данные авторизации VK
VK_TOKEN = 'vk1.a.9Un3zv5v1nePrxDaG-N3ZKdswyn_nU3-nWWBtszmZS-g9zM0LUt6KrV2arjHOSJiQEfZo-mwgCbC3j0HBURj5gcoOftEtOz5tGxHmTRfBTSfQfR34beE03gmebxfaHqJkIgYlL9JYtQ0LU0I1k9MeZKB_aHBkue9wwXVOqkBvf2w7bS5z4zkmdBbZHnlLdFu7D8rR35zuhUd0vIBSKvgpA'

def text_to_speech(text):
    # Преобразование текста в речь
    tts = gTTS(text=text, lang='ru')
    tts.save('voice.mp3')

def send_voice_message(vk, peer_id, message):
    # Преобразование текста в речь
    text_to_speech(message)

    # Отправка голосового сообщения
    upload = vk_api.VkUpload(vk)
    audio = upload.audio_message('voice.mp3', peer_id=peer_id)
    attachment = f"doc{audio['audio_message']['owner_id']}_{audio['audio_message']['id']}"
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )

def handle_new_message(event, vk):
    if event.text:
        # Преобразование текстового сообщения в голосовое
        send_voice_message(vk, event.peer_id, event.text)

def main():
    # Авторизация в VK
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_new_message(event, vk)

if __name__ == '__main__':
    main()
