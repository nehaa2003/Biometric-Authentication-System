import threading
import customtkinter as ctk
from tkinter import messagebox

from biometric_system import (
    authenticate_face,
    capture_face_samples
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def run_app():
    app = ctk.CTk()

    app.title("Biometric Authentication System")
    app.geometry("900x650")
    app.resizable(False, False)

    # Theme colours
    background = "#0F172A"
    card_colour = "#172033"
    secondary_card = "#1E293B"
    primary = "#2563EB"
    primary_hover = "#1D4ED8"
    success_colour = "#22C55E"
    success_hover = "#16A34A"
    warning_colour = "#F59E0B"
    danger_colour = "#EF4444"
    text_primary = "#F8FAFC"
    text_secondary = "#94A3B8"
    border_colour = "#334155"

    app.configure(fg_color=background)

    def set_controls_state(state):
        register_button.configure(state=state)
        login_button.configure(state=state)
        username_entry.configure(state=state)

    def set_status(message, colour=text_secondary):
        status_label.configure(
            text=message,
            text_color=colour
        )

        status_dot.configure(
            text_color=colour
        )

    def show_result(is_successful, message):
        set_controls_state("normal")

        if is_successful:
            set_status(message, success_colour)
            messagebox.showinfo("Success", message)
        else:
            set_status(message, danger_colour)
            messagebox.showerror("Authentication", message)

    def register_user():
        username = username_entry.get().strip()

        if not username:
            messagebox.showwarning(
                "Missing Username",
                "Please enter a username before registering."
            )
            return

        set_controls_state("disabled")

        set_status(
            "Opening webcam for face registration...",
            warning_colour
        )

        def registration_task():
            try:
                success_value, result_message = capture_face_samples(username)

                app.after(
                    0,
                    lambda: show_result(
                        success_value,
                        result_message
                    )
                )

                if success_value:
                    app.after(
                        0,
                        lambda: username_entry.delete(0, "end")
                    )

            except Exception as error:
                app.after(
                    0,
                    lambda: show_result(
                        False,
                        f"Registration failed: {error}"
                    )
                )

        threading.Thread(
            target=registration_task,
            daemon=True
        ).start()

    def login_user():
        set_controls_state("disabled")

        set_status(
            "Opening webcam for biometric authentication...",
            warning_colour
        )

        def authentication_task():
            try:
                success_value, result_message = authenticate_face()

                app.after(
                    0,
                    lambda: show_result(
                        success_value,
                        result_message
                    )
                )

            except Exception as error:
                app.after(
                    0,
                    lambda: show_result(
                        False,
                        f"Authentication failed: {error}"
                    )
                )

        threading.Thread(
            target=authentication_task,
            daemon=True
        ).start()

    # Main container
    main_frame = ctk.CTkFrame(
        app,
        fg_color="transparent"
    )
    main_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=30
    )

    # Header
    header_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    header_frame.pack(
        fill="x",
        pady=(0, 25)
    )

    icon_label = ctk.CTkLabel(
        header_frame,
        text="◉",
        font=("Segoe UI", 34, "bold"),
        text_color=primary
    )
    icon_label.pack(
        side="left",
        padx=(0, 12)
    )

    header_text_frame = ctk.CTkFrame(
        header_frame,
        fg_color="transparent"
    )
    header_text_frame.pack(side="left")

    title_label = ctk.CTkLabel(
        header_text_frame,
        text="Biometric Authentication",
        font=("Segoe UI", 30, "bold"),
        text_color=text_primary
    )
    title_label.pack(anchor="w")

    subtitle_label = ctk.CTkLabel(
        header_text_frame,
        text="Secure face registration and identity verification",
        font=("Segoe UI", 14),
        text_color=text_secondary
    )
    subtitle_label.pack(
        anchor="w",
        pady=(4, 0)
    )

    # Content area
    content_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    content_frame.pack(
        fill="both",
        expand=True
    )

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

    # Registration card
    registration_card = ctk.CTkFrame(
        content_frame,
        fg_color=card_colour,
        corner_radius=18,
        border_width=1,
        border_color=border_colour
    )
    registration_card.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 12),
        pady=5
    )

    registration_badge = ctk.CTkLabel(
        registration_card,
        text="  NEW USER  ",
        font=("Segoe UI", 11, "bold"),
        text_color="#BFDBFE",
        fg_color="#1E3A8A",
        corner_radius=8
    )
    registration_badge.pack(
        anchor="w",
        padx=28,
        pady=(26, 18)
    )

    registration_title = ctk.CTkLabel(
        registration_card,
        text="Register Your Face",
        font=("Segoe UI", 22, "bold"),
        text_color=text_primary
    )
    registration_title.pack(
        anchor="w",
        padx=28
    )

    registration_description = ctk.CTkLabel(
        registration_card,
        text=(
            "Create a biometric profile by capturing\n"
            "face samples through your webcam."
        ),
        font=("Segoe UI", 13),
        text_color=text_secondary,
        justify="left"
    )
    registration_description.pack(
        anchor="w",
        padx=28,
        pady=(8, 24)
    )

    username_label = ctk.CTkLabel(
        registration_card,
        text="Username",
        font=("Segoe UI", 13, "bold"),
        text_color=text_primary
    )
    username_label.pack(
        anchor="w",
        padx=28,
        pady=(0, 8)
    )

    username_entry = ctk.CTkEntry(
        registration_card,
        width=330,
        height=46,
        placeholder_text="Enter your name",
        font=("Segoe UI", 14),
        fg_color=secondary_card,
        border_color=border_colour,
        border_width=1,
        corner_radius=10,
        text_color=text_primary,
        placeholder_text_color="#64748B"
    )
    username_entry.pack(
        padx=28,
        fill="x"
    )

    register_button = ctk.CTkButton(
        registration_card,
        text="Register Face",
        command=register_user,
        height=46,
        font=("Segoe UI", 14, "bold"),
        fg_color=primary,
        hover_color=primary_hover,
        corner_radius=10
    )
    register_button.pack(
        padx=28,
        pady=(24, 28),
        fill="x"
    )

    # Login card
    login_card = ctk.CTkFrame(
        content_frame,
        fg_color=card_colour,
        corner_radius=18,
        border_width=1,
        border_color=border_colour
    )
    login_card.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(12, 0),
        pady=5
    )

    login_badge = ctk.CTkLabel(
        login_card,
        text="  RETURNING USER  ",
        font=("Segoe UI", 11, "bold"),
        text_color="#BBF7D0",
        fg_color="#14532D",
        corner_radius=8
    )
    login_badge.pack(
        anchor="w",
        padx=28,
        pady=(26, 18)
    )

    login_title = ctk.CTkLabel(
        login_card,
        text="Authenticate Identity",
        font=("Segoe UI", 22, "bold"),
        text_color=text_primary
    )
    login_title.pack(
        anchor="w",
        padx=28
    )

    login_description = ctk.CTkLabel(
        login_card,
        text=(
            "Verify your identity using the trained\n"
            "biometric face recognition model."
        ),
        font=("Segoe UI", 13),
        text_color=text_secondary,
        justify="left"
    )
    login_description.pack(
        anchor="w",
        padx=28,
        pady=(8, 24)
    )

    security_box = ctk.CTkFrame(
        login_card,
        fg_color=secondary_card,
        corner_radius=12,
        border_width=1,
        border_color=border_colour
    )
    security_box.pack(
        padx=28,
        fill="x",
        pady=(8, 24)
    )

    security_icon = ctk.CTkLabel(
        security_box,
        text="✓",
        font=("Segoe UI", 22, "bold"),
        text_color=success_colour
    )
    security_icon.pack(
        side="left",
        padx=(16, 10),
        pady=18
    )

    security_text = ctk.CTkLabel(
        security_box,
        text=(
            "Local biometric verification\n"
            "No cloud upload required"
        ),
        font=("Segoe UI", 13),
        text_color=text_primary,
        justify="left"
    )
    security_text.pack(
        side="left",
        pady=15
    )

    login_button = ctk.CTkButton(
        login_card,
        text="Authenticate Face",
        command=login_user,
        height=46,
        font=("Segoe UI", 14, "bold"),
        fg_color=success_colour,
        hover_color=success_hover,
        corner_radius=10
    )
    login_button.pack(
        padx=28,
        pady=(0, 28),
        fill="x"
    )

    # Status area
    status_frame = ctk.CTkFrame(
        main_frame,
        fg_color=card_colour,
        corner_radius=14,
        border_width=1,
        border_color=border_colour
    )
    status_frame.pack(
        fill="x",
        pady=(22, 12)
    )

    status_dot = ctk.CTkLabel(
        status_frame,
        text="●",
        font=("Segoe UI", 15),
        text_color=success_colour
    )
    status_dot.pack(
        side="left",
        padx=(18, 10),
        pady=15
    )

    status_label = ctk.CTkLabel(
        status_frame,
        text="System ready",
        font=("Segoe UI", 13),
        text_color=text_secondary
    )
    status_label.pack(
        side="left",
        pady=15
    )

    # Privacy notice
    privacy_label = ctk.CTkLabel(
        main_frame,
        text=(
            "Privacy notice: Face images and biometric models are stored "
            "locally on this device."
        ),
        font=("Segoe UI", 12),
        text_color="#64748B"
    )
    privacy_label.pack(
        pady=(4, 0)
    )

    username_entry.focus()

    app.mainloop()