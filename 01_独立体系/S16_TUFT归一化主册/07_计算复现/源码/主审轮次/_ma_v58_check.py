# -*- coding: utf-8 -*-
import io,os
h=io.open('TUFT_企业级归一化全维架构图_E1-E336.html',encoding='utf-8-sig').read()
for tag in ['v5.7','E1–E497','勘误 #42','v5.3–v5.7 证据审计','main_agent_v53_v57_unsupported_claims','UNVERIFIED','v4.4']:
    print(tag, h.count(tag))
print('--- master ---')
m=io.open('TUFT_归一化主册_v1.0.md',encoding='utf-8-sig').read()
print('audit block', 'MainAgent 证据审计注记' in m, 'UNVERIFIED', m.count('UNVERIFIED'))
print('head line1:', m.splitlines()[0][:80])
print('--- sizes ---')
for f in ['TUFT_归一化台账_v1.0.json','TUFT_归一化主册_v1.0.md','TUFT_企业级归一化全维架构图_E1-E336.html']:
    print(f, os.path.getsize(f))
