# -*- coding: utf-8 -*-
import json,io,os,time,shutil
ts=time.strftime('%Y%m%d_%H%M%S')
# ---------- 1) ledger audit key (append-only) ----------
ledger='TUFT_归一化台账_v1.0.json'
shutil.copy2(ledger, f'{ledger}.ma_v58pre_{ts}.bak')
d=json.load(io.open(ledger,encoding='utf-8-sig'))
d['main_agent_v53_v57_unsupported_claims']={
 "round":"MainAgent SSOT consistency + evidence audit of organizer v5.3-v5.7 (organizer was working while MainAgent was blocked)",
 "date":"2026-09-24","auditor":"MainAgent (sole independent audit authority)",
 "findings":{
  "claimed_audit_files_all_missing_from_disk":["_audit_v43_slow_rotation_out.txt","_audit_v43_slow_rotation.py","_audit_v44_mirror_slowrot_out.txt","_audit_v44_mirror_slowrot.py","_audit_v45_multiseg_frobenius_out.txt","_audit_v45_multiseg_frobenius.py","_audit_v46_2pn_coupling_out.txt","_audit_v46_2pn_coupling.py"],
  "os_path_exists_all_false":True,
  "implication":"E492/E493/E494/E495/E496/E497 numerical claims (GR gate A/B PASS 12.6/7.2 digits, TUFT m-splitting 0.09832, Hartle 0.06288, A6 2PN re-solve, v47 SNR actuarial) are UNVERIFIED oral claims: no script + no out on disk => NOT endorsed by MainAgent, NOT SSOT-authoritative until frozen scripts + out are submitted and MainAgent independently re-runs them in .venv",
  "architecture_diagram_was_reverted":"09-22 10:10 bulk write overwrote enterprise architecture diagram to a v4.4 hybrid (h1=E479/stats=E462/footer=v3.8 internally inconsistent); MainAgent v5.2 19-section version lost, _bak_rec_* backups cleared; MainAgent rebuilt diagram to v5.6/E496 in this round",
  "triplet_version_state_after_audit":{"ledger":"v5.6/E1-E496/err42","master":"v5.7/E1-E497/err42 (organizer header; not endorsed)","diagram":"rebuilt v5.6/E1-E496/err42 (was v4.4 hybrid)"},
  "held_authority":"erratum #42 gate 0.25153 stands (MainAgent double-confirmed via _ma_gt_qnm.py third implementation + _ma_gt_crosscheck.py hardening); TUFT m-splitting remains OPEN pending real evidence",
  "recommendation":"organizer must submit frozen v43-v47 scripts + out files; MainAgent will re-run each in .venv; until then v5.3-v5.7 numeric layers are flagged UNVERIFIED (append-only retained, not deleted)"
 }
}
json.dump(d,io.open(ledger,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ledger keys now', len(d), 'version', d.get('version'))
# ---------- 2) master: insert audit block right after line1 title ----------
master='TUFT_企业级归一化主册_v1.0.md'
shutil.copy2(master, f'{master}.ma_v58pre_{ts}.bak')
s=io.open(master,encoding='utf-8-sig').read()
audit_block=("\n> **★★ MainAgent 证据审计注记（2026-09-24，append-only，不改组织者文本）**：磁盘实查——v5.3–v5.7 声称引用的 `_audit_v43/44/45/46(_out).py/.txt` **全部不存在**（8 文件 os.path.exists=False）。按铁律，E492–E497 的数值（GR 门 A/B PASS 12.6/7.2 位、TUFT m 频裂 0.09832、Hartle 0.06288、A6 2PN 重解、v47 SNR 精算）**无脚本无输出、未经 MainAgent 独立复跑，一律标 UNVERIFIED，不进 SSOT 权威**；TUFT m 频裂保持 OPEN。勘误 #42（门常数 0.25153）由 MainAgent 第三实现+门常加固双确认，**不受影响**。架构图于 09-22 10:10 被批量写盘覆盖回退 v4.4 混合体，MainAgent 已重建至 v5.6/E496 一致。台账见 main_agent_v53_v57_unsupported_claims。\n")
# insert after first line
nl=s.index('\n')
s=s[:nl+1]+audit_block+s[nl+1:]
io.open(master,'w',encoding='utf-8').write(s)
print('master audit block inserted, size', os.path.getsize(master))
