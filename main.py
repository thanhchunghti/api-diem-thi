# file: main.py
from fastapi import FastAPI, HTTPException
import sqlite3
import os

# --- Cấu hình ---
DB_FILE_PATH = 'diem_thi.db'
TABLE_NAME = 'thi_sinh'

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="API Tra Cứu Điểm Thi",
    description="API đơn giản để tra cứu điểm thi THPT bằng Số Báo Danh.",
    version="1.1.0"
)

# --- Hàm trợ giúp ---

def query_db(query: str, params: tuple = ()):
    """Hàm chung để thực hiện truy vấn an toàn vào database."""
    if not os.path.exists(DB_FILE_PATH):
        raise HTTPException(
            status_code=500, 
            detail=f"Lỗi Server: Không tìm thấy file database '{DB_FILE_PATH}'."
        )
    
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi truy vấn cơ sở dữ liệu: {e}")

# --- Các Endpoint của API ---

@app.get("/")
def read_root():
    """Trang chủ của API."""
    return {"message": "Chào mừng đến với API tra cứu điểm thi. Hãy truy cập /docs để xem tài liệu."}

@app.get("/sbd/{so_bao_danh}")
async def tra_cuu_sbd(so_bao_danh: int):
    """
    Tra cứu thông tin chi tiết của một thí sinh bằng **Số Báo Danh**.
    """
    # Câu lệnh SQL để tìm chính xác theo cột SOBAODANH
    sql_query = f'SELECT * FROM "{TABLE_NAME}" WHERE "SOBAODANH" = ?'
    results = query_db(sql_query, (so_bao_danh,))

    if not results:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy thí sinh có số báo danh: {so_bao_danh}")

    # Trả về kết quả đầu tiên (và duy nhất) tìm được
    return {"data": results[0]}