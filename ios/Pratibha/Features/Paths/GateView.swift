import SwiftUI

/// A single gate: orientation → teaching → key idea → the anchor passage →
/// a practice to do → a reflection → the integration checkpoint that must
/// ripen before moving on.
struct GateView: View {
    let route: GateRoute
    @Environment(CorpusStore.self) private var corpus
    @State private var showReflection = false

    private var step: PathStep { route.step }

    var body: some View {
        PratibhaScreen {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    VStack(alignment: .leading, spacing: 10) {
                        Eyebrow(text: "Gate \(route.index + 1) · \(route.path.title)")
                        Text(step.title)
                            .font(.serifDisplay(30))
                            .foregroundStyle(Palette.parchment)
                        Text(step.orientation)
                            .font(.serifBody(16))
                            .italic()
                            .foregroundStyle(Palette.muted)
                            .lineSpacing(4)
                    }

                    Text(AttributedString.fromCommentary(step.teaching))
                        .font(.serifBody(17))
                        .foregroundStyle(Palette.parchment.opacity(0.92))
                        .lineSpacing(6)

                    KeyIdeaCallout(label: "The one idea", text: step.keyIdea)

                    if !step.misconception.isEmpty {
                        GlassCard {
                            VStack(alignment: .leading, spacing: 8) {
                                LayerLabel(text: "A common misunderstanding", color: Palette.muted)
                                Text(step.misconception)
                                    .font(.serifBody(16))
                                    .foregroundStyle(Palette.muted)
                                    .lineSpacing(4)
                            }
                        }
                    }

                    if let anchor = corpus.passage(id: step.passageId) {
                        anchorLink(anchor)
                    }

                    let supporting = step.supportingPassageIds.compactMap { corpus.passage(id: $0) }
                    if !supporting.isEmpty {
                        VStack(alignment: .leading, spacing: 10) {
                            LayerLabel(text: "Resonant readings")
                            ForEach(supporting) { p in
                                NavigationLink(value: p) {
                                    HStack(spacing: 8) {
                                        Image(systemName: "arrow.up.right")
                                            .font(.system(size: 11, weight: .bold))
                                        Text("\(p.title) · \(corpus.collectionTitle(for: p.workId))")
                                            .font(.serifBody(15))
                                            .lineLimit(1)
                                    }
                                    .foregroundStyle(Palette.goldHi)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                    }

                    GlassCard(tone: .practice) {
                        VStack(alignment: .leading, spacing: 8) {
                            LayerLabel(text: "The practice", color: Palette.vermillion)
                            Text(step.practice)
                                .font(.serifBody(17))
                                .foregroundStyle(Palette.parchment)
                                .lineSpacing(5)
                        }
                    }

                    Button { showReflection = true } label: {
                        Label("Reflect on this gate", systemImage: "square.and.pencil")
                    }
                    .buttonStyle(PrimaryButtonStyle())

                    GlassCard(tone: .lapis) {
                        VStack(alignment: .leading, spacing: 8) {
                            LayerLabel(text: "Before you pass this gate", color: Color(hex: 0xB9CDEA))
                            Text(step.integration)
                                .font(.serifBody(16))
                                .foregroundStyle(Palette.parchment)
                                .lineSpacing(4)
                        }
                    }
                }
                .padding(20)
                .padding(.bottom, 40)
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showReflection) {
            ReflectionEditor(
                passageId: step.passageId,
                passageTitle: step.title,
                prompt: step.journalPrompt
            )
        }
    }

    private func anchorLink(_ passage: Passage) -> some View {
        NavigationLink(value: passage) {
            GlassCard {
                VStack(alignment: .leading, spacing: 8) {
                    LayerLabel(text: "Sit with the passage")
                    Text(passage.title)
                        .font(.serifBody(18, weight: .medium))
                        .foregroundStyle(Palette.parchment)
                    if passage.hasOriginalScript {
                        Text(passage.devanagari)
                            .font(.serifBody(17))
                            .foregroundStyle(Palette.goldHi)
                            .lineLimit(1)
                    }
                    Text(passage.readingText)
                        .font(.serifBody(15))
                        .foregroundStyle(Palette.muted)
                        .lineLimit(2)
                    Text("Open all seven layers →")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(Palette.goldHi)
                }
            }
        }
        .buttonStyle(.plain)
    }
}
