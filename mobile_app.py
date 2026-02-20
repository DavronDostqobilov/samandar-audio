import flet as ft
import os
import threading

def main(page: ft.Page):
    page.title = "Audio Kitob Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#0c0e14"
    
    # Simple state
    current_category = "audiobooks"
    
    # UI Elements
    header = ft.Row(
        [
            ft.Icon(ft.icons.LIBRARY_MUSIC, color="#8b5cf6", size=30),
            ft.Text("Audio Kitob", size=24, weight=ft.FontWeight.BOLD),
            ft.Spacer(),
            ft.IconButton(ft.icons.MIC, icon_color="white", bgcolor="#8b5cf6")
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    hero = ft.Column(
        [
            ft.Text("Xush kelibsiz!", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Nima tinglashni xohlaysiz?", color="#94a3b8"),
        ],
        spacing=5
    )
    
    list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def play_item(title, author):
        show_player(title, author)
        
    def render_items(category):
        list_container.controls.clear()
        
        # Simulated data (In real version, we scan the folders)
        items = []
        if category == "audiobooks":
            items = [
                ("Sariq devni minib", "Xudayberdi To'xtaboyev"),
                ("O'tkan kunlar", "Abdulla Qodiriy"),
                ("Yulduzli tunlar", "Pirimqul Qodirov")
            ]
        else:
            items = [
                ("Lazgi", "Xorazm ansambli"),
                ("Dutor navosi", "Milliy cholg'ular")
            ]
            
        for title, author in items:
            list_container.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                bgcolor="#1a1d27",
                                width=60, height=60,
                                border_radius=10,
                                content=ft.Icon(ft.icons.BOOK if category=="audiobooks" else ft.icons.MUSIC_NOTE)
                            ),
                            ft.Column(
                                [
                                    ft.Text(title, weight=ft.FontWeight.W_600),
                                    ft.Text(author, size=12, color="#94a3b8"),
                                ],
                                spacing=0,
                                expand=True
                            ),
                            ft.IconButton(ft.icons.PLAY_ARROW_ROUNDED, icon_color="white")
                        ]
                    ),
                    bgcolor="#1a1d27",
                    padding=10,
                    border_radius=15,
                    border=ft.border.all(1, "#252a3a"),
                    on_click=lambda e, t=title, a=author: play_item(t, a)
                )
            )
        page.update()

    def change_tab(e):
        nonlocal current_category
        current_category = "audiobooks" if e.control.selected_index == 0 else "music"
        render_items(current_category)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Kitoblar", icon=ft.icons.BOOK),
            ft.Tab(text="Musiqalar", icon=ft.icons.MUSIC_NOTE),
        ],
        on_change=change_tab,
        divider_color="transparent",
        indicator_color="#8b5cf6",
        label_color="#8b5cf6",
        unselected_label_color="#94a3b8",
    )

    # Player Sheet
    def show_player(title, author):
        def close_sheet(e):
            bs.open = False
            bs.update()

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Row([ft.IconButton(ft.icons.KEYBOARD_ARROW_DOWN, on_click=close_sheet)], alignment=ft.MainAxisAlignment.START),
                        ft.Container(
                            bgcolor="#1a1d27",
                            width=250, height=250,
                            border_radius=20,
                            content=ft.Icon(ft.icons.MUSIC_VIDEO, size=100, color="#8b5cf6")
                        ),
                        ft.Column(
                            [
                                ft.Text(title, size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.Text(author, size=16, color="#94a3b8", text_align=ft.TextAlign.CENTER),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Slider(min=0, max=100, value=30, active_color="#8b5cf6"),
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.SKIP_PREVIOUS, icon_size=40),
                                ft.IconButton(ft.icons.PLAY_CIRCLE_FILL, icon_size=70, icon_color="#8b5cf6"),
                                ft.IconButton(ft.icons.SKIP_NEXT, icon_size=40),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=20)
                    ],
                    main_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                bgcolor="#0c0e14",
                border_radius=ft.border_radius.only(top_left=30, top_right=30)
            ),
            open=True,
        )
        page.overlay.append(bs)
        page.update()

    # Initial Render
    page.add(
        header,
        ft.Container(height=20),
        hero,
        ft.Container(height=20),
        tabs,
        ft.Container(height=10),
        list_container
    )
    
    render_items("audiobooks")

if __name__ == "__main__":
    # To run as a web app for testing: flet run mobile_app.py --web
    # To build APK: flet build apk
    ft.app(target=main)
