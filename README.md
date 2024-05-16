
CookCook Game




## Giới thiệu 
Đây là tựa game 2D với lối chơi đơn giản cổ điển được 1 nhóm sinh viên thử sức lập trình .

 " Bạn sẽ tham gia vào thế giới 2D với bản thân bạn chính là 1 khối slime , bạn chỉ có thể di chuyển và nhảy để tránh khỏi sự tấn công của chú Voi khổng lồ với các công nghệ tối tân mà nó được trang bị . Nếu bạn nghĩ bạn có thể thoát khỏi được " mưa đá " và tia laser và hàng chục các lưỡi cưa đang măm me giúp bạn restart game sớm nhất có thể thì bạn hãy thử , để biết bạn đi được bao xa ! "
## Cài đặt
Trước hết ta cần cài đặt Python

Trước tiên, hãy chắc chắn rằng bạn đã cài đặt Python trên máy tính của mình bằng cách mở mở cửa sổ Command Prompt (hoặc PowerShell) sau đó nhập dòng lệnh :
```bash
 python --version
```

Nếu chưa cài đặt , bạn có thể tải xuống phiên bản Python phù hợp với hệ điều hành của bạn từ trang web Python.org. (http://www.python.org/downloads/)

Sau khi tải xuống, nhấp đúp chuột vào tệp cài đặt và làm theo hướng dẫn để cài đặt Python. Đảm bảo bạn chọn tùy chọn “Add Python to PATH” để thêm Python vào biến môi trường PATH của bạn

Hướng dẫn cài đặt chi tiết : ( https://realpython.com/installing-python/ )





Để có thể khởi tạo trò chơi ta cần phải cài đặt thư viện Pygame :
Với Windows , mở cửa sổ Command Prompt (hoặc PowerShell) sau đó nhập dòng lệnh :

```bash
  pip install pygame
```



## Cách chạy

Để chạy game với giao diện hoàn thiện  :

```bash
  python playGui.py
```

Để chạy game với chỉ với màn hình game singleplayer  :

```bash
  python main.py
```

Để chạy game với chỉ với màn hình game multiplayer  :

- Khởi tạo server 
```bash 
  python server.py
```
- Khởi tạo client 
```bash 
  python client.py
```
## Tech Stack

**Client:** pygame , Tiled , pytmx

**Server:** socket , pickle , thread


## License

[MIT](https://choosealicense.com/licenses/mit/)

