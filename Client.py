import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = socket.gethostbyname(socket.gethostname())   #ipconfig
PORT = 9060

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.name = simpledialog.askstring('Nickname', 'Give your nickname', parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        rcv_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        rcv_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg='lightgray')

        self.chat_label = tkinter.Label(self.win, text='Chat: ', bg='lightgray')
        self.chat_label.config(font=('Book Antiqua', 12))
        self.chat_label.pack(padx=20, pady=5)

        self.txt_box = tkinter.scrolledtext.ScrolledText(self.win)
        self.txt_box.pack(padx=20, pady=5)
        self.txt_box.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text='Message: ', bg='lightgray')
        self.msg_label.config(font=('Book Antiqua', 12))
        self.msg_label.pack(padx=20, pady=5)

        self.inp_area = tkinter.Text(self.win, height=3)
        self.inp_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text='send', command=self.write)
        self.send_button.config(font=('Book Antiqua', 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol('WM_DELETE_WINDOW', self.stop)
        self.win.mainloop()

    def write(self):
        msg = f'{self.name}: {self.inp_area.get("1.0", "end")}'
        self.sock.send(msg.encode('utf-8'))
        self.inp_area.delete("1.0", "end")

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if msg == 'NAME: ':
                    self.sock.send(self.name.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.txt_box.config(state='normal')
                        self.txt_box.insert('end', msg)
                        self.txt_box.yview('end')
                        self.txt_box.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print('404 Error!')
                self.sock.close()
                break

client = Client(HOST, PORT)