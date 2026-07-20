import SwiftUI

/// Phase 1 surface for Ask. The RAG conversation is the one feature that must
/// reach the server (retrieval + LLM), so it arrives with the Conversation
/// phase. Reading, Library, and Paths all work fully offline without it.
/// This screen states the value plainly rather than shipping a dead input.
struct AskView: View {
    var body: some View {
        NavigationStack {
            PratibhaScreen {
                ScrollView {
                    VStack(alignment: .leading, spacing: 18) {
                        VStack(alignment: .leading, spacing: 8) {
                            Eyebrow(text: "Grounded in the corpus")
                            Text("Ask")
                                .font(.serifDisplay(34))
                                .foregroundStyle(Palette.parchment)
                            Text("Ask in plain language and receive an answer grounded in the texts — with tappable citations back to the exact passage.")
                                .font(.serifBody(17))
                                .foregroundStyle(Palette.muted)
                                .lineSpacing(5)
                        }

                        GlassCard {
                            VStack(alignment: .leading, spacing: 10) {
                                LayerLabel(text: "What it does")
                                bullet("Every claim cites its source passage — no ungrounded answers.")
                                bullet("Structured replies: a direct answer, a source-grounded insight, a concrete practice, and a reflection question.")
                                bullet("Two Voices — let two traditions speak to the same question, then converge.")
                            }
                        }

                        GlassCard(tone: .lapis) {
                            VStack(alignment: .leading, spacing: 8) {
                                LayerLabel(text: "Example questions", color: Color(hex: 0xB9CDEA))
                                ForEach(examples, id: \.self) { q in
                                    Text("“\(q)”")
                                        .font(.serifBody(15))
                                        .italic()
                                        .foregroundStyle(Palette.parchment.opacity(0.9))
                                        .lineSpacing(3)
                                }
                            }
                        }

                        GlassCard(tone: .practice) {
                            VStack(alignment: .leading, spacing: 8) {
                                LayerLabel(text: "Coming with Pratibhā+", color: Palette.vermillion)
                                Text("Reading every layer, the full library, guided paths, and your private journal are free and work offline. Ask is the intelligence layer — it connects to the study engine and arrives in the next release.")
                                    .font(.serifBody(15))
                                    .foregroundStyle(Palette.muted)
                                    .lineSpacing(4)
                            }
                        }
                    }
                    .padding(20)
                    .padding(.bottom, 40)
                }
            }
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private let examples = [
        "Explain this passage in plain language.",
        "How do the Stoics and the Upaniṣads differ on facing death?",
        "Give me one reflection question and one short practice on desire.",
        "Compare Heraclitus and the Daoists on change.",
    ]

    private func bullet(_ text: String) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Text("·").foregroundStyle(Palette.gold).font(.system(size: 16, weight: .bold))
            Text(text)
                .font(.serifBody(15))
                .foregroundStyle(Palette.parchment.opacity(0.9))
                .lineSpacing(3)
        }
    }
}

#Preview {
    AskView().preferredColorScheme(.dark)
}
