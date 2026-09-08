import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'code' / 'dodobot'))

from pdf_to_longimage import PDFToLongImage


def convert_missing_pdfs(root_dir):
    root = Path(root_dir)
    converter = PDFToLongImage(
        max_pages=4,
        max_size_mb=10.0,
        quality=98,
        dpi=300,
        force_single=False,
        output_format='jpg',
        background_color='white',
        margin=0,
        trim_whitespace=True,
        antialias=True,
        use_lcd_rendering=True,
    )

    for subdir in sorted(root.iterdir()):
        if subdir.is_dir():
            pdf_files = list(subdir.glob('*.pdf'))
            img_dir = subdir / 'img'
            
            if pdf_files and not img_dir.exists():
                for pdf_file in pdf_files:
                    print(f"\n处理: {pdf_file.name}")
                    print(f"输出目录: {img_dir}")
                    
                    output_paths = converter.convert(
                        str(pdf_file),
                        str(img_dir),
                        output_with_file_dir=True,
                    )
                    
                    print(f"完成: 生成 {len(output_paths)} 张图片")


if __name__ == "__main__":
    root_dir = r"d:\a10\aikjx\code\my_lib\article\zh\2026\7\4\乖乖数学"
    print(f"处理遗漏的PDF转换")
    print(f"源目录: {root_dir}")
    convert_missing_pdfs(root_dir)
    print("\n完成")