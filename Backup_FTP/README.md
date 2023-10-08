# Backup_FTP
Backup_FTP는 FTP 서버에 백업하는 프로그램으로 제작되었습니다.
ftplib, os, shutil, json, multiprocessing, tkinter를 사용하였으며
백업이 지원되는 항목은 

PDF 확장자
.pdf

한글 확장자
.hwp,.hwpx

엑셀 확장자
.xlsx", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xls", ".xlml", ".xlam", ".xla", ".xlw", ".xlr", ".csv", ".dif", ".slk"

의 파일들을 '바탕화면'에 우선 모두 복사해 둔 뒤
이 파일을 해당 서버의 폴더에 업로드 하는 방식으로 지정되어있습니다.

사용전 FTP 서버의 해당 위치에 폴더이름 pdf, hwp, excel이 각각 존재하는지 확인하시고
존재하지 않는다면 생성후 프로그램을 작동시켜주세요.
(폴더가 존재하지 않는다면 업로드가 제대로 동작하지 않습니다.)
