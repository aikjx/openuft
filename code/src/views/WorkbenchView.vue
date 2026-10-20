<template>
  <div>
    <div class="page-head">
      <div class="page-title">攻破工作台 · 持续突破机制</div>
      <div class="page-sub">录入一个新宣称，套用本库沉淀的审计判据逐条自检，生成机读 verdict 并存为新的攻破轮——它立即进入关联图谱与攻破链。所有新增仅留存在本机浏览器（localStorage），可导出为与 53 引擎同 schema 的 JSON。</div>
    </div>

    <div class="grid grid-1-1">
      <!-- form -->
      <div class="card">
        <div class="card-title">登记新宣称</div>
        <label class="field">宣称标题 <span class="req">*</span></label>
        <input v-model="form.title" :class="{ 'input-error': err }" placeholder="例如：某理论称光子内部存在 X 结构" />
        <div class="err-line" v-if="err">{{ err }}</div>
        <label class="field">关联主题</label>
        <select v-model="form.theme">
          <option v-for="t in themes" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <label class="field">靶宣称（被攻破的对象）</label>
        <input v-model="form.target" placeholder="该宣称主张什么" />
        <label class="field">内容与依据（文本/链接）</label>
        <textarea v-model="form.content" placeholder="粘贴关键推导或结论；工作台不重判，只记录你的判定"></textarea>
        <label class="field">自定义编号（可选，留空自动生成）</label>
        <input v-model="form.id" placeholder="如 r124 / u-xxx" />

        <div class="card-title" style="margin-top:16px">审计判据自检 <span class="tag">机读守卫</span></div>
        <div v-for="c in criteria" :key="c.id" class="crit">
          <div class="crit-head">
            <b>{{ c.name }}</b>
            <div class="seg" style="margin-left:auto">
              <button :class="{active: guardState[c.id]==='pass'}" @click="guardState[c.id]='pass'">通过</button>
              <button :class="{active: guardState[c.id]==='fail'}" @click="guardState[c.id]='fail'">失败</button>
              <button :class="{active: guardState[c.id]==='na'}" @click="guardState[c.id]='na'">不适用</button>
            </div>
          </div>
          <div class="crit-desc">{{ c.desc }}</div>
          <input v-if="guardState[c.id]!=='na'" v-model="guardNotes[c.id]" class="crit-note" :placeholder="guardState[c.id]==='fail'?'失败证据/缺口…':'通过证据…'" />
        </div>

        <div class="verdict-box" :class="'vb-'+computedVerdict">
          <span class="vb-label">机读判决</span>
          <span class="vb-val">{{ computedVerdict }}</span>
          <span class="vb-sub">失败守卫 {{ failCount }} · 通过 {{ passCount }} · 不适用 {{ naCount }}</span>
        </div>

        <div class="btn-row">
          <button class="btn btn-primary" @click="commit">登记为攻破轮</button>
          <button class="btn" @click="reset">重置</button>
        </div>
      </div>

      <!-- user rounds + criteria library -->
      <div>
        <div class="card" style="margin-bottom:16px">
          <div class="card-title">审计判据库 <span class="tag tag-info">REUSABLE</span></div>
          <div v-for="c in criteria" :key="c.id" class="lib-row">
            <b>{{ c.name }}</b><span class="dim" style="font-size:11.5px;margin-top:3px;display:block">{{ c.desc }}</span>
          </div>
        </div>
        <div class="card">
          <div class="card-title">
            已登记的攻破轮 <span class="tag">{{ userRounds.length }}</span>
            <button v-if="userRounds.length" class="btn btn-sm" style="margin-left:auto" @click="exportJson">导出 JSON</button>
          </div>
          <div v-if="!userRounds.length" class="empty-state">尚无新增。登记第一条即可让它在关联图谱中诞生节点。</div>
          <div v-for="r in userRounds" :key="r.id" class="ur-row">
            <div class="ur-head">
              <span class="mono">{{ r.id }}</span>
              <span :class="verdictClass(r.verdict)" style="margin-left:8px">{{ r.verdict }}</span>
              <button class="ur-del" @click="remove(r.id)">删除</button>
            </div>
            <div class="ur-title">{{ r.title }}</div>
            <div class="ur-target dim">{{ r.target }}</div>
            <p class="ur-concl dim">{{ r.conclusion }}</p>
          </div>
          <button v-if="userRounds.length" class="btn" style="margin-top:8px" @click="clear">清空全部</button>
        </div>
      </div>
    </div>
    <div class="toast" v-if="toast">✔ {{ toast }}</div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useOpenuft } from '@/composables/useOpenuft.js'
const { themes, criteria, state, addUserRound, removeUserRound, clearUserRounds } = useOpenuft()

const form = reactive({ title: '', theme: 'T-photon', target: '', content: '', id: '' })
const guardState = reactive({})
const guardNotes = reactive({})
const err = ref('')
const toast = ref('')
criteria.value.forEach(c => { guardState[c.id] = 'na'; guardNotes[c.id] = '' })

