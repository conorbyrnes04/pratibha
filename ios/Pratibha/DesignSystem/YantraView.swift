import SwiftUI

/// A breathing yantra — concentric rings, interlocking triangles, and a
/// glowing bindu that pulse like a living cakra. Drawn in Canvas and driven by
/// TimelineView; pauses (renders static) when Reduce Motion is on.
struct YantraView: View {
    var size: CGFloat = 150
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 30.0, paused: reduceMotion)) { timeline in
            Canvas { context, canvasSize in
                draw(in: &context, size: canvasSize,
                     t: timeline.date.timeIntervalSinceReferenceDate)
            }
        }
        .frame(width: size, height: size)
        .accessibilityHidden(true)
    }

    private func draw(in context: inout GraphicsContext, size: CGSize, t: TimeInterval) {
        let center = CGPoint(x: size.width / 2, y: size.height / 2)
        let base = min(size.width, size.height) / 2 - 2

        func breath(speed: Double) -> Double { (sin(t * speed) + 1) / 2 } // 0…1

        // Concentric rings
        let rings: [(scale: Double, color: Color, base: Double, speed: Double)] = [
            (0.96, Palette.lapis, 0.45, 0.55),
            (0.72, Palette.gold, 0.5, 0.8),
            (0.5, Palette.vermillion, 0.55, 1.05),
        ]
        for ring in rings {
            let b = breath(speed: ring.speed)
            let r = base * ring.scale * (1 + 0.03 * b)
            let rect = CGRect(x: center.x - r, y: center.y - r, width: r * 2, height: r * 2)
            let opacity = ring.base * (0.55 + 0.45 * b)
            context.stroke(Path(ellipseIn: rect),
                           with: .color(ring.color.opacity(opacity)),
                           lineWidth: 1)
        }

        // Interlocking triangles (Śiva / Śakti)
        let tr = base * 0.62 * (1 + 0.02 * breath(speed: 0.7))
        let up = trianglePath(center: center, radius: tr, pointingUp: true)
        let down = trianglePath(center: center, radius: tr, pointingUp: false)
        let triOpacity = 0.4 + 0.3 * breath(speed: 0.7)
        context.stroke(up, with: .color(Palette.gold.opacity(triOpacity)), lineWidth: 1)
        context.stroke(down, with: .color(Palette.goldHi.opacity(triOpacity)), lineWidth: 1)

        // Bindu glow + core
        let glowR = base * 0.22 * (1 + 0.15 * breath(speed: 1.3))
        context.fill(
            Path(ellipseIn: CGRect(x: center.x - glowR, y: center.y - glowR,
                                   width: glowR * 2, height: glowR * 2)),
            with: .radialGradient(
                Gradient(colors: [Palette.goldHi.opacity(0.55), .clear]),
                center: center, startRadius: 0, endRadius: glowR)
        )
        let coreR = base * 0.05 * (1 + 0.2 * breath(speed: 1.3))
        context.fill(
            Path(ellipseIn: CGRect(x: center.x - coreR, y: center.y - coreR,
                                   width: coreR * 2, height: coreR * 2)),
            with: .color(Palette.goldHi))
    }

    private func trianglePath(center: CGPoint, radius r: Double, pointingUp: Bool) -> Path {
        let dir: Double = pointingUp ? -1 : 1
        let dx = r * 0.87
        let dy = r * 0.5
        var path = Path()
        path.move(to: CGPoint(x: center.x, y: center.y + dir * r))
        path.addLine(to: CGPoint(x: center.x - dx, y: center.y - dir * dy))
        path.addLine(to: CGPoint(x: center.x + dx, y: center.y - dir * dy))
        path.closeSubpath()
        return path
    }
}

#Preview {
    ZStack {
        PratibhaBackground()
        YantraView(size: 220)
    }
}
