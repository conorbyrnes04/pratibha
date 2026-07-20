import Foundation

/// A collection (work) — e.g. Śiva Sūtra — with curated display metadata.
struct CorpusCollection: Codable, Identifiable, Hashable {
    let id: String
    let title: String
    let tradition: String
    let blurb: String
    let order: Int
    let count: Int
}

/// Top-level shape of the bundled `corpus.json`.
struct CorpusFile: Codable {
    let version: Int
    let passageCount: Int
    let collectionCount: Int
    let collections: [CorpusCollection]
    let passages: [Passage]
}
