import sys
filepath = r"d:\a10\aikjx\code\my_lib\utf\gaq_uft_v8_rc1_full_validation.py"
try:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print("OK", len(lines))
except Exception as e:
    print("ERR", e)
    # Try with unicode in filename
    import os
    d = r"d:\a10\aikjx\code\my_lib\utf"
    files = os.listdir(d)
    for fn in files:
        if "gaq_uft" in fn:
            print("FOUND:", repr(fn))
