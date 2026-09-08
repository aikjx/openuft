import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'code' / 'dodobot'))

from pdf_to_longimage import PDFToLongImage


def batch_convert_pdf_to_images(root_dir):
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

    pdf_files = []
    for subdir in sorted(root.iterdir()):
        if subdir.is_dir():
            for file in subdir.glob('*.pdf'):
                pdf_files.append(file)

    print(f"找到 {len(pdf_files)} 个PDF文件")
    print("=" * 80)

    success_count = 0
    fail_count = 0

    for pdf_file in pdf_files:
        try:
            output_dir = pdf_file.parent / 'img'
            output_dir.mkdir(parents=True, exist_ok=True)

            print(f"\n处理: {pdf_file.name}")
            print(f"输出目录: {output_dir}")

            output_paths = converter.convert(
                str(pdf_file),
                str(output_dir),
                output_with_file_dir=True,
            )

            print(f"完成: 生成 {len(output_paths)} 张图片")
            success_count += 1
        except Exception as e:
            print(f"失败: {e}")
            fail_count += 1

    print("\n" + "=" * 80)
    print(f"处理完成: {success_count} 成功, {fail_count} 失败")


if __name__ == "__main__":
    root_dir = r"d:\a10\aikjx\code\my_lib\article\zh\2026\7\4\乖乖数学"
    print(f"批量转换PDF到图片")
    print(f"源目录: {root_dir}")
    batch_convert_pdf_to_images(root_dir)