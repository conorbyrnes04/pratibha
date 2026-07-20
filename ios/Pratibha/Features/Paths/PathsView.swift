import SwiftUI

/// Guided journeys walked "gate by gate" — teaching → passage → practice →
/// checkpoint. Authored content, bundled, fully offline.
struct PathsView: View {
    @Environment(CorpusStore.self) private var corpus

    var body: some View {
        NavigationStack {
            PratibhaScreen {
                ScrollView {
                    VStack(alignment: .leading, spacing: 16) {
                        VStack(alignment: .leading, spacing: 6) {
                            Eyebrow(text: "Guided practice")
                            Text("Paths")
                                .font(.serifDisplay(32))
                                .foregroundStyle(Palette.parchment)
                            Text("Each path is an initiatic sequence. You advance not by reading the next gate, but by passing the one you're at.")
                                .font(.serifBody(16))
                                .foregroundStyle(Palette.muted)
                                .lineSpacing(4)
                        }
                        .padding(.bottom, 4)

                        ForEach(corpus.paths) { path in
                            NavigationLink(value: path) { PathCard(path: path) }
                                .buttonStyle(.plain)
                        }
                    }
                    .padding(20)
                    .padding(.bottom, 40)
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .navigationDestination(for: LearningPath.self) { PathDetailView(path: $0) }
            .navigationDestination(for: GateRoute.self) { GateView(route: $0) }
            .navigationDestination(for: Passage.self) { PassageDetailView(passage: $0) }
        }
    }
}

private struct PathCard: View {
    let path: LearningPath

    var body: some View {
        GlassCard {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    LayerLabel(text: path.level)
                    Spacer()
                    Text("\(path.steps.count) gates")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundStyle(Palette.muted2)
                }
                Text(path.title)
                    .font(.serifDisplay(24))
                    .foregroundStyle(Palette.parchment)
                Text(path.focus)
                    .font(.serifBody(15))
                    .foregroundStyle(Palette.gold.opacity(0.9))
                    .lineSpacing(3)
                Text(path.description)
                    .font(.serifBody(15))
                    .foregroundStyle(Palette.muted)
                    .lineSpacing(3)
                    .lineLimit(3)
                Text(path.estimatedSessions)
                    .font(.system(size: 12))
                    .foregroundStyle(Palette.muted2)
                    .padding(.top, 2)
            }
        }
    }
}
