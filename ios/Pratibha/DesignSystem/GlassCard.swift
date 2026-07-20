import SwiftUI

/// A translucent reading surface. Uses `.ultraThinMaterial` over the dark
/// ground for a glassy feel that stays legible for long-form text, with a
/// thin gold hairline. Tone tints the fill for semantic surfaces.
struct GlassCard<Content: View>: View {
    enum Tone { case neutral, practice, lapis }

    var tone: Tone = .neutral
    var cornerRadius: CGFloat = 20
    @ViewBuilder var content: Content

    var body: some View {
        content
            .padding(16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background {
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(.ultraThinMaterial)
                    .overlay(
                        RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                            .fill(fillTint)
                    )
            }
            .overlay {
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .strokeBorder(borderColor, lineWidth: 1)
            }
            .shadow(color: .black.opacity(0.28), radius: 18, y: 10)
    }

    private var fillTint: LinearGradient {
        switch tone {
        case .neutral:
            return LinearGradient(
                colors: [Color.white.opacity(0.05), .clear],
                startPoint: .topLeading, endPoint: .bottomTrailing)
        case .practice:
            return LinearGradient(
                colors: [Palette.vermillion.opacity(0.16), Palette.gold.opacity(0.05)],
                startPoint: .topLeading, endPoint: .bottomTrailing)
        case .lapis:
            return LinearGradient(
                colors: [Palette.lapis.opacity(0.22), .clear],
                startPoint: .topLeading, endPoint: .bottomTrailing)
        }
    }

    private var borderColor: Color {
        switch tone {
        case .neutral: return Palette.goldLine
        case .practice: return Palette.vermillion.opacity(0.4)
        case .lapis: return Palette.lapis.opacity(0.5)
        }
    }
}

/// A rounded theme/keyword pill.
struct ThemeChip: View {
    let text: String
    var selected: Bool = false

    var body: some View {
        Text(text)
            .font(.system(size: 13, weight: .medium))
            .foregroundStyle(selected ? Palette.ink : Palette.parchment)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background {
                Capsule().fill(selected
                    ? AnyShapeStyle(LinearGradient(colors: [Palette.goldHi, Palette.gold],
                                                   startPoint: .top, endPoint: .bottom))
                    : AnyShapeStyle(Color.white.opacity(0.05)))
            }
            .overlay {
                Capsule().strokeBorder(selected ? .clear : Palette.hairline, lineWidth: 1)
            }
    }
}
