import tkinter as tk


class PeerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.frame_input = tk.Frame()
        self.entry_path = tk.Entry()
        self.output_text1 = tk.Text()
        self.output_text2 = tk.Text()
        self.output_text3 = None

    def set_application_title(self, text="Torrent Application"):
        self.root.title(text)

    def get_file_path(self):
        file_path = self.entry_path.get()
        self.entry_path.delete(0, tk.END)
        return file_path

    def print_textbox_downloader(self, text):
        self.output_text1.insert(tk.END, text + '\n')

    def print_textbox_uploader(self, text):
        self.output_text2.insert(tk.END, text + '\n')

    def print_textbox_torrent(self, text):
        self.output_text3.insert(tk.END, text + '\n')

    def setup_ui(self, download_exe=None, create_torrent_exe=None):
        # Title
        self.set_application_title()

        # Create a input frame
        self.frame_input = tk.Frame(self.root)
        self.frame_input.pack(pady=10)

        # Tạo label và entry cho đường dẫn file
        tk.Label(self.frame_input, text="File path:").grid(row=0, column=0)
        self.entry_path = tk.Entry(self.frame_input, width=50)
        self.entry_path.grid(row=0, column=1)

        # Tạo nút Download
        btn_download = tk.Button(self.frame_input, text="Download", command=download_exe)
        btn_download.grid(row=0, column=2, padx=10)

        # Tạo nút Create Torrent
        btn_create_torrent = tk.Button(self.frame_input, text="Create Torrent", command=create_torrent_exe)
        btn_create_torrent.grid(row=0, column=3)

        # Tạo Frame cho phần xuất thông tin
        frame_output = tk.Frame(self.root)
        frame_output.pack()

        # Tạo Frame cho Output Text 1
        frame_output_text1 = tk.Frame(frame_output)
        frame_output_text1.pack(side=tk.LEFT, padx=10)

        label_output1 = tk.Label(frame_output_text1, text="Downloading information")
        label_output1.pack()
        self.output_text1 = tk.Text(frame_output_text1, height=10, width=50)
        self.output_text1.pack()

        # Tạo Frame cho Output Text 2
        frame_output_text2 = tk.Frame(frame_output)
        frame_output_text2.pack(side=tk.RIGHT, padx=10)

        label_output2 = tk.Label(frame_output_text2, text="Uploading information:")
        label_output2.pack()
        self.output_text2 = tk.Text(frame_output_text2, height=10, width=50)
        self.output_text2.pack()

        # Tạo nhãn và cửa sổ hiển thị thông tin output_text
        label_output = tk.Label(self.root, text="Torrent list")
        label_output.pack()
        self.output_text3 = tk.Text(self.root, height=10, width=100)
        self.output_text3.pack()

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = PeerUI()


    def download_button_proc():
        global window
        print(f'fPressed Download button: {window.get_file_path()}')

    def upload_button_proc():
        global window
        print(f'Pressed Upload button: {window.get_file_path()}')

    window.setup_ui(download_exe=download_button_proc, create_torrent_exe=upload_button_proc)
    window.print_textbox_3(f'Line {1+0}')
    window.print_textbox_3(f'Line {1+1}')
    window.start()