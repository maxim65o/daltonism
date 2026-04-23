import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class VisionTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Тест на Дальтонизм (6 Изображений)")
        self.geometry("700x950")
        self.resizable(True, True)

        # --- 6 ВОПРОСОВ ---
        self.questions = [
            {
                "id": 1,
                "image": "img1.png",
                "text": "Какую цифру вы видите?",
                "options": ["12", "21", "Ничего не вижу"],
                "normal": "12",
                "achromat": "Ничего не вижу"
            },
            {
                "id": 2,
                "image": "img2.png",
                "text": "Какую цифру вы видите?",
                "options": ["13", "31", "Ничего не вижу"],
                "normal": "13",
                "achromat": "Ничего не вижу"
            },
            {
                "id": 3,
                "image": "img3.png",
                "text": "Какую цифру вы видите?",
                "options": ["16", "61", "Ничего не вижу"],
                "normal": "16",
                "achromat": "Ничего не вижу"
            },
            {
                "id": 4,
                "image": "img4.png",
                "text": "Какую цифру вы видите?",
                "options": ["8", "3", "Ничего не вижу"],
                "normal": "8",
                "achromat": "Ничего не вижу"
            },
            {
                "id": 5,
                "image": "img5.png",
                "text": "Какую цифру вы видите?",
                "options": ["9", "92", "Ничего не вижу"],
                "normal": "9",
                "achromat": "Ничего не вижу"
            },
            {
                "id": 6,
                "image": "img6.png",
                "text": "Какую фигуру вы видите?",
                "options": ["7", "4", "Ничего не вижу"],
                "normal": "7",
                "achromat": "Ничего не вижу"
            }
        ]

        self._create_placeholders()

        self.current_q_index = 0
        self.user_results = []  # Будет хранить 'Normal', 'Achromatopsia', или 'Error'
        self.selected_answer = ctk.StringVar(value=None)

        # Прокручиваемый фрейм
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=680)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.header = ctk.CTkLabel(self.scrollable_frame, text="Проверка цветовосприятия", font=("Roboto", 24, "bold"))
        self.header.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self.scrollable_frame, width=600)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.img_container = ctk.CTkFrame(self.scrollable_frame, width=500, height=500, fg_color="#1f1f1f")
        self.img_container.pack(pady=10)
        self.img_label = ctk.CTkLabel(self.img_container, text="")
        self.img_label.pack(expand=True)

        self.q_label = ctk.CTkLabel(self.scrollable_frame, text="", font=("Roboto", 18))
        self.q_label.pack(pady=15)

        self.btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=50)

        self.submit_btn = ctk.CTkButton(
            self.scrollable_frame,
            text="Подтвердить ответ",
            command=self.submit_answer,
            height=50,
            font=("Roboto", 18, "bold"),
            fg_color="#2b2b2b",
            hover_color="#3a3a3a"
        )
        self.submit_btn.pack(pady=25)

        self.load_question()

    def _create_placeholders(self):
        for q in self.questions:
            if not os.path.exists(q['image']):
                img = Image.new('RGB', (500, 500), color=(100, 100, 100))
                img.save(q['image'])

    def load_image(self, path):
        try:
            pil_img = Image.open(path)
            pil_img.thumbnail((480, 480), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)

            self.img_label.configure(image=ctk_img, text="")
            self.img_label.image = ctk_img
        except Exception as e:
            self.img_label.configure(text=f"Ошибка: {path}")

    def load_question(self):
        if self.current_q_index >= len(self.questions):
            self.show_final_screen()
            return

        q_data = self.questions[self.current_q_index]

        self.selected_answer.set(None)

        self.submit_btn.configure(
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            text="Подтвердить ответ"
        )

        progress_val = (self.current_q_index) / len(self.questions)
        self.progress.set(progress_val)

        self.q_label.configure(text=f"Вопрос {self.current_q_index + 1} из 6: {q_data['text']}")
        self.load_image(q_data['image'])

        for widget in self.btn_frame.winfo_children():
            widget.destroy()

        for option_text in q_data['options']:
            radio = ctk.CTkRadioButton(
                self.btn_frame,
                text=option_text,
                variable=self.selected_answer,
                value=option_text,
                font=("Roboto", 16),
                command=self.on_option_select,
                height=40
            )
            radio.pack(fill="x", pady=8, padx=20)

    def on_option_select(self):
        self.submit_btn.configure(
            fg_color="#2ea043",
            hover_color="#2c974b",
            text="ПОДТВЕРДИТЬ ОТВЕТ"
        )

    def submit_answer(self):
        choice = self.selected_answer.get()
        if not choice:
            return

        current_q = self.questions[self.current_q_index]

        # ЛОГИКА ДИАГНОСТИКИ
        if choice == current_q['normal']:
            diagnosis = "Normal"
        elif choice == current_q['achromat']:
            diagnosis = "Achromatopsia"
        else:
            diagnosis = "Error"  # Неправильный ответ — возможно, дальтонизм или ошибка

        self.user_results.append(diagnosis)

        self.current_q_index += 1
        self.load_question()

    def show_final_screen(self):
        self.scrollable_frame.destroy()

        self.result_frame = ctk.CTkScrollableFrame(self, width=680)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        total = len(self.user_results)
        normal_count = self.user_results.count("Normal")
        achromat_count = self.user_results.count("Achromatopsia")
        error_count = self.user_results.count("Error")

        # Вердикт
        if achromat_count >= 4 or (achromat_count + error_count) >= 5:
            title = "Вероятна АХРОМАТОПСИЯ"
            color = "#ff3333"
            desc = f"Вы дали {achromat_count} ответов как при ахроматопсии и {error_count} ошибок.\nРекомендуется консультация офтальмолога."
        elif error_count > 2:
            title = "Есть отклонения"
            color = "#ffaa00"
            desc = f"Вы допустили {error_count} ошибок. Возможно, у вас есть легкий дальтонизм или вы были невнимательны."
        elif normal_count == total:
            title = "Цветовосприятие в НОРМЕ"
            color = "#33cc33"
            desc = "Вы правильно определили все изображения!"
        else:
            title = "Смешанный результат"
            color = "#ffaa00"
            desc = f"Норма: {normal_count}, Ахроматопсия: {achromat_count}, Ошибки: {error_count}"

        ctk.CTkLabel(self.result_frame, text=title, font=("Roboto", 30, "bold"), text_color=color).pack(pady=40)
        ctk.CTkLabel(self.result_frame, text=desc, wraplength=600, font=("Roboto", 16)).pack(pady=10)

        res_frame = ctk.CTkFrame(self.result_frame)
        res_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, res in enumerate(self.user_results):
            if res == "Normal":
                status = "Норма"
                col = "#33cc33"
            elif res == "Achromatopsia":
                status = "Ахроматопсия"
                col = "#ff3333"
            else:
                status = "Ошибка"
                col = "#ffaa00"

            row = ctk.CTkFrame(res_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(row, text=f"Вопрос {i + 1}", anchor="w", width=100).pack(side="left")
            ctk.CTkLabel(row, text=status, text_color=col, anchor="e").pack(side="right", fill="x", expand=True)

        ctk.CTkButton(self.result_frame, text="Закрыть", command=self.quit, width=200, height=40).pack(pady=30)


if __name__ == "__main__":
    app = VisionTestApp()
    app.mainloop()
