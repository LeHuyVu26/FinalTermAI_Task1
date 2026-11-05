# Cơ Sở Lý Thuyết & Kỹ Thuật Sử Dụng Trong Task 1 — N-Queens Solver

Tài liệu này trình bày **nền tảng lý thuyết** (Propositional Logic, SAT, Local Search) và **các công thức toán học** được dùng trong thư mục `AI_Task1/`.

---

## Mục lục
1. [Bài toán N-Queens](#1-bài-toán-n-queens)
2. [Mô hình hóa Propositional Logic](#2-mô-hình-hóa-propositional-logic)
3. [Thuật toán chuyển đổi sang CNF](#3-thuật-toán-chuyển-đổi-sang-cnf)
4. [Giải bằng SAT Solver (Glucose3)](#4-giải-bằng-sat-solver-glucose3)
5. [Thuật toán Min-Conflicts](#5-thuật-toán-min-conflicts)
6. [Heuristic chọn biến đề xuất](#6-heuristic-chọn-biến-đề-xuất)
7. [Phân tích thực nghiệm](#7-phân-tích-thực-nghiệm)

---

## 1. Bài toán N-Queens

Bài toán yêu cầu đặt $N$ quân hậu lên bàn cờ $N \times N$ sao cho không có hai quân hậu nào tấn công nhau. Hai quân hậu tấn công nhau nếu chúng nằm trên cùng một hàng, cùng một cột, hoặc cùng một đường chéo (chính hoặc phụ).

**Độ phức tạp:** Không gian tìm kiếm "thô" là $N^N$. Với $N=8$, số trạng thái là $8^8 \approx 16.7$ triệu. Ta cần các phương pháp mô hình hóa thông minh (SAT) hoặc tìm kiếm cục bộ (Local Search) để giải quyết.

---

## 2. Mô hình hóa Propositional Logic

Mỗi ô trên bàn cờ (hàng $r$, cột $c$) được ánh xạ thành một biến mệnh đề $X(r,c)$.
*   $X(r,c) = \text{True}$ nếu ô đó có quân hậu.
*   $X(r,c) = \text{False}$ nếu ô đó trống.

### 2.1. Ràng buộc (Constraints)
Để tạo ra một nghiệm hợp lệ, ta cần 2 loại ràng buộc:
1.  **AMO (At Most One - Nhiều nhất một):** Trên mỗi hàng, cột, và 2 đường chéo, không được có 2 quân hậu.
    $$ AMO(x_1..x_k) = \bigwedge_{i<j} (\neg x_i \vee \neg x_j) $$
2.  **ALO (At Least One - Ít nhất một):** Mỗi hàng và mỗi cột phải có ít nhất 1 quân hậu (để đảm bảo tổng cộng có đúng $N$ quân).
    $$ ALO(x_1..x_k) = (x_1 \vee x_2 \vee ... \vee x_k) $$

---

## 3. Thuật toán chuyển đổi sang CNF

Để đưa vào SAT Solver, bài toán phải ở dạng **Chuẩn hội (CNF - Conjunctive Normal Form)**: Phép AND của các mệnh đề OR.

*   **ALO** đã ở dạng CNF (1 mệnh đề OR).
*   **AMO** chuyển thành các mệnh đề 2 literal: $(\neg x_1 \vee \neg x_2), (\neg x_1 \vee \neg x_3), ...$

### 3.1. Công thức đếm số mệnh đề
Tổng số mệnh đề CNF được sinh ra là:
$$ \text{Total Clauses} = 2N + 2(N+1)\binom{N}{2} + 4\binom{N}{3} $$
*   $2N$: ALO cho $N$ hàng và $N$ cột.
*   $2(N+1)\binom{N}{2}$: AMO cho hàng và cột.
*   $4\binom{N}{3}$: AMO cho 2 đường chéo chính và 2 đường chéo phụ.
*   **Độ phức tạp:** $O(N^3)$ mệnh đề. Đây là lý do bộ giải SAT sẽ chạy chậm dần khi $N$ tăng lớn.

---

## 4. Giải bằng SAT Solver (Glucose3)

**Glucose3** là bộ giải SAT dựa trên thuật toán **CDCL** (Conflict-Driven Clause Learning). Nó hoạt động bằng cách:
1.  **Unit Propagation:** Nếu một mệnh đề chỉ còn 1 literal chưa gán, ép buộc nó phải đúng.
2.  **Conflict Learning:** Khi gặp xung đột, phân tích nguyên nhân và thêm mệnh đề mới để tránh lặp lại sai lầm.
3.  **Backjumping:** Nhảy lùi thông minh thay vì quay lui từng bước.

---

## 5. Thuật toán Min-Conflicts

Min-Conflicts là thuật toán tìm kiếm cục bộ (Local Search) cho bài toán CSP. Thay vì duyệt toàn bộ, nó bắt đầu bằng một trạng thái gán sai và liên tục sửa lỗi.
*   **Biến:** Cột $c$. **Giá trị:** Hàng $r$.
*   **Quy ước:** Mỗi cột chỉ có đúng 1 quân hậu. Do đó, ràng buộc "cùng cột" tự động được thỏa mãn.

### 5.1. Đếm xung đột trong $O(1)$
Để tăng tốc độ, hệ thống duy trì 3 mảng đếm:
*   `row_cnt[r]`: Số quân hậu trên hàng $r$.
*   `d1[r-c+N-1]`: Số quân hậu trên đường chéo chính.
*   `d2[r+c]`: Số quân hậu trên đường chéo phụ.

Số xung đột của quân hậu ở cột $c$ (hàng $r$):
$$ \text{conflicts}(c) = (\text{row\_cnt}[r] - 1) + (\text{d1}[r-c+N-1] - 1) + (\text{d2}[r+c] - 1) $$
*(Trừ 1 vì không tính chính quân hậu đó).*

---

## 6. Heuristic chọn biến đề xuất

Thuật toán Min-Conflicts chuẩn chọn biến ngẫu nhiên, dễ rơi vào cực tiểu địa phương. Hệ thống đề xuất **Heuristic MaxConflict + Noise**:
*   **Với xác suất $p=0.1$ (Noise):** Chọn ngẫu nhiên một cột đang xung đột (giúp thoát khỏi cực tiểu địa phương).
*   **Với xác suất $1-p=0.9$:** Chọn cột có số xung đột lớn nhất ($\arg\max \text{conflicts}(c)$). Sửa quân hậu "tệ nhất" giúp giảm tổng số xung đột toàn cục nhanh hơn.

---

## 7. Phân tích thực nghiệm (Tóm tắt)
*   **SAT:** Đảm bảo tìm ra nghiệm chính xác tuyệt đối. Tuy nhiên số mệnh đề tăng theo $O(N^3)$ nên thời gian tăng rất nhanh khi $N > 50$.
*   **Min-Conflicts:** Không đảm bảo tìm ra nghiệm (xác suất), nhưng tốc độ cực nhanh ở các $N$ lớn. Heuristic MaxConflict giúp giảm số bước lặp trung bình và tăng tỉ lệ thành công đáng kể so với chuẩn.