import SwiftUI
import SwiftData

/// An inline, in-context reflection tied to a passage. Saved privately on
/// device via SwiftData. Reflection is never a lonely empty tab — it always
/// arrives with a prompt and the passage that occasioned it.
struct ReflectionEditor: View {
    let passageId: String
    let passageTitle: String
    var prompt: String = ""

    @Environment(\.modelContext) private var context
    @Environment(\.dismiss) private var dismiss
    @State private var text = ""
    @FocusState private var focused: Bool

    var body: some View {
        NavigationStack {
            ZStack {
                PratibhaBackground()
                ScrollView {
                    VStack(alignment: .leading, spacing: 16) {
                        Eyebrow(text: "Reflection")
                        Text(passageTitle)
                            .font(.serifDisplay(24))
                            .foregroundStyle(Palette.parchment)

                        if !prompt.isEmpty {
                            Text(prompt)
                                .font(.serifBody(17))
                                .italic()
                                .foregroundStyle(Palette.goldHi)
                                .lineSpacing(4)
                        }

                        GlassCard {
                            TextEditor(text: $text)
                                .focused($focused)
                                .font(.serifBody(17))
                                .foregroundStyle(Palette.parchment)
                                .scrollContentBackground(.hidden)
                                .frame(minHeight: 220)
                                .overlay(alignment: .topLeading) {
                                    if text.isEmpty {
                                        Text("Write freely…")
                                            .font(.serifBody(17))
                                            .foregroundStyle(Palette.muted2)
                                            .padding(.top, 8)
                                            .padding(.leading, 5)
                                            .allowsHitTesting(false)
                                    }
                                }
                        }
                    }
                    .padding(20)
                }
                .scrollContentBackground(.hidden)
            }
            .navigationTitle("")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") { save() }
                        .disabled(text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                        .fontWeight(.semibold)
                }
            }
            .onAppear { focused = true }
        }
    }

    private func save() {
        let trimmed = text.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return }
        context.insert(JournalEntry(
            passageId: passageId,
            passageTitle: passageTitle,
            prompt: prompt,
            text: trimmed
        ))
        dismiss()
    }
}
