import SwiftUI

/// The seven-layer reader — the jewel of the app. Original script first,
/// depth revealed on tap, practice set apart in vermillion, and an inline
/// invitation to reflect.
struct PassageDetailView: View {
    let passage: Passage
    @Environment(CorpusStore.self) private var corpus
    @State private var showReflection = false

    var body: some View {
        PratibhaScreen {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    heading

                    if let quote = passage.pullQuote {
                        Text(quote)
                            .font(.serifBody(20))
                            .italic()
                            .foregroundStyle(Palette.goldHi)
                            .lineSpacing(4)
                            .padding(.vertical, 2)
                    }

                    if passage.hasOriginalScript {
                        GlassCard {
                            layer(label: "Original", color: Palette.gold) {
                                Text(passage.devanagari)
                                    .font(.serifBody(22))
                                    .foregroundStyle(Palette.goldHi)
                                    .lineSpacing(8)
                                    .textSelection(.enabled)
                            }
                        }
                    }

                    if passage.hasTransliteration {
                        GlassCard {
                            layer(label: "Transliteration") {
                                Text(passage.iast)
                                    .font(.serifBody(17))
                                    .italic()
                                    .foregroundStyle(Palette.muted)
                                    .lineSpacing(5)
                                    .textSelection(.enabled)
                            }
                        }
                    }

                    GlassCard {
                        layer(label: passage.isRootText ? "Translation" : "Source") {
                            Text(passage.readingText)
                                .font(.serifBody(19))
                                .foregroundStyle(Palette.parchment)
                                .lineSpacing(6)
                                .textSelection(.enabled)
                        }
                    }

                    if passage.hasCommentary {
                        GlassCard {
                            layer(label: "Commentary") {
                                ExpandableText(text: passage.commentary)
                            }
                        }
                    }

                    if passage.hasPractice {
                        GlassCard(tone: .practice) {
                            layer(label: "Practice · Abhyāsa", color: Palette.vermillion) {
                                Text(passage.practice)
                                    .font(.serifBody(17))
                                    .foregroundStyle(Palette.parchment)
                                    .lineSpacing(5)
                            }
                        }
                    }

                    if !passage.themes.isEmpty {
                        themeChips
                    }

                    Button {
                        showReflection = true
                    } label: {
                        Label("Reflect on this", systemImage: "square.and.pencil")
                    }
                    .buttonStyle(PrimaryButtonStyle())
                    .padding(.top, 4)
                }
                .padding(20)
                .padding(.bottom, 40)
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showReflection) {
            ReflectionEditor(
                passageId: passage.id,
                passageTitle: passage.title,
                prompt: reflectionPrompt
            )
        }
    }

    private var heading: some View {
        VStack(alignment: .leading, spacing: 8) {
            Eyebrow(text: headingEyebrow)
            Text(passage.title)
                .font(.serifDisplay(32))
                .foregroundStyle(Palette.parchment)
                .lineSpacing(2)
        }
    }

    private var themeChips: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(passage.themes, id: \.self) { ThemeChip(text: $0) }
            }
            .padding(.vertical, 2)
        }
    }

    @ViewBuilder
    private func layer<Content: View>(
        label: String,
        color: Color = Palette.gold,
        @ViewBuilder content: () -> Content
    ) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            LayerLabel(text: label, color: color)
            content()
        }
    }

    private var headingEyebrow: String {
        let coll = corpus.collectionTitle(for: passage.workId)
        return passage.unitLabel.isEmpty ? coll : "\(coll) · \(passage.unitLabel)"
    }

    private var reflectionPrompt: String {
        if let theme = passage.themes.first {
            return "Where do you notice \"\(theme)\" in direct experience today?"
        }
        return "What one shift in seeing does this passage invite right now?"
    }
}
