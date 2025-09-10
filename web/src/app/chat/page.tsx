'use client'
import { useState } from 'react'

export default function ChatPage() {
  const [q, setQ] = useState('')
  const [a, setA] = useState('')
  const [useRag, setUseRag] = useState(false)

  async function ask() {
    const res = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ messages: [{ role:'user', content: q }], use_rag: useRag })
    })
    const data = await res.json()
    setA(data.answer || '(no answer)')
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-indigo-950 to-black text-gray-100 p-8">
      <h1 className="text-3xl font-serif text-amber-300">Ask Pratibha</h1>
      <label className="block mt-4">
        <input type="checkbox" checked={useRag} onChange={e=>setUseRag(e.target.checked)} /> Use RAG
      </label>
      <textarea className="mt-3 w-full max-w-2xl p-3 rounded bg-gray-900 border border-amber-300"
        rows={5} value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask about ŚS 1.2…" />
      <div className="mt-3">
        <button onClick={ask} className="px-5 py-2 rounded bg-amber-400 text-black font-semibold">Ask</button>
      </div>
      {a && <pre className="mt-6 max-w-2xl p-4 rounded bg-gray-800 border border-amber-400 whitespace-pre-wrap">{a}</pre>}
    </main>
  )
}