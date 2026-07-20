import SwiftUI

struct CollectionDetailView: View {
    let collection: CorpusCollection
    @Environment(CorpusStore.self) private var corpus

    var body: some View {
        PratibhaScreen {
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 0) {
                    header
                    ForEach(corpus.passages(in: collection.id)) { passage in
                        NavigationLink(value: passage) {
                            PassageRow(passage: passage, showCollection: false)
                        }
                        .buttonStyle(.plain)
                        Divider().overlay(Palette.hairline)
                    }
                }
                .padding(20)
                .padding(.bottom, 40)
            }
        }
        .navigationTitle(collection.title)
        .navigationBarTitleDisplayMode(.inline)
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            Eyebrow(text: collection.tradition)
            Text(collection.title)
                .font(.serifDisplay(28))
                .foregroundStyle(Palette.parchment)
            Text(collection.blurb)
                .font(.serifBody(16))
                .foregroundStyle(Palette.muted)
                .lineSpacing(3)
            Text("\(collection.count) passages")
                .font(.system(size: 12))
                .foregroundStyle(Palette.muted2)
                .padding(.top, 2)
        }
        .padding(.bottom, 18)
    }
}
