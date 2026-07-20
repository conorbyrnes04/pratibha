import Foundation
import Observation

/// Loads the bundled corpus and paths once at launch and serves them to the
/// UI. Everything is on-device: reading, search, daily, and paths work with
/// no network. Only Ask (RAG chat) needs the server.
@MainActor
@Observable
final class CorpusStore {
    private(set) var collections: [CorpusCollection] = []
    private(set) var passages: [Passage] = []
    private(set) var paths: [LearningPath] = []

    private var byId: [String: Passage] = [:]
    private var byWork: [String: [Passage]] = [:]

    init() {
        loadCorpus()
        loadPaths()
    }

    private func loadCorpus() {
        guard let url = Bundle.main.url(forResource: "corpus", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let file = try? JSONDecoder().decode(CorpusFile.self, from: data)
        else {
            assertionFailure("corpus.json missing or malformed")
            return
        }
        collections = file.collections.filter { $0.count > 0 }.sorted { $0.order < $1.order }
        passages = file.passages
        byId = Dictionary(passages.map { ($0.id, $0) }, uniquingKeysWith: { first, _ in first })
        byWork = Dictionary(grouping: passages, by: { $0.workId })
    }

    private func loadPaths() {
        guard let url = Bundle.main.url(forResource: "paths", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let file = try? JSONDecoder().decode(PathsFile.self, from: data)
        else { return }
        paths = file.paths
    }

    // MARK: - Lookups

    func passage(id: String) -> Passage? { byId[id] }
    func passages(in workId: String) -> [Passage] { byWork[workId] ?? [] }
    func collection(id: String) -> CorpusCollection? { collections.first { $0.id == id } }
    func collectionTitle(for workId: String) -> String { collection(id: workId)?.title ?? workId }

    // MARK: - Discovery

    func search(_ query: String) -> [Passage] {
        let q = query.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard !q.isEmpty else { return [] }
        return passages.filter { p in
            p.title.lowercased().contains(q)
            || p.readingText.lowercased().contains(q)
            || p.commentary.lowercased().contains(q)
            || p.themes.contains { $0.lowercased().contains(q) }
        }
    }

    /// Themes ordered by frequency, most common first.
    var popularThemes: [String] {
        var counts: [String: Int] = [:]
        for p in passages { for t in p.themes { counts[t, default: 0] += 1 } }
        return counts.sorted { $0.value > $1.value }.map(\.key)
    }

    func passages(theme: String) -> [Passage] {
        passages.filter { $0.themes.contains(theme) }
    }

    /// A stable passage for the given day — same passage all day, changes daily.
    func daily(for date: Date = Date()) -> Passage? {
        guard !passages.isEmpty else { return nil }
        let day = Calendar.current.ordinality(of: .day, in: .era, for: date) ?? 0
        return passages[day % passages.count]
    }

    func random() -> Passage? { passages.randomElement() }
}
