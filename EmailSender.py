import tkinter as tk
from tkinter import filedialog, messagebox
import smtplib
from email.message import EmailMessage
import os
import re

def email_function(subject, body, to, user, password, attachment=None):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject.replace('\n', '').replace('\r', '')
    msg['to'] = ", ".join(to).replace('\n', '').replace('\r', '')
    msg['From'] = user
    if attachment:
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def send_email():
    subject = subject_entry.get().replace('\n', '').replace('\r', '')
    body = body_text.get("1.0", tk.END)
    to = [entry.get().replace('\n', '').replace('\r', '') for entry in email_entries if entry.get()]
    user = email_entry.get().replace('\n', '').replace('\r', '')
    password = password_entry.get().replace('\n', '').replace('\r', '')
    if not subject or not body or not to or not user or not password:
        messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
        return
    try:
        email_function(subject, body, to, user, password, attachment_path.get())
        messagebox.showinfo("نجاح", "تم إرسال البريد الإلكتروني بنجاح")
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل في إرسال البريد الإلكتروني. خطأ: {str(e)}")

def add_email_entry(email=""):
    email_entry = tk.Entry(scrollable_frame, width=40)
    email_entry.pack(pady=5, padx=10)
    email_entry.insert(0, email)
    email_entries.append(email_entry)
    email_canvas.update_idletasks()
    email_canvas.config(scrollregion=email_canvas.bbox("all"))

def attach_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        attachment_path.set(file_path)
        attachment_label.config(text=os.path.basename(file_path))

def import_emails():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', content)
        for email in emails:
            add_email_entry(email)

def clear_emails():
    for email_entry in email_entries:
        email_entry.destroy()
    email_entries.clear()
    email_canvas.update_idletasks()
    email_canvas.config(scrollregion=email_canvas.bbox("all"))

root = tk.Tk()
root.title("Email Sender")
root.geometry("400x700")

tk.Label(root, text="البريد الإلكتروني:").pack(pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

tk.Label(root, text="كلمة المرور:").pack(pady=5)
password_entry = tk.Entry(root, show='*', width=40)
password_entry.pack(pady=5)

tk.Label(root, text="العنوان:").pack(pady=5)
subject_entry = tk.Entry(root, width=40)
subject_entry.pack(pady=5)

tk.Label(root, text="البريد الإلكتروني للمستلمين:").pack(pady=5)

email_frame = tk.Frame(root)
email_canvas = tk.Canvas(email_frame, width=300, height=150)
scrollbar = tk.Scrollbar(email_frame, orient="vertical", command=email_canvas.yview)
scrollable_frame = tk.Frame(email_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: email_canvas.configure(
        scrollregion=email_canvas.bbox("all")
    )
)

email_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
email_canvas.configure(yscrollcommand=scrollbar.set)

email_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
email_frame.pack(pady=5, fill="both", expand=True)

email_entries = []
add_email_entry()

add_email_button = tk.Button(root, text="إضافة بريد إلكتروني آخر", command=add_email_entry)
add_email_button.pack(pady=5)

import_email_button = tk.Button(root, text="استيراد عناوين البريد الإلكتروني من ملف", command=import_emails)
import_email_button.pack(pady=5)

clear_email_button = tk.Button(root, text="مسح جميع عناوين البريد الإلكتروني", command=clear_emails)
clear_email_button.pack(pady=5)

tk.Label(root, text="الرسالة:").pack(pady=5)
body_text = tk.Text(root, height=10, width=40)
body_text.pack(pady=5)

attachment_path = tk.StringVar()
attachment_label = tk.Label(root, text="")
attachment_label.pack(pady=5)
attach_button = tk.Button(root, text="إضافة ملف", command=attach_file)
attach_button.pack(pady=5)

send_button = tk.Button(root, text="ارسال", command=send_email)
send_button.pack(pady=20)

root.mainloop()
