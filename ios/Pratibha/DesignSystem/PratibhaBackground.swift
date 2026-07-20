import SwiftUI

/// The ambient ground: ink gradient with a lapis dawn at top-right and a
/// vermillion warmth at top-left, matching the web identity.
struct PratibhaBackground: View {
    var body: some View {
        ZStack {
            LinearGradient(
                colors: [Color(hex: 0x07070D), Color(hex: 0x100E18), Color(hex: 0x14101A)],
                startPoint: .top,
                endPoint: .bottom
            )
            RadialGradient(
                colors: [Palette.lapis.opacity(0.22), .clear],
                center: UnitPoint(x: 0.85, y: -0.05),
                startRadius: 0,
                endRadius: 540
            )
            RadialGradient(
                colors: [Palette.vermillion.opacity(0.13), .clear],
                center: UnitPoint(x: 0.1, y: 0.02),
                startRadius: 0,
                endRadius: 460
            )
        }
        .ignoresSafeArea()
    }
}

/// Applies the Pratibhā ground behind a scroll view and hides the default
/// system background so the gradient shows through the glass chrome.
struct PratibhaScreen<Content: View>: View {
    @ViewBuilder var content: Content

    var body: some View {
        content
            .background(PratibhaBackground())
            .scrollContentBackground(.hidden)
    }
}
