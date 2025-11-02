import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.wm_iconbitmap('your_icon.ico')  # Set icon early
# ... your GUI setup ...
root.mainloop()  # Starts the event loop

# ---------- AI parseur simple ----------


def ai_calc(text: str):
    try:
        text = text.lower().strip()
        for phrase in ["calcule", "combien fait", "fais moi", "calculer", "please"]:
            text = text.replace(phrase, "")
        text = text.strip()
        if not text:
            return None
        for op in ["+", "-", "*", "/"]:
            if op in text:
                left, right = text.split(op, 1)
                left = left.replace(",", ".").strip()
                right = right.replace(",", ".").strip()
                a = float(left)
                b = float(right)
                if op == "+":
                    return a + b
                if op == "-":
                    return a - b
                if op == "*":
                    return a * b
                if op == "/":
                    return a / b
        return None
    except Exception:
        return None

# ---------- Calculator logic ----------


class Calculator:
    def __init__(self):
        self.expr = ""

    def press(self, char):
        self.expr += str(char)
        return self.expr

    def clear(self):
        self.expr = ""
        return self.expr

    def backspace(self):
        self.expr = self.expr[:-1]
        return self.expr

    def evaluate(self):
        try:
            safe_expr = self.expr.replace(",", ".")
            allowed = "0123456789+-*/.() "
            if all(c in allowed for c in safe_expr):
                result = eval(safe_expr)
                self.expr = str(result)
                return self.expr
            else:
                return "ERR"
        except Exception:
            return "ERR"

# ---------- UI ----------


class AICalcApp:
    def __init__(self, root):
        self.root = root
        root.title("AI Hybrid Calculator")
        root.geometry("360x520")
        root.resizable(False, False)
        self.bg = "#0f1724"
        self.fg = "#e6eef6"
        self.accent = "#1f6feb"
        root.configure(bg=self.bg)
        self.calc = Calculator()

        # Top: AI input
        top = tk.Frame(root, bg=self.bg)
        top.pack(padx=12, pady=(12, 6), fill="x")
        self.ai_entry = tk.Entry(top, font=("Segoe UI", 14), bd=0, relief="flat")
        self.ai_entry.pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 8))
        ai_btn = tk.Button(top, text="AI →", command=self.on_ai, bd=0,
                           font=("Segoe UI", 12), bg=self.accent, fg="white")
        ai_btn.pack(side="right", ipadx=8, ipady=6)

        help_label = tk.Label(root, text="Ex: calcule 12 + 7 ou utilisez les boutons",
                              bg=self.bg, fg="#9fb0d6", font=("Segoe UI", 9))
        help_label.pack(padx=12, anchor="w")

        # Middle: display
        disp_frame = tk.Frame(root, bg=self.bg)
        disp_frame.pack(padx=12, pady=12, fill="x")
        self.display = tk.Entry(disp_frame, font=("Segoe UI", 28), bd=0, relief="flat", justify="right")
        self.display.pack(fill="x", ipady=10)

        # Bottom: keypad
        keypad = tk.Frame(root, bg=self.bg)
        keypad.pack(padx=12, pady=(4, 12))
        buttons = [
            ("C", "C"), ("⌫", "BS"), ("%", "%"), ("/", "/"),
            ("7", "7"), ("8", "8"), ("9", "9"), ("*", "*"),
            ("4", "4"), ("5", "5"), ("6", "6"), ("-", "-"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("+", "+"),
            ("+/-", "NEG"), ("0", "0"), (".", "."), ("=", "="),
        ]
        r = 0
        c = 0
        for (text, val) in buttons:
            def action(v=val): return self.on_button(v)
            b = tk.Button(keypad, text=text, width=6, height=2, bd=0, font=("Segoe UI", 14), command=action)
            b.grid(row=r, column=c, padx=6, pady=6)
            c += 1
            if c == 4:
                c = 0
                r += 1

        footer = tk.Label(root, text="Hybrid AI Calculator — project", bg=self.bg, fg="#9fb0d6", font=("Segoe UI", 8))
        footer.pack(side="bottom", pady=6)

    def on_ai(self):
        txt = self.ai_entry.get()
        if not txt.strip():
            messagebox.showinfo("AI", "Écris un calcul, ex : calcule 10 + 5")
            return
        res = ai_calc(txt)
        if res is None:
            messagebox.showwarning("AI", "Impossible de parser l'entrée.")
        else:
            self.display.delete(0, tk.END)
            self.display.insert(0, str(res))
            self.calc.expr = str(res)

    def on_button(self, val):
        if val == "C":
            self.calc.clear()
            self.display.delete(0, tk.END)
        elif val == "BS":
            self.calc.backspace()
            self.display.delete(0, tk.END)
            self.display.insert(0, self.calc.expr)
        elif val == "=":
            out = self.calc.evaluate()
            self.display.delete(0, tk.END)
            self.display.insert(0, out)
        elif val == "NEG":
            cur = self.display.get()
            if cur.startswith("-"):
                cur = cur[1:]
            else:
                cur = "-" + cur if cur else cur
            self.calc.expr = cur
            self.display.delete(0, tk.END)
            self.display.insert(0, cur)
        else:
            self.calc.press(val)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.calc.expr)


if __name__ == "__main__":
    root = tk.Tk()
    app = AICalcApp(root)
    root.mainloop()
root.iconbitmap("assets/icon.ico")
