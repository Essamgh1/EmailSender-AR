import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
    
        tk.Label(self.root, text="ادخل ايميلك:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
        self.email_user = tk.Entry(self.root, width=50)
        self.email_user.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        
        tk.Label(self.root, text="كلمة المرور:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10)
        self.email_password = tk.Entry(self.root, show="*", width=50)
        self.email_password.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        
        add_email_button = tk.Button(self.root, text="إضافة البريد الإلكتروني لمستلم اضافي", command=self.add_email_entry, bg="#4CAF50", fg="white", padx=20, pady=10)
        add_email_button.grid(row=5, column=0, columnspan=2, pady=10)

        
        tk.Label(self.root, text="البريد الإلكتروني للمستلمين:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10)
        self.email_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.email_frame.grid(row=3, column=1, columnspan=2, padx=9, pady=10, sticky="w" )
        self.email_entries = []
        self.add_email_entry()

        
        remove_email_button = tk.Button(self.root, text="إزالة البريد الإلكتروني الأخير", command=self.remove_email_entry, bg="#FF5733", fg="white", padx=20, pady=10)
        remove_email_button.grid(row=6, column=0, columnspan=2, pady=10)

       
        tk.Label(self.root, text="العنوان:", bg="#f0f0f0").grid(row=6, column=0, padx=10, pady=10)
        self.subject = tk.Entry(self.root, width=50)
        self.subject.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        
        tk.Label(self.root, text="الرسالة:", bg="#f0f0f0").grid(row=7, column=0, padx=10, pady=10)
        self.body = tk.Text(self.root, height=10, width=50)
        self.body.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        

        
        self.resume_file = tk.Label(self.root, text="", bg="#f0f0f0")
        self.resume_file.grid(row=10, column=1, padx=10, pady=10, sticky="w")

        
        attach_file_button = tk.Button(self.root, text="اضافة ملف", command=self.attach_file, bg="#4CAF50", fg="white", padx=20, pady=10)
        attach_file_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10,)

        
        tk.Button(self.root, text="ارسال الايميل", command=self.send_email, bg="#4CAF50", fg="white", padx=20, pady=10).grid(row=11, column=0, columnspan=2, pady=10)

        
        self.credits_label = tk.Label(self.root, text="by Essam Alghamdi", bg="#f0f0f0", fg="#777777")
        self.credits_label.grid(row=12, column=0, columnspan=2, pady=5)
        self.credits_label.bind("<Button-1>", lambda e: self.open_link("https://www.linkedin.com/in/essam-alghamdii/"))
        self.credits_label.config(cursor="hand2")

    def add_email_entry(self):
        email_entry = tk.Entry(self.email_frame, width=50)
        email_entry.pack(padx=10, pady=5)
        self.email_entries.append(email_entry)

    def remove_email_entry(self):
        if self.email_entries:
            entry = self.email_entries.pop()
            entry.destroy()

    def attach_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.resume_file.config(text=file_path)
            file_name = file_path.split("/")[-1]  
            messagebox.showinfo("تمت العملية", f"تم اختيار ملف: {file_name}")
        else:
            messagebox.showinfo("تنبيه", "لم يتم اختيار ملف.")
            

    def send_email(self):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        email_user = self.email_user.get()
        email_password = self.email_password.get()
        subject = self.subject.get()
        body = self.body.get("1.0", tk.END)
        resume_file = self.resume_file.cget("text")
        
        to_emails = [entry.get() for entry in self.email_entries if entry.get()]
        
        if not all([email_user, email_password, to_emails, subject, body, resume_file]):
            messagebox.showerror("خطا", "يجب ملء جميع الحقول ويجب توفير بريد إلكتروني واحد للمستلم على الأقل!")
            return
        
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with open(resume_file, 'rb') as file:
            part = MIMEApplication(file.read(), Name='resume.pdf')
            part['Content-Disposition'] = 'attachment; filename="resume.pdf"'
            msg.attach(part)
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_password)
            for to_email in to_emails:
                msg['To'] = to_email
                server.sendmail(email_user, to_email, msg.as_string())
            server.close()
            messagebox.showinfo("تم الارسال", "تم إرسال رسائل البريد الإلكتروني بنجاح!")
        except Exception as e:
            messagebox.showerror("خطا", f"فشل في إرسال البريد الإلكتروني. خطأ: {str(e)}")

    def open_link(self, link):
        import webbrowser
        webbrowser.open(link)


root = tk.Tk()
app = EmailApp(root)
root.mainloop()
