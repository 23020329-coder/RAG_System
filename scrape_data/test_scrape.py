import os
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import io

def scrape_url(url):
    print(f"Bắt đầu cào: {url}")
    try:
        # Gửi request để lấy dữ liệu trang
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Báo lỗi nếu kết nối thất bại
        
        # 1. Xử lý nếu URL là file PDF
        if url.endswith('.pdf') or 'application/pdf' in response.headers.get('Content-Type', ''):
            pdf_file = io.BytesIO(response.content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
            
        # 2. Xử lý nếu URL là trang web (HTML)
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Lấy tiêu đề trang
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Không có tiêu đề"
            print(f"  Tiêu đề: {title_text}")
            
            # Lấy text từ tất cả các thẻ <p>
            paragraphs = soup.find_all('p')
            text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            return text
            
    except Exception as e:
        print(f"  Lỗi khi cào {url}: {e}")
        return None

def main():
    # Đường dẫn
    path_file = r"d:\season2_3rd\RAG_System\data\path_for_data.txt"
    output_dir = r"d:\season2_3rd\RAG_System\data\raw_knowledge"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Đọc list URL từ file của bạn
    with open(path_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
        
    # CHỌN TEST 3 TRANG: 
    # urls[0]: Wikipedia Pittsburgh (Text nhiều)
    # urls[1]: pittsburghpa.gov/index.html (Trang web thành phố, HTML)
    # urls[6]: File PDF Budget (đang ở dòng 7 trong file của bạn)
    test_urls = [urls[0], urls[1], urls[6]] 
    
    for url in test_urls:
        content = scrape_url(url)
        if content:
            # Tạo tên file dễ đọc từ URL
            filename = url.split("/")[-1].replace(".html", "").replace(".pdf", "")
            if not filename:
                filename = url.split("/")[-2]
            filename = filename.replace("?", "_").replace("=", "_") + ".txt"
            
            output_path = os.path.join(output_dir, filename)
            
            # Ghi vào file
            with open(output_path, "w", encoding="utf-8") as out_f:
                out_f.write(content)
                
            print(f"  => Đã lưu: {filename} ({len(content)} ký tự)")
            print("-" * 50)

if __name__ == "__main__":
    main()
