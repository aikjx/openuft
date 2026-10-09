import fitz
import os

def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    print(f"页面数: {len(doc)}")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    img_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        print(f"页面 {page_num + 1}: {len(images)} 张图片")
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            img_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            img_path = os.path.join(output_folder, img_filename)
            
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            img_count += 1
            print(f"  提取: {img_filename}")
    
    print(f"\n共提取 {img_count} 张图片")
    doc.close()

if __name__ == "__main__":
    # PDF 与输出目录为库外路径，由环境变量 PDF_SRC_DIR 指定
    src_dir = os.environ.get("PDF_SRC_DIR", "")
    if not src_dir:
        raise SystemExit("请先设置环境变量 PDF_SRC_DIR 为 PDF 所在目录（库外路径）")
    pdf_path = os.path.join(src_dir, "·几何本源（补卷）(1).pdf")
    output_folder = os.path.join(src_dir, "images")
    extract_images_from_pdf