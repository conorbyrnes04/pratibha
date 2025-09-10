export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-black via-indigo-950 to-purple-900 text-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-5xl font-serif tracking-widest text-amber-300">Pratibha ✨</h1>
      <p className="mt-6 max-w-xl text-center text-lg text-gray-300">
        Daily verse, meditation, and luminous commentary.
      </p>
      <a href="/chat" className="mt-8 px-6 py-3 rounded-xl bg-amber-400 text-black font-semibold">Enter the Temple</a>
    </main>
  )
}
