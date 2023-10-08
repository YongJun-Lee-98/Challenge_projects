import ftplib
import os
import shutil
import json
from multiprocessing import Process
from tkinter import Tk, Checkbutton, Button, BooleanVar, messagebox
from ftplib import FTP

def read_config():
    # JSON 파일을 읽습니다.
    with open('ftp_config.json', 'r') as f:
        return json.load(f)

def define_path():
    # 바탕화면의 PDF 폴더와 hwp 폴더, excel 폴더의 경로를 정의합니다.
    return [os.path.join(os.path.expanduser("~/Desktop"), folder) for folder in ["PDF", "hwp", "excel"]]

# FTP 세션을 닫습니다.
def ftp_upload_task(ftp, filename, file_path):
    with open(file_path, 'rb') as file:
        try:
            ftp.storbinary('STOR ' + filename, file)
        except ftplib.error_perm as e:
            print(f'Error: {e}')

def upload_task(folder_path, ftp_path, config):
    # FTP 클라이언트 객체를 생성하고 서버에 연결합니다.
    ftp = FTP(config['ftp_server'])
    ftp.login(user=config['ftp_user'], passwd=config['ftp_password'])

    # FTP 서버의 업로드 디렉토리로 이동합니다.
    ftp.cwd(ftp_path)

    # 디렉토리에 있는 모든 파일을 FTP 서버에 업로드합니다.
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ftp_upload_task(ftp, filename, file_path)
    ftp.quit()

def copy_files_with_extension(src_dir, dst_dir, extension):
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith(extension):
                src_file_path = os.path.join(dirpath, filename)
                dst_file_path = os.path.join(dst_dir, filename)

                # 대상 경로에 이미 같은 이름의 파일이 있다면, 메타데이터를 비교합니다.
                if os.path.exists(dst_file_path):
                    # 소스 파일과 대상 파일의 마지막 수정 시간을 비교합니다.
                    if os.path.getmtime(src_file_path) > os.path.getmtime(dst_file_path):
                        # 소스 파일이 더 최신이라면, 대상 파일을 덮어씁니다.
                        shutil.copy2(src_file_path, dst_file_path)
                else:
                    shutil.copy2(src_file_path, dst_file_path)

def ensure_directory_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def copy_task(src_dir, dst_dir, extension):
    ensure_directory_exists(dst_dir)
    copy_files_with_extension(src_dir, dst_dir, extension)

def run_process(target_func, args):
    process = Process(target=target_func, args=args)
    process.start()
    process.join()

def run_tasks(var_ssh, var_pdf, var_hwp, var_excel, folder_path, folder_path1, folder_path2, config):
    if var_pdf.get():
        run_process(copy_task, (os.path.expanduser("~/"), folder_path, ".pdf"))
        if var_ssh.get():
            run_process(upload_task, (folder_path, '/HDD1/Backup/pdf/', config))

    if var_hwp.get():
        run_process(copy_task, (os.path.expanduser("~/"), folder_path1, ".hwp"))
        run_process(copy_task, (os.path.expanduser("~/"), folder_path1, ".hwpx"))
        if var_ssh.get():
            run_process(upload_task, (folder_path1, '/HDD1/Backup/hwp/', config))

    if var_excel.get():
        excel_extensions = [".xlsx", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xls", ".xlml", ".xlam", ".xla", ".xlw", ".xlr", ".csv", ".dif", ".slk"]
        for extension in excel_extensions:
            run_process(copy_task, (os.path.expanduser("~/"), folder_path2, extension))
        if var_ssh.get():
            run_process(upload_task, (folder_path2, '/HDD1/Backup/excel/', config))
    messagebox.showinfo("작업 완료", "모든 작업이 완료되었습니다!")

if __name__ == "__main__":
    root = Tk()
    root.geometry("500x300")
    var_ssh = BooleanVar()
    var_pdf = BooleanVar()
    var_hwp = BooleanVar()
    var_excel = BooleanVar()

    Checkbutton(root, text='서버에 백업', variable=var_ssh).pack()
    Checkbutton(root, text='PDF 작업', variable=var_pdf).pack()
    Checkbutton(root, text='hwp 작업', variable=var_hwp).pack()
    Checkbutton(root, text='excel 작업', variable=var_excel).pack()

    config = read_config()
    folder_path, folder_path1, folder_path2 = define_path()

    Button(root, text='작업 시작', command=lambda: run_tasks(var_ssh, var_pdf, var_hwp, var_excel, folder_path, folder_path1, folder_path2, config)).pack()

    root.mainloop()
