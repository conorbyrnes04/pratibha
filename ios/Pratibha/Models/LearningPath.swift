import Foundation

/// A guided journey walked "gate by gate."
struct LearningPath: Codable, Identifiable, Hashable {
    let id: String
    let title: String
    let level: String
    let focus: String
    let outcome: String
    let description: String
    let arc: String
    let estimatedSessions: String
    let steps: [PathStep]
}

/// One gate in a path: a teaching, an anchor passage, a practice, a checkpoint.
struct PathStep: Codable, Identifiable, Hashable {
    let id: String
    let title: String
    let orientation: String
    let teaching: String
    let keyIdea: String
    let misconception: String
    let passageId: String
    let supportingPassageIds: [String]
    let theme: String
    let chatMode: String
    let chatPrompt: String
    let practice: String
    let journalPrompt: String
    let integration: String
}

struct PathsFile: Codable {
    let version: Int
    let pathCount: Int
    let paths: [LearningPath]
}

/// Navigation route to a single gate, carrying its path for numbering/context.
struct GateRoute: Hashable {
    let path: LearningPath
    let index: Int
    var step: PathStep { path.steps[index] }
}
