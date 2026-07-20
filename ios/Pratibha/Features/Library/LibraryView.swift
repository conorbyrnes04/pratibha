import SwiftUI

/// Browse all passages by collection, by theme, or by free search — everything
/// on device, instant and offline. Flat rows (not nested cards) keep long
/// lists legible on a phone; the glass ground shows through the nav bar.
struct LibraryView: View {
    @Environment(CorpusStore.self) private var corpus
    @State private var query = ""
    @State private var selectedTheme: String?

    var body: some View {
        NavigationStack {
            PratibhaScreen {
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 0) {
                        header

                        if searching {
                            resultsList(corpus.search(query), emptyNote: "No passages match “\(query)”.")
                        } else if let theme = selectedTheme {
                            themedHeader(theme)
                            resultsList(corpus.passages(theme: theme), emptyNote: "")
                        } else {
                            themesRow
                            collectionsList
                        }
                    }
                    .padding(20)
                    .padding(.bottom, 40)
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar(removing: .title)
            .searchable(text: $query, prompt: "Search passages, themes…")
            .navigationDestination(for: Passage.self) { PassageDetailView(passage: $0) }
            .navigationDestination(for: CorpusCollection.self) { CollectionDetailView(collection: $0) }
        }
    }

    private var searching: Bool {
        !query.trimmingCharacters(in: .whitespaces).isEmpty
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Eyebrow(text: "The corpus")
            Text("Library")
                .font(.serifDisplay(32))
                .foregroundStyle(Palette.parchment)
            Text("\(corpus.passages.count) passages across \(corpus.collections.count) traditions.")
                .font(.serifBody(16))
                .foregroundStyle(Palette.muted)
        }
        .padding(.bottom, 18)
    }

    private var themesRow: some View {
        VStack(alignment: .leading, spacing: 10) {
            LayerLabel(text: "Themes")
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(corpus.popularThemes.prefix(14), id: \.self) { theme in
                        Button {
                            withAnimation(.easeInOut(duration: 0.2)) { selectedTheme = theme }
                        } label: { ThemeChip(text: theme) }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.vertical, 2)
            }
        }
        .padding(.bottom, 22)
    }

    private var collectionsList: some View {
        VStack(alignment: .leading, spacing: 0) {
            LayerLabel(text: "Collections")
                .padding(.bottom, 8)
            ForEach(corpus.collections) { collection in
                NavigationLink(value: collection) {
                    CollectionRow(collection: collection)
                }
                .buttonStyle(.plain)
                Divider().overlay(Palette.hairline)
            }
        }
    }

    private func themedHeader(_ theme: String) -> some View {
        HStack {
            LayerLabel(text: "Theme · \(theme)")
            Spacer()
            Button("Clear") {
                withAnimation(.easeInOut(duration: 0.2)) { selectedTheme = nil }
            }
            .font(.system(size: 13, weight: .semibold))
            .foregroundStyle(Palette.goldHi)
        }
        .padding(.bottom, 8)
    }

    private func resultsList(_ passages: [Passage], emptyNote: String) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            if passages.isEmpty {
                Text(emptyNote)
                    .font(.serifBody(16))
                    .foregroundStyle(Palette.muted)
                    .padding(.top, 8)
            } else {
                ForEach(passages) { passage in
                    NavigationLink(value: passage) {
                        PassageRow(passage: passage)
                    }
                    .buttonStyle(.plain)
                    Divider().overlay(Palette.hairline)
                }
            }
        }
    }
}

private struct CollectionRow: View {
    let collection: CorpusCollection

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            VStack(alignment: .leading, spacing: 5) {
                Text(collection.title)
                    .font(.serifBody(19, weight: .medium))
                    .foregroundStyle(Palette.parchment)
                Text(collection.tradition)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundStyle(Palette.gold.opacity(0.85))
                Text(collection.blurb)
                    .font(.serifBody(14))
                    .foregroundStyle(Palette.muted)
                    .lineLimit(2)
            }
            Spacer(minLength: 8)
            VStack(spacing: 2) {
                Text("\(collection.count)")
                    .font(.system(size: 15, weight: .semibold))
                    .monospacedDigit()
                    .foregroundStyle(Palette.goldHi)
                Image(systemName: "chevron.right")
                    .font(.system(size: 11, weight: .semibold))
                    .foregroundStyle(Palette.muted2)
            }
        }
        .padding(.vertical, 12)
        .contentShape(Rectangle())
    }
}
