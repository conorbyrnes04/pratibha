import Foundation
import SwiftData

/// A private contemplative reflection, tied to a passage. Stored on device
/// with SwiftData; syncs via iCloud when the user enables it (later phase).
@Model
final class JournalEntry {
    var id: UUID
    var passageId: String
    var passageTitle: String
    var prompt: String
    var text: String
    var createdAt: Date

    init(passageId: String, passageTitle: String, prompt: String, text: String) {
        self.id = UUID()
        self.passageId = passageId
        self.passageTitle = passageTitle
        self.prompt = prompt
        self.text = text
        self.createdAt = Date()
    }
}
