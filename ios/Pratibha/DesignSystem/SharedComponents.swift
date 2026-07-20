import SwiftUI

/// A compact passage row for lists. Wrap in a `NavigationLink(value:)`.
struct PassageRow: View {
    let passage: Passage
    var showCollection: Bool = true
    @Environment(CorpusStore.self) private var corpus

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(passage.title)
                .font(.serifBody(18, weight: .medium))
                .foregroundStyle(Palette.parchment)
                .lineLimit(2)

            if showCollection {
                Text(subtitle)
                    .font(.system(size: 12))
                    .foregroundStyle(Palette.muted2)
            }

            Text(passage.readingText)
                .font(.system(size: 14))
                .foregroundStyle(Palette.muted)
                .lineLimit(2)
                .lineSpacing(2)

            if !passage.themes.isEmpty {
                Text(passage.themes.prefix(3).joined(separator: " · "))
                    .font(.system(size: 11, weight: .medium))
                    .foregroundStyle(Palette.gold.opacity(0.85))
            }
        }
        .padding(.vertical, 4)
    }

    private var subtitle: String {
        let coll = corpus.collectionTitle(for: passage.workId)
        return passage.unitLabel.isEmpty ? coll : "\(coll) · \(passage.unitLabel)"
    }
}

/// Long prose that trims to a limit with a "Continue reading" toggle.
struct ExpandableText: View {
    let text: String
    var limit: Int = 340
    @State private var expanded = false

    var body: some View {
        let needsTrim = text.count > limit
        VStack(alignment: .leading, spacing: 12) {
            Text(AttributedString.fromCommentary(displayed(needsTrim: needsTrim)))
                .font(.serifBody(16))
                .foregroundStyle(Palette.parchment.opacity(0.92))
                .lineSpacing(5)
                .textSelection(.enabled)

            if needsTrim {
                Button {
                    withAnimation(.easeInOut(duration: 0.25)) { expanded.toggle() }
                } label: {
                    Text(expanded ? "Show less" : "Continue reading")
                        .font(.system(size: 13, weight: .semibold))
                        .foregroundStyle(Palette.goldHi)
                }
                .buttonStyle(.plain)
            }
        }
    }

    private func displayed(needsTrim: Bool) -> String {
        guard needsTrim, !expanded else { return text }
        return String(text.prefix(limit)).trimmingCharacters(in: .whitespacesAndNewlines) + "…"
    }
}

/// A highlighted single idea (gold) — used for the "key idea" of a gate.
struct KeyIdeaCallout: View {
    let label: String
    let text: String

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Rectangle()
                .fill(Palette.gold)
                .frame(width: 2)
            VStack(alignment: .leading, spacing: 6) {
                LayerLabel(text: label)
                Text(text)
                    .font(.serifBody(17, weight: .medium))
                    .foregroundStyle(Palette.goldHi)
                    .lineSpacing(3)
            }
        }
    }
}

/// A rounded, prominent action button in gold.
struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 15, weight: .semibold))
            .foregroundStyle(Palette.ink)
            .padding(.vertical, 12)
            .padding(.horizontal, 20)
            .frame(maxWidth: .infinity)
            .background {
                Capsule().fill(LinearGradient(colors: [Palette.goldHi, Palette.gold],
                                              startPoint: .top, endPoint: .bottom))
            }
            .opacity(configuration.isPressed ? 0.85 : 1)
            .scaleEffect(configuration.isPressed ? 0.98 : 1)
    }
}
