# GUI & Email Library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import smtplib
import imaplib
import email

def send_email():
    # Mengambil Informasi dari Input Pengguna
    sender_email = sender_email_entry.get()
    sender_password = sender_password_entry.get()
    recipient_email = recipient_email_entry.get()
    subject = subject_entry.get()
    message = message_text.get("1.0", END)

    try:
        # Mengatur Koneksi ke Server SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            # Login ke Akun Pengirim
            smtp.login(sender_email, sender_password)

            # Membuat Email
            email_body = f'Subject: {subject}\n\n{message}'
            # Mengirim Email
            smtp.sendmail(sender_email, recipient_email, email_body)

        # Memverifikasi Email Berhasil di Kirim atau Tidak
        messagebox.showinfo("Success", "Email Has Been Sent Successfully!")
    except smtplib.SMTPException as e:
        error_message = str(e)
        messagebox.showerror("Error", f"Failed to send email:\n\n{error_message}")

def receive_email():
    # Mengambil Informasi dari Input Pengguna
    recipient_email = recipient_email_entry.get()
    recipient_password = recipient_password_entry.get()

    # Mengatur Koneksi ke Server IMAP
    with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
        # Login ke Akun Penerima
        imap.login(recipient_email, recipient_password)
        imap.select('INBOX')

        # Mencari Email yang Belum Dibaca
        _, message_numbers = imap.search(None, 'ALL')
        message_numbers = message_numbers[0].split()

        latest_number = message_numbers[-1]  # Ambil nomor email terbaru
        _, message_data = imap.fetch(latest_number, '(RFC822)')
        raw_email = message_data[0][1]

        email_message = email.message_from_bytes(raw_email)
        subject = email_message['Subject']
        sender = email_message['From']
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')

    # Menampilkan Detail Email
    messagebox.showinfo("Success", f"New Email Received!\n\nSender : {sender}\nSubject : {subject}\n\nMessage :\n{body}")

# Membuat GUI
window = Tk()
window.title("Send and Receive Email")

# Frame Utama Untuk Label & Entry
window.geometry("430x420")
window.resizable(False, False)

# Membuat style untuk entry dengan radius
style = ttk.Style()
style.configure("RoundedEntry.TEntry", borderwidth=0, relief="solid", 
                padding=5, bordercolor="#bfbfbf", 
                background="#ffffff", foreground="#000000", 
                focuscolor="#80bdff", fieldbackground="#ffffff")

# Jenis Font
font_style = ("Arial", 9)

# Label & Entry Untuk Sender Email
sender_email_label = Label(window, text = "Sender Email : ", anchor = "e")
sender_email_label.grid(row = 0, column = 0, sticky = "E")
sender_email_entry = ttk.Entry(window, width = 30, justify = CENTER, style="RoundedEntry.TEntry", font = font_style)
sender_email_entry.grid(row = 0, column = 1, pady = 10)

# Label & Entry Untuk Password
sender_password_label = Label(window, text = "Sender Password : ", anchor = "e")
sender_password_label.grid(row = 1, column = 0, sticky = "E")
sender_password_entry = ttk.Entry(window, width = 30, justify = CENTER, show = "*", style="RoundedEntry.TEntry", font = font_style)
sender_password_entry.grid(row = 1, column = 1, pady = 5)

# Label & Entry Untuk Recipient Email
recipient_email_label = Label(window, text = "Recipient Email : ")
recipient_email_label.grid(row = 2, column = 0, sticky = "E")
recipient_email_entry = ttk.Entry(window, width = 30, justify = CENTER, style="RoundedEntry.TEntry", font = font_style)
recipient_email_entry.grid(row = 2, column = 1, pady = 5)

# Label & Entry Untuk Recipient Password
recipient_password_label = Label(window, text = "Recipient Password : ", anchor = "e")
recipient_password_label.grid(row = 3, column = 0, sticky = "E")
recipient_password_entry = ttk.Entry(window, width = 30, justify = CENTER, show = "*", style="RoundedEntry.TEntry", font = font_style)
recipient_password_entry.grid(row = 3, column = 1, pady = 5)

# Label & Entry Untuk Subject
subject_label = Label(window, text = "Subject : ")
subject_label.grid(row = 4, column = 0, sticky = "E")
subject_entry = ttk.Entry(window, width = 30, justify = CENTER, style="RoundedEntry.TEntry", font = font_style)
subject_entry.grid(row = 4, column = 1, pady = 5)

# # Label & Text Untuk Message
message_label = Label(window, text = "Message : ")
message_label.grid(row = 5, column = 0, sticky = "NE")
message_text = Text(window, height = 10, width = 40, font = font_style)
message_text.grid(row = 5, column = 1, padx = 10, pady = 10)

# Tombol Kirim Email
send_button = ttk.Button(window, text = "Send Email", command = send_email)
send_button.place(x = 165, y = 380, width = 100, height = 30)

# Tombel Menerima Email
receive_button = ttk.Button(window, text = "Email Received", command = receive_email)
receive_button.place(x = 275, y = 380, width = 100, height = 30)

window.mainloop()