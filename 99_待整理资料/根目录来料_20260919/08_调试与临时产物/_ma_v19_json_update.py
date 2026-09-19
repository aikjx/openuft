# -*- coding: utf-8 -*-
"""台账升 v2.0：version/latest_round/equation_range + v19 audit 对象 + backlog 转 v20。保留 CRLF。"""
import io, json
p=r"D:\a10\aikjx\code\my_lib\TUFT_归一化台账_v1.0.json"
d=json.load(io.open(p,"r",encoding="utf-8"))

d["version"]="v2.0"
d["latest_round"]="v19"
d["equation_range"]="E1-E429"

d["v19_ringdown_distortion_audit"]={
 "round":"v19","normalization":"v2.0","equations":"E419-E429 coalition",
 "script_mainagent":"_ma_v19_audit.py / _ma_v19_audit_out.txt (independent, exit0)",
 "coalition_claim":"dw_r/w_r=+2.64%, dtau/tau=-9.53%, rho_req~5.6",
 "verdict":"quantitative FALSIFIED (erratum #25), direction kept",
 "E422_fit_artifact":{
   "method":"coalition fit the transient echo train sum_n r^n h_GR(t-nT), n=0..6, with a SINGLE exponential A e^{-t/tau}cos(wt) over [2.5tau,8tau]",
   "reproduced":"0.38354 (+2.64%) / tau 10.170 (-9.53%) reproduced bit-for-bit -> proves that is the sole source",
   "window_scan_drift":"dw spans +7.41% to -3.39%, dtau spans +11.80% to -13.72% as only the fit window changes -> not a robust pole",
   "steady_state_late":"all echoes launched by 6T=83.6M=7.44tau; late-window fits return w=0.37367/tau=11.241 EXACTLY (dw=dtau=0.00%); de-enveloped late freq matches w_GR to 1.5e-16; theoretical steady residue |C|=1.06 t-independent",
   "reason":"each echo term has pole w_GR; geometric ratio r e^{T/tau}=0.729<1 converges; late h=|C|e^{-t/tau_GR}cos(w_GR t+argC): same pole, changed residue only (consistent v19 analytic skeleton sec1)",
   "physical_sign":"reflecting cavity should LENGTHEN tau (return energy, |w_i|=-ln rho/T); coalition reports tau SHORTENED -> sign also wrong"},
 "E421_E424_ratio":{
   "claimed_r_echo":0.21095,"formula":"Rbarr*e^{-T/tau}=0.72897*0.28938",
   "cancellation":"r_echo^n * e^{nT/tau} = Rbarr^n EXACTLY (n=2: .04450*e^{2T/tau}=.53140=Rbarr^2); .211/.289 cancel, true waveform ratio = Rbarr=0.729",
   "Rbarr_status":"0.729=sqrt(.5314) is v18 NET reflection with ABSORBING horizon behind barrier; required lossless two-sided OUTGOING barrier-only r_b(w) (|r|2+|t|2=1) NOT computed -> OPEN"},
 "E425_E426_snr":"REJECTED: template double-counts (uses fitted pseudo-pole w_TU AND multiplies echo factor (1+r e^{i2pi f te})); PSD is self-authored analytic formula not calibrated O4/Voyager design curve; supplementary table separately uses barrier-top WKB eps=.64 (ruled magnitude-only); rho_req=5.6 and O4 x2.5/Voy x46 void",
 "kept":{"E423":"T/tau=1.24, prompt .289 (strict, v18 reference)","E429":"C-grade direction: echo buried, no clean late echo"},
 "four_state":{"E419":"reference/conditional","E420":"reference only (no independent pole gate)",
   "E421":"reject","E422":"reject erratum25","E423":"strict(reference)","E424":"reject",
   "E425":"downgraded","E426":"reject","E427":"open(values void)","E428":"open(values void)",
   "E429":"direction kept, quantitative -9.5% void"},
 "open_v20":"modified-QNM pole shift magnitude OPEN; path: (1) lossless two-sided OUTGOING barrier IVP r_b(w) |r|2+|t|2=1, never reuse .531; (2) g=r_core*r_b incl phase, solve self-consistent D0(w)=a e^{iwT} via two-ended Frobenius x outgoing Wronskian matching (single-ended shooting ill-posed, erratum 18/19), pass Schwarzschild complex QNM >=4 digits; (3) or clean time-domain with multi-exponential/Prony/spectral pole extraction (NO single-exponential fit); (4) report SNR only CONDITIONAL on epsilon with calibrated aLIGO ZERO_DET_high_P design PSD, single physical template (no double count)"
}

# backlog 首条（v19 PRIORITY [MA analytic skeleton...]）整条替换为 v20
bl=d["open_backlog"]
idx=[i for i,x in enumerate(bl) if x.startswith("v19 PRIORITY")]
assert len(idx)==1, idx
bl[idx[0]]=("v20 PRIORITY: TRUE modified-QNM pole of R->0 reflecting cavity. v19 E422 +2.64%/-9.53% FALSIFIED "
 "(erratum #25): single-exp fit of transient echo train is window artifact, steady state returns w_GR/tau_GR "
 "exactly (1.5e-16); r_echo .211 cancels to Rbarr .729 which wrongly includes absorbing horizon; rho_req void "
 "(double-counted template, self-authored PSD). DO: (1) lossless two-sided OUTGOING barrier-only scattering IVP "
 "for r_b(w), |r|2+|t|2=1, never reuse v18 net .531; (2) g(w)=r_core*r_b, solve self-consistent pole "
 "D0(w)=a e^{iw*13.94} via two-ended Frobenius x outgoing Wronskian (pass Schwarzschild 0.37367-0.08896i >=4 "
 "digits; single-ended shooting known ill-posed); (3) or clean time-domain inject l=m=2 QNM initial data with "
 "R->0 core, extract poles by multi-exp/Prony/spectral NOT single-exp fit; (4) SNR conditional on epsilon with "
 "calibrated aLIGO/O4 design-curve PSD, one physical template. Geometry fixed: T=2L=13.9389M, T/tau=1.24, prompt .289.")

d["last_updated"]="2026-09-18"
text=json.dumps(d,ensure_ascii=False,indent=2).replace("\n","\r\n")
io.open(p,"w",encoding="utf-8",newline="").write(text)

chk=json.load(io.open(p,"r",encoding="utf-8"))
print("OK",chk["version"],chk["latest_round"],chk["equation_range"],"| v19 audit keys:",len(chk["v19_ringdown_distortion_audit"]))
print("backlog0 head:",chk["open_backlog"][0][:80])
