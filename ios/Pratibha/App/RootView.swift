import SwiftUI

/// Four-tab shell. On iOS 26 the tab bar renders as Liquid Glass automatically,
/// so we lean into the system chrome rather than styling an opaque bar.
struct RootView: View {
    // Honors a launch env var (PRATIBHA_TAB) so automated runs can open a
    // specific tab; defaults to Today in normal use.
    @State private var selection: String = ProcessInfo.processInfo
        .environment["PRATIBHA_TAB"] ?? "today"

    var body: some View {
        TabView(selection: $selection) {
            Tab("Today", systemImage: "sun.horizon", value: "today") {
                TodayView()
            }
            Tab("Library", systemImage: "books.vertical", value: "library") {
                LibraryView()
            }
            Tab("Paths", systemImage: "signpost.right", value: "paths") {
                PathsView()
            }
            Tab("Ask", systemImage: "bubble.left.and.bubble.right", value: "ask") {
                AskView()
            }
        }
        .tint(Palette.goldHi)
    }
}

#Preview {
    RootView()
        .environment(CorpusStore())
        .preferredColorScheme(.dark)
}
