# Task 1 – N-Queens: Propositional Logic & Local Search

## 1. Yêu cầu hệ thống (Prerequisites)
- Python >= 3.9 (Khuyến nghị dùng **Python 3.11** để đảm bảo thư viện PySAT có sẵn bản cài đặt (wheel) ổn định trên Windows)

## 2. Cài đặt (Installation)

### Dành cho macOS / Linux (Môi trường chấm điểm)
```bash
# Tạo và chạy hoạt môi trường ảo
## Mac
python3 -m venv venv
source venv/bin/activate

## Window
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

# Cài đặt thư viện
pip install -r requirements.txt
```

## 3. Run (Usage)

```bash
python main.py gui
python main.py bench-sat
python main.py bench-sat --sizes 4 8 12 16 20 24 32
python main.py bench-mc --runs 20

## Cấu trúc
| File | Vai trò |
|---|---|
| `nqueens/models.py` | `Board`, `SolveResult`, lớp cơ sở `QueensSolver` |
| `nqueens/constraints.py` | `ConstraintDiscoverer` (tìm ràng buộc), `CNFConverter` (→ CNF) |
| `nqueens/sat_solver.py` | `SATQueensSolver` dùng `Glucose3` |
| `nqueens/min_conflicts.py` | `MinConflictsSolver`, `MaxConflictMinConflictsSolver` (heuristic) |
| `nqueens/benchmark.py` | Thực nghiệm |
| `nqueens/gui.py` | Giao diện Tkinter |

## Mô hình hóa mệnh đề (Req 1)
- Biến `X(r,c)` = True nếu ô (r,c) có hậu; mã hóa `r*N + c + 1`.
- Ràng buộc:
  - **ALO** mỗi hàng, mỗi cột: `(X(r,0) ∨ ... ∨ X(r,N-1))` → N hậu.
  - **AMO** mỗi hàng, cột, đường chéo chính (r−c), chéo phụ (r+c): `⋀ (¬a ∨ ¬b)` với mọi cặp ô trong cùng đường.
- Thuật toán khám phá: gom ô theo khóa `r`, `c`, `r−c`, `r+c` (O(N²)); mỗi nhóm sinh ràng buộc.
- Chuyển CNF: ALO → 1 mệnh đề dạng OR; AMO → C(k,2) mệnh đề 2-literal. Tất cả đã ở dạng CNF, không cần biến phụ.
- Số mệnh đề xấp xỉ O(N³).

## Min-Conflicts (Req 3)
- Trạng thái: mỗi cột 1 hậu (loại sẵn xung đột cột); biến = cột, giá trị = hàng.
- Chuẩn: chọn ngẫu nhiên cột đang xung đột, đặt vào hàng ít xung đột nhất.
- Heuristic đề xuất (**MaxConflict + noise**): chọn cột có nhiều xung đột nhất (hòa → ngẫu nhiên), với xác suất 10% chọn ngẫu nhiên để tránh kẹt.
- Đếm xung đột O(1) bằng mảng đếm hàng/đường chéo.
- Dùng `bench-mc` để so sánh tỉ lệ thành công, số bước, thời gian trung bình.