import flet as ft


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
                content=ft.Text(self.get_initials(message.user_name)),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
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
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
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
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    join_user_name = ft.TextField(
        autofocus=True,
        on_submit=join_chat_click,
        label="Informe seu nome.",
    )

    # Chat messages
    chat = ft.ListView(
        spacing=10,
        expand=True,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        autofocus=True,
        shift_enter=True,
        on_submit=send_message_click,
        hint_text="Escreva uma mensagem...",
    )

    page.dialog = ft.AlertDialog(
        open=False,
        modal=True,
        actions_alignment="end",
        title=ft.Text("Bem Vindo!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Entrar no chat", on_click=join_chat_click)],
    )

    # Add everything to the page
    page.add(
        ft.Container(
            padding=10,
            expand=True,
            content=chat,
            border_radius=5,
            border=ft.border.all(1, ft.colors.OUTLINE),
        ),
        ft.Row([
            new_message,
            ft.IconButton(
                tooltip="Envia mensagem",
                icon=ft.icons.SEND_ROUNDED,
                on_click=send_message_click,
            )
        ])
    )


ft.app(port=3000, target=main, view=ft.WEB_BROWSER)
