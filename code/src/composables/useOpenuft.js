import { reactive, computed } from 'vue'
import base from '@/data/openuft-graph.json'

const STORE_KEY = 'openuft_user_rounds_v1'

function loadUserRounds() {
  try {
    const raw = localStorage.getItem(STORE_KEY)
    if (!raw) return []
    const arr = JSON.parse(raw)
    return Array.isArray(arr) ? arr : []
  } catch (e) {
    return []
  }
}

function saveUserRounds(list) {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(list)) } catch (e) { /* ignore quota */ }
}

// ---- reactive singleton state ----
const state = reactive({
  base,
  userRounds: loadUserRounds()
})

function allRounds() {
  return [...base.rounds, ...state.userRounds]
}

// ---- graph builder ----
function buildGraph() {
  const rounds = allRounds()
  const nodes = []
  const edges = []
  const idSet = new Set()

  const push = (n) => { if (!idSet.has(n.id)) { nodes.push(n); idSet.add(n.id) } }

  // hubs: themes
  base.themes.forEach(t => push({ id: t.id, type: 'theme', label: t.name, verdict: t.verdict, color: t.color }))
  // rounds
  rounds.forEach(r => push({ id: r.id, type: 'round', label: r.id, verdict: r.verdict, color: r.verdict === 'FAIL' ? 'var(--fail)' : (r.verdict === 'PASS' ? 'var(--ok)' : 'var(--boundary)') }))
  // blacklist
  base.blacklist.forEach(b => push({ id: b.id, type: 'blacklist', label: b.id, verdict: 'BAN', color: 'var(--fail)' }))
  // cores
  base.cores.forEach(c => push({ id: c.id, type: 'core', label: c.id, verdict: c.status === 'correct' ? 'OK' : 'DOWN', color: c.status === 'correct' ? 'var(--ok)' : 'var(--boundary)' }))

  // edges: round -> theme (member)
  rounds.forEach(r => {
    if (r.theme) edges.push({ source: r.id, target: r.theme, kind: 'member' })
    ;(r.blacklists || []).forEach(b => edges.push({ source: r.id, target: b, kind: 'registers' }))
    ;(r.downgrades || []).forEach(k => edges.push({ source: r.id, target: k, kind: 'downgrades' }))
  })

  return { nodes, edges }
}

const graph = computed(buildGraph)
const roundsAll = computed(allRounds)
const themes = computed(() => base.themes)
const cores = computed(() => base.cores)
const blacklist = computed(() => base.blacklist)
const spiral = computed(() => base.spiral)
const domains = computed(() => base.domains)
const cosmic = computed(() => base.cosmicEssence)
const correctSystem = computed(() => base.correctSystem)
const criteria = computed(() => base.auditCriteria)
const meta = computed(() => base.meta)

// ---- workbench: add / remove user round ----
function addUserRound(payload) {
  const id = payload.id || ('u' + Date.now().toString(36))
  const rec = {
    id,
    title: payload.title,
    verdict: payload.verdict,
    theme: payload.theme,
    date: new Date().toISOString().slice(0, 10),
    target: payload.target,
    conclusion: payload.conclusion,
    blacklists: payload.blacklists || [],
    downgrades: payload.downgrades || [],
    user: true
  }
  state.userRounds.unshift(rec)
  saveUserRounds(state.userRounds)
  return rec
}

function removeUserRound(id) {
  state.userRounds = state.userRounds.filter(r => r.id !== id)
  saveUserRounds(state.userRounds)
}

function clearUserRounds() {
  state.userRounds = []
  saveUserRounds([])
}

export function useOpenuft() {
  return {
    state, meta, themes, cores, blacklist, spiral, domains, cosmic, correctSystem, criteria,
    graph, roundsAll, allRounds, addUserRound, removeUserRound, clearUserRounds
  }
}
