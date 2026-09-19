path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\main.tex"
with open(path, 'r', encoding='utf-8') as f:
    tex = f.read()

old = r"by 1.2\%, which is within the current experimental uncertainty."
new = r"by 7.4\%. The value $3.7959$ used a circular definition $\alpha_W=4\alpha_{\rm EM}$."

if old in tex:
    tex = tex.replace(old, new, 1)
    print("REPLACED")
else:
    print("NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(tex)
print("Done")
