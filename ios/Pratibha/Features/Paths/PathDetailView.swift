import SwiftUI

struct PathDetailView: View {
    let path: LearningPath

    var body: some View {
        PratibhaScreen {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    VStack(alignment: .leading, spacing: 10) {
                        Eyebrow(text: "\(path.level) · \(path.estimatedSessions)")
                        Text(path.title)
                            .font(.serifDisplay(30))
                            .foregroundStyle(Palette.parchment)
                        Text(path.focus)
                            .font(.serifBody(17))
                            .foregroundStyle(Palette.goldHi)
                            .lineSpacing(4)
                    }

                    GlassCard {
                        VStack(alignment: .leading, spacing: 10) {
                            LayerLabel(text: "The arc")
                            Text(AttributedString.fromCommentary(path.arc))
                                .font(.serifBody(16))
                                .foregroundStyle(Palette.parchment.opacity(0.92))
                                .lineSpacing(5)
                        }
                    }

                    VStack(alignment: .leading, spacing: 12) {
                        LayerLabel(text: "The gates")
                        ForEach(Array(path.steps.enumerated()), id: \.element.id) { index, step in
                            NavigationLink(value: GateRoute(path: path, index: index)) {
                                GateRow(number: index + 1, step: step)
                            }
                            .buttonStyle(.plain)
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

private struct GateRow: View {
    let number: Int
    let step: PathStep

    var body: some View {
        HStack(alignment: .top, spacing: 14) {
            Text("\(number)")
                .font(.serifDisplay(20))
                .foregroundStyle(Palette.gold)
                .monospacedDigit()
                .frame(width: 30, height: 30)
                .overlay(Circle().strokeBorder(Palette.goldLine, lineWidth: 1))

            VStack(alignment: .leading, spacing: 4) {
                Text(step.title)
                    .font(.serifBody(18, weight: .medium))
                    .foregroundStyle(Palette.parchment)
                Text(step.orientation)
                    .font(.system(size: 13))
                    .foregroundStyle(Palette.muted)
                    .lineLimit(2)
            }
            Spacer(minLength: 0)
        }
        .padding(.vertical, 8)
    }
}
