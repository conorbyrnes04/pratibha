import SwiftUI
import SwiftData

@main
struct PratibhaApp: App {
    @State private var corpus = CorpusStore()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(corpus)
                .tint(Palette.goldHi)
                .preferredColorScheme(.dark)
        }
        .modelContainer(for: JournalEntry.self)
    }
}
