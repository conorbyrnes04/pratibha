import SwiftUI

/// A contemplative serif for source text and titles (system serif ≈ New York),
/// SF Pro for every control and label.
extension Font {
    static func serifDisplay(_ size: CGFloat) -> Font {
        .system(size: size, weight: .semibold, design: .serif)
    }
    static func serifBody(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight, design: .serif)
    }
}

/// Tracked, uppercase micro-label naming a layer or section.
struct LayerLabel: View {
    let text: String
    var color: Color = Palette.gold

    var body: some View {
        Text(text.uppercased())
            .font(.system(size: 11, weight: .bold))
            .tracking(2)
            .foregroundStyle(color)
            .accessibilityAddTraits(.isHeader)
    }
}

/// Small caps eyebrow used above titles.
struct Eyebrow: View {
    let text: String
    var body: some View {
        Text(text.uppercased())
            .font(.system(size: 12, weight: .bold))
            .tracking(2.2)
            .foregroundStyle(Palette.goldHi)
    }
}
