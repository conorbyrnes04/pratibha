import Foundation

/// One canonical unit — a sūtra, verse, fragment, or teaching passage.
struct Passage: Codable, Identifiable, Hashable {
    let id: String
    let workId: String
    let title: String
    let unitLabel: String
    let unitType: String
    let category: String
    let devanagari: String
    let iast: String
    let primary: String
    let translation: String
    let sourceExcerpt: String
    let commentary: String
    let thesis: String
    let insight: String
    let practice: String
    let section: String
    let themes: [String]
    let qualityScore: Int

    var isRootText: Bool { category == "root_text" }
    var hasOriginalScript: Bool { !devanagari.isEmpty }
    var hasTransliteration: Bool { !iast.isEmpty }
    var hasPractice: Bool { !practice.isEmpty }
    var hasCommentary: Bool { !commentary.isEmpty }

    /// The main reading line — translation for root texts, source excerpt otherwise.
    var readingText: String { translation.isEmpty ? primary : translation }

    /// Show `insight` as a pull-quote only when it adds something the commentary
    /// doesn't already open with, and is short enough to read as an epigraph.
    var pullQuote: String? {
        let ins = insight.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !ins.isEmpty, ins.count <= 180 else { return nil }
        if commentary.hasPrefix(ins) { return nil }
        if ins == readingText { return nil }
        return ins
    }
}
