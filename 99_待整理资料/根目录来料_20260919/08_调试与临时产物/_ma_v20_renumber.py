# -*- coding: utf-8 -*-
import io
p=r"D:\a10\aikjx\code\my_lib\TUFT_v20_modifiedQNM独立审计裁决_勘误26.md"
s=io.open(p,encoding="utf-8").read()
s=s.replace("E436（MainAgent 新增，严格认识）","@@E442_NEW@@")
s=s.replace("E430–E435","E436–E441").replace("E430-E435","E436-E441")
s=s.replace("E430–E432","E436–E438").replace("E430-E432","E436-E438")
s=s.replace("E430/E431/E432","E436/E437/E438")
for old,new in [("E435","E441"),("E434","E440"),("E433","E439"),("E432","E438"),("E431","E437"),("E430","E436")]:
    s=s.replace(old,new)
s=s.replace("@@E442_NEW@@","E442（MainAgent 新增，严格认识）")
io.open(p,"w",encoding="utf-8",newline="\r\n").write(s)
print("placeholder residual:",s.count("@@E442"))
for t in ["E436","E437","E438","E439","E440","E441","E442"]:
    print(t,s.count(t))
# 不应再出现孤立的旧 v20 编号（E430-E435 现存于主册指 v19，本裁决内应为 0）
for t in ["E430","E431","E432","E433","E434","E435"]:
    print("residual",t,s.count(t))
