import SwiftUI
import SwiftData

/// The arrival screen — opens where practice left off, not on a menu.
/// Daily passage, the path you're mid-way through, and your last reflection.
struct TodayView: View {
    @Environment(CorpusStore.self) private var corpus
    @Query(sort: \JournalEntry.createdAt, order: .reverse) private var entries: [JournalEntry]
    @State private var drawn: Passage?

    var body: some View {
        NavigationStack {
            PratibhaScreen {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        header

                        if let daily = corpus.daily() {
                            NavigationLink(value: daily) { DailyCard(passage: daily) }
                                .buttonStyle(.plain)
                        }

                        Button {
                            drawn = corpus.random()
                        } label: {
                            Label("Draw a fresh passage", systemImage: "shuffle")
                                .font(.system(size: 14, weight: .medium))
                                .foregroundStyle(Palette.goldHi)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 12)
                                .background {
                                    Capsule().strokeBorder(Palette.goldLine, lineWidth: 1)
                                }
                        }
                        .buttonStyle(.plain)

                        if let path = corpus.paths.first {
                            NavigationLink(value: path) { ContinuePathCard(path: path) }
                                .buttonStyle(.plain)
                        }

                        if let last = entries.first,
                           let passage = corpus.passage(id: last.passageId) {
                            NavigationLink(value: passage) { ReflectionRecallCard(entry: last) }
                                .buttonStyle(.plain)
                        }
                    }
                    .padding(20)
                    .padding(.bottom, 40)
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .navigationDestination(for: Passage.self) { PassageDetailView(passage: $0) }
            .navigationDestination(for: LearningPath.self) { PathDetailView(path: $0) }
            .navigationDestination(item: $drawn) { PassageDetailView(passage: $0) }
            .onAppear {
                // Automated-run hook: open the daily passage on launch.
                if ProcessInfo.processInfo.environment["PRATIBHA_OPEN_DAILY"] == "1" {
                    drawn = corpus.daily()
                }
            }
        }
    }

    private var header: some View {
        HStack(alignment: .center) {
            VStack(alignment: .leading, spacing: 6) {
                Eyebrow(text: dateLine)
                Text(greeting)
                    .font(.serifDisplay(34))
                    .foregroundStyle(Palette.parchment)
            }
            Spacer()
            YantraView(size: 78)
        }
        .padding(.top, 8)
    }

    private var greeting: String {
        let hour = Calendar.current.component(.hour, from: Date())
        switch hour {
        case 5..<12: return "A still morning"
        case 12..<17: return "Good afternoon"
        case 17..<22: return "A quiet evening"
        default: return "Late, and awake"
        }
    }

    private var dateLine: String {
        let f = DateFormatter()
        f.dateFormat = "EEEE, d MMMM"
        return f.string(from: Date())
    }
}

private struct DailyCard: View {
    let passage: Passage
    @Environment(CorpusStore.self) private var corpus

    var body: some View {
        GlassCard {
            VStack(alignment: .leading, spacing: 10) {
                LayerLabel(text: "Today's passage · \(corpus.collectionTitle(for: passage.workId))")
                if passage.hasOriginalScript {
                    Text(passage.devanagari)
                        .font(.serifBody(20))
                        .foregroundStyle(Palette.goldHi)
                        .lineSpacing(6)
                        .lineLimit(2)
                }
                Text(passage.title)
                    .font(.serifDisplay(22))
                    .foregroundStyle(Palette.parchment)
                Text(passage.readingText)
                    .font(.serifBody(16))
                    .foregroundStyle(Palette.muted)
                    .lineSpacing(4)
                    .lineLimit(3)
                Text("Read all seven layers →")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundStyle(Palette.goldHi)
                    .padding(.top, 2)
            }
        }
    }
}

private struct ContinuePathCard: View {
    let path: LearningPath

    var body: some View {
        GlassCard(tone: .lapis) {
            VStack(alignment: .leading, spacing: 8) {
                LayerLabel(text: "Continue · \(path.title)", color: Color(hex: 0xB9CDEA))
                Text(path.steps.first?.title ?? path.focus)
                    .font(.serifBody(18, weight: .medium))
                    .foregroundStyle(Palette.parchment)
                Text("\(path.steps.count) gates · \(path.estimatedSessions)")
                    .font(.system(size: 12))
                    .foregroundStyle(Palette.muted)
            }
        }
    }
}

private struct ReflectionRecallCard: View {
    let entry: JournalEntry

    var body: some View {
        GlassCard(tone: .practice) {
            VStack(alignment: .leading, spacing: 8) {
                LayerLabel(text: "Return to your reflection", color: Palette.vermillion)
                Text(entry.passageTitle)
                    .font(.serifBody(17, weight: .medium))
                    .foregroundStyle(Palette.parchment)
                Text(entry.text)
                    .font(.serifBody(15))
                    .foregroundStyle(Palette.muted)
                    .lineSpacing(3)
                    .lineLimit(2)
            }
        }
    }
}
