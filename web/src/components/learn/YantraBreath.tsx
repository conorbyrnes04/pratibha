/** Breathing śrīcakra-inspired field — concentric rings, bindu, subtle triangles. */
export function YantraBreath({ className = "" }: { className?: string }) {
  return (
    <svg
      className={`yantra-breath pointer-events-none ${className}`}
      viewBox="0 0 400 400"
      aria-hidden
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <radialGradient id="yantra-bindu-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="rgb(240 201 121)" stopOpacity="0.55" />
          <stop offset="45%" stopColor="rgb(216 168 74)" stopOpacity="0.12" />
          <stop offset="100%" stopColor="rgb(216 168 74)" stopOpacity="0" />
        </radialGradient>
        <radialGradient id="yantra-field-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="rgb(184 91 61)" stopOpacity="0.08" />
          <stop offset="70%" stopColor="rgb(50 72 103)" stopOpacity="0.04" />
          <stop offset="100%" stopColor="transparent" />
        </radialGradient>
      </defs>

      <circle cx="200" cy="200" r="198" fill="url(#yantra-field-glow)" />

      {/* bhūpura — outer square, barely visible */}
      <rect
        x="58"
        y="58"
        width="284"
        height="284"
        fill="none"
        stroke="rgb(240 201 121 / 0.06)"
        strokeWidth="0.75"
        transform="rotate(45 200 200)"
      />

      {/* breathing rings — staggered animation delays */}
      {[168, 142, 116, 90, 64].map((r, i) => (
        <circle
          key={r}
          cx="200"
          cy="200"
          r={r}
          fill="none"
          stroke="rgb(240 201 121 / 0.14)"
          strokeWidth="0.6"
          className="yantra-ring"
          style={{ animationDelay: `${i * 0.7}s` }}
        />
      ))}

      {/* four subtle downward triangles (āvaraṇa hint) */}
      {[0, 90, 180, 270].map((deg) => (
        <polygon
          key={deg}
          points="200,118 168,178 232,178"
          fill="none"
          stroke="rgb(240 201 121 / 0.05)"
          strokeWidth="0.5"
          transform={`rotate(${deg} 200 200)`}
          className="yantra-triangle"
          style={{ animationDelay: `${deg / 90}s` }}
        />
      ))}

      {/* eight lotus petal marks */}
      {Array.from({ length: 8 }, (_, i) => {
        const a = ((i * 45 - 90) * Math.PI) / 180;
        const x = 200 + Math.cos(a) * 152;
        const y = 200 + Math.sin(a) * 152;
        return (
          <ellipse
            key={i}
            cx={x}
            cy={y}
            rx="5"
            ry="2.5"
            fill="rgb(240 201 121 / 0.07)"
            transform={`rotate(${i * 45} ${x} ${y})`}
          />
        );
      })}

      {/* bindu */}
      <circle cx="200" cy="200" r="28" fill="url(#yantra-bindu-glow)" className="yantra-bindu" />
      <circle cx="200" cy="200" r="3.5" fill="rgb(240 201 121 / 0.85)" className="yantra-bindu-core" />
    </svg>
  );
}
