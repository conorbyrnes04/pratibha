export default function Home() {
  return (
    <main className="mx-auto min-h-[calc(100vh-60px)] max-w-6xl px-4 py-10">
      <section className="card p-8">
        <h1 className="text-4xl text-amber-200 sm:text-5xl">Study living wisdom, not just text.</h1>
        <p className="soft mt-4 max-w-3xl text-lg">
          Move from reading to understanding to practice. Start with a random verse, read chapter context, and ask grounded
          questions in study chat.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <a className="card p-4 hover:border-amber-300/30" href="/read">
            <h2 className="text-lg font-semibold text-amber-100">Library</h2>
            <p className="soft mt-2 text-sm">Browse all imported texts and chapters.</p>
          </a>
          <a className="card p-4 hover:border-amber-300/30" href="/daily">
            <h2 className="text-lg font-semibold text-amber-100">Daily</h2>
            <p className="soft mt-2 text-sm">One selected passage each day.</p>
          </a>
          <a className="card p-4 hover:border-amber-300/30" href="/random">
            <h2 className="text-lg font-semibold text-amber-100">Random</h2>
            <p className="soft mt-2 text-sm">Discover a surprising chapter and dive deeper.</p>
          </a>
          <a className="card p-4 hover:border-amber-300/30" href="/chat">
            <h2 className="text-lg font-semibold text-amber-100">Study Chat</h2>
            <p className="soft mt-2 text-sm">Ask in plain language and get practical takeaways.</p>
          </a>
          <a className="card p-4 hover:border-amber-300/30" href="/learn">
            <h2 className="text-lg font-semibold text-amber-100">Learning Paths</h2>
            <p className="soft mt-2 text-sm">Follow guided tracks from concept to practice.</p>
          </a>
        </div>
      </section>
    </main>
  );
}
