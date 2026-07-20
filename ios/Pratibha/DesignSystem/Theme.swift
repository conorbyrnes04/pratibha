import SwiftUI

extension Color {
    init(hex: UInt, alpha: Double = 1) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255,
            opacity: alpha
        )
    }
}

/// Manuscript-pigment palette: gold leaf, vermillion sindoor, lapis ultramarine,
/// lamp-black ink, parchment. Gold is the only accent that "acts."
enum Palette {
    static let ink = Color(hex: 0x0B0A12)
    static let ink2 = Color(hex: 0x100E18)
    static let surface = Color(hex: 0x171320)
    static let gold = Color(hex: 0xE8B84B)
    static let goldHi = Color(hex: 0xF2CE7E)
    static let vermillion = Color(hex: 0xC0563B)
    static let lapis = Color(hex: 0x3A5680)
    static let parchment = Color(hex: 0xF1E7D4)
    static let muted = Color(hex: 0xA99C85)
    static let muted2 = Color(hex: 0x7C7161)

    static let hairline = Color.white.opacity(0.08)
    static let goldLine = Color(hex: 0xF0C979, alpha: 0.18)
}