const failCount = computed(() => Object.values(guardState).filter(v => v === 'fail').length)
const passCount = computed(() => Object.values(guardState).filter(v => v === 'pass').length)
const naCount = computed(() => Object.values(guardState).filter(v => v === 'na').length)
const computedVerdict = computed(() => failCount.value > 0 ? 'FAIL' : (passCount.value > 0 ? 'PASS' : 'BOUNDARY'))

const userRounds = computed(() => state.userRounds)

function buildConclusion() {
  const lines = ['机读守卫自检：']
  criteria.value.forEach(c => {
    const s = guardState[c.id]
    if (s === 'na') return
    lines.push(`- ${c.name}：${s === 'fail' ? '失败' : '通过'}${guardNotes[c.id] ? '（' + guardNotes[c.id] + '）' : ''}`)
  })
  lines.push(`\n内容依据：${form.content || '（未填）'}`)
  return lines.join('\n')
}

function commit() {
  if (!form.title.trim()) { err.value = '请填写宣称标题'; return }
  err.value = ''
  const rec = addUserRound({
    id: form.id.trim() || undefined,
    title: form.title.trim(),
    verdict: computedVerdict.value,
    theme: form.theme,
    target: form.target.trim() || '（未指定）',
    conclusion: buildConclusion()
  })
  toast.value = `已登记攻破轮 ${rec.id}（verdict=${rec.verdict}）`
  setTimeout(() => { toast.value = '' }, 4000)
  reset()
}

// 导出与 53 引擎 round 记录同 schema 的 JSON，便于真正入账本
function exportJson() {
  const payload = {
    schema: 'openuft-user-rounds/v1',
    exported: new Date().toISOString(),
    source: 'openuft/code 攻破工作台（localStorage）',
    rounds: state.userRounds.map(r => ({
      id: r.id, title: r.title, verdict: r.verdict, theme: r.theme,
      date: r.date, target: r.target, conclusion: r.conclusion,
      blacklists: r.blacklists || [], downgrades: r.downgrades || [], user: true
    }))
  }
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `openuft_user_rounds_${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(a.href)
}

function reset() {
  form.title = ''; form.target = ''; form.content = ''; form.id = ''
  criteria.value.forEach(c => { guardState[c.id] = 'na'; guardNotes[c.id] = '' })
}
function remove(id) { removeUserRound(id) }
function clear() { if (confirm('确认清空全部本地攻破轮？')) clearUserRounds() }
function verdictClass(v) { return (v === 'FAIL') ? 'tag-fail' : (v === 'PASS' ? 'tag-ok' : 'tag-boundary') }
</script>

<style scoped>
.req { color: var(--fail); }
.input-error { border-color: var(--fail) !important; }
.err-line { font-size: 11.5px; color: var(--fail); margin-top: 5px; }
.btn-row { display: flex; gap: 10px; margin-top: 14px; align-items: center; }
.btn-sm { padding: 4px 10px; font-size: 11.5px; }
.toast {
  position: fixed; bottom: 22px; left: 50%; transform: translateX(-50%);
  background: var(--panel-2); border: 1px solid var(--ok); color: var(--text);
  padding: 9px 18px; border-radius: 10px; font-size: 12.5px; z-index: 60;
  box-shadow: var(--shadow);
}
.crit { padding: 9px 0; border-bottom: 1px solid var(--line-soft); }
.crit-head { display: flex; align-items: center; gap: 10px; font-size: 13px; }
.crit-desc { font-size: 11.5px; color: var(--text-mute); line-height: 1.55; margin: 5px 0; }
.crit-note { margin-top: 6px; font-size: 12px; }
.verdict-box { margin-top: 14px; padding: 12px 15px; border-radius: 10px; display: flex; align-items: center; gap: 12px; border: 1px solid var(--line); }
.vb-label { font-size: 12px; color: var(--text-mute); }
.vb-val { font-size: 20px; font-weight: 800; }
.vb-sub { font-size: 11px; color: var(--text-dim); margin-left: auto; }
.vb-FAIL { background: rgba(255,93,108,.12); } .vb-FAIL .vb-val { color: var(--fail); }
.vb-PASS { background: rgba(46,194,126,.12); } .vb-PASS .vb-val { color: var(--ok); }
.vb-BOUNDARY { background: rgba(245,177,61,.12); } .vb-BOUNDARY .vb-val { color: var(--boundary); }
.lib-row { padding: 7px 0; border-bottom: 1px solid var(--line-soft); font-size: 12.5px; }
.lib-row:last-child { border-bottom: none; }
.ur-row { padding: 10px 0; border-bottom: 1px solid var(--line-soft); }
.ur-row:last-child { border-bottom: none; }
.ur-head { display: flex; align-items: center; gap: 4px; font-size: 12.5px; }
.ur-del { margin-left: auto; background: none; border: 1px solid var(--line); color: var(--fail); border-radius: 6px; padding: 2px 8px; font-size: 11px; cursor: pointer; }
.ur-title { font-size: 13px; margin: 4px 0; color: var(--text); }
.ur-target { font-size: 11.5px; }
.ur-concl { font-size: 11.5px; line-height: 1.55; white-space: pre-wrap; margin: 5px 0 0; }
</style>
