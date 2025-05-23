import tkinter as tk
from tkinter import messagebox, font
from predict import AirAlertDurationPredictor
import math

class AirAlertDurationApp:
    def __init__(self, master):
        self.master = master
        master.title("Air Alert Duration Predictor")
        master.geometry("440x340")
        master.configure(bg="#232946")

        self.predictor = AirAlertDurationPredictor()
        mse = self.predictor.last_mse if hasattr(self.predictor, "last_mse") else None
        self.mse = mse
        self.std_minutes = int(round(math.sqrt(mse))) if mse is not None else None

        # Fonts
        self.title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.result_font = font.Font(family="Segoe UI", size=14)
        self.button_font = font.Font(family="Segoe UI", size=12, weight="bold")
        self.info_font = font.Font(family="Segoe UI", size=10)

        # Title label
        self.title_label = tk.Label(
            master,
            text="Air Alert Duration Predictor",
            font=self.title_font,
            fg="#eebbc3",
            bg="#232946",
            pady=10
        )
        self.title_label.pack()

        # Info label for MSE and bias
        if self.mse is not None and self.std_minutes is not None:
            mse_text = (
                f"Model MSE: {self.mse:.2f}\n"
                f"Typical prediction error: ±{self.std_minutes} minutes\n"
                "Predictions are most accurate near the average duration."
            )
        else:
            mse_text = "Model error info unavailable."
        self.info_label = tk.Label(
            master,
            text=mse_text,
            font=self.info_font,
            fg="#b8c1ec",
            bg="#232946",
            pady=5
        )
        self.info_label.pack()

        # Result label
        self.result_var = tk.StringVar()
        self.result_label = tk.Label(
            master,
            textvariable=self.result_var,
            font=self.result_font,
            fg="#b8c1ec",
            bg="#232946",
            pady=20
        )
        self.result_label.pack()

        # Predict button
        self.predict_button = tk.Button(
            master,
            text="Predict",
            command=self.predict_duration_ui,
            font=self.button_font,
            bg="#eebbc3",
            fg="#232946",
            activebackground="#b8c1ec",
            activeforeground="#232946",
            relief="raised",
            bd=3,
            padx=20,
            pady=10
        )
        self.predict_button.pack(pady=20)

    def predict_duration_ui(self):
        try:
            self.result_var.set("")  # Clear previous result
            self.result_label.update_idletasks()  # Force UI update
            predicted_duration = self.predictor.predict()
            self.result_var.set(f"Predicted air alert duration:\n{predicted_duration:.1f} minutes")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AirAlertDurationApp(root)
    root.mainloop()
