from flet import Page, Text, colors, app,\
    TextField, ListView, AlertDialog, icons, \
    ElevatedButton, Column, MainAxisAlignment,\
    Container, border, Row, IconButton, WEB_BROWSER

from classes.message import Message
from classes.chat_message import ChatMessage


def main(page: Page):
    page.horizontal_alignment = "stretch"
    page.title = "Chat"

    def open_dialog():
        page.dialog.open = True
        page.update()

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "O nome não pode ficar vazio!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(user_name=join_user_name.value, text=f"{join_user_name.value} entrou no chat.",
                        message_type="login_message"))
            page.update()

    def send_message_click(e):
        if page.session.get("user_name") is None:
            open_dialog()
        elif new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
            chat.controls.append(m)
        elif message.message_type == "login_message":
            m = Text(message.text, italic=True, color=colors.BLACK45, size=12)
            chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    join_user_name = TextField(
        autofocus=True,
        on_submit=join_chat_click,
        label="Informe seu nome.",
    )

    # Chat messages
    chat = ListView(
        spacing=10,
        expand=True,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = TextField(
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        autofocus=True,
        shift_enter=True,
        on_submit=send_message_click,
        hint_text="Escreva uma mensagem...",
    )

    page.dialog = AlertDialog(
        open=False,
        modal=True,
        actions_alignment=MainAxisAlignment.END,
        title=Text("Bem Vindo!"),
        content=Column([join_user_name], width=300, height=70, tight=True),
        actions=[ElevatedButton(text="Entrar no chat", on_click=join_chat_click)],
    )

    # Add everything to the page
    page.add(
        Container(
            padding=10,
            expand=True,
            content=chat,
            border_radius=5,
            border=border.all(1, colors.OUTLINE),
        ),
        Row([
            new_message,
            IconButton(
                tooltip="Envia mensagem",
                icon=icons.SEND_ROUNDED,
                on_click=send_message_click,
            )
        ])
    )


app(port=3000, target=main, view=WEB_BROWSER)
