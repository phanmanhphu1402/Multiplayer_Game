

**Hướng dẫn cài đặt game High and Low**

## Cách 1: Tải từ GitHub

Bước 1:
Truy cập đường dẫn sau để đến file trên GitHub: https://github.com/phanmanhphu1402/Multiplayer_Game

Bước 2:
Copy đường dẫn trên hoặc tham khảo hình dưới.

![image](https://github.com/phanmanhphu1402/Multiplayer_Game/blob/main/image/Picture1.png)

Bước 3:
Chọn thư mục mà bạn muốn đặt game vào.

Bước 4: Trong thư mục đó bấm chuột phải, chọn open in Terminal.

Bước 5: Trong Terminal nhập lệnh sau git init

Bước 6: Tiếp theo nhập lệnh git clone và thêm đường dẫn

![image](https://github.com/phanmanhphu1402/Multiplayer_Game/blob/main/image/Picture2.png)


## Cách 2: Tải file .zip

Bước 1: Tương tự như trên

Bước 2: Chọn download file .zip

Bước 3: Tải hoàn thành, giải nén.

**Chỉnh để chơi game:**

Do game có cơ chế chơi online nên chúng ta cần thay đổi một bài thông số trong
game để có thể sử dụng hết tính năng của game.

(Kết nối mạng LAN và client phải truy cập đến địa chỉ của server trong mạng LAN)

- Vào Python và mở thư mục chứa game
  
- Mở Terminal nhấn ipconfig

- Copy địa chỉ IPv4 và thay đổi vào biến server ở file server.py và network.py
  
- Chạy file server.py để khởi động server

- Chạy file client.py để chơi game

## Python 3.12 | General Public License
