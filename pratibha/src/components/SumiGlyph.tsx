import { sumiUrl, type InkState } from "../lib/sumi";
import "./sumi.css";

// A sumi ink mark, recolored to its ink state by the FastAPI /sumi endpoint and
// painted into a Lynx <image>. `breath` gives the Spanda pulse (cover mark);
// recognized marks carry a faint ember glow on their own.
export function SumiGlyph({
  glyph,
  state = "arising",
  size = 52,
  breath = false,
}: {
  glyph: string;
  state?: InkState;
  size?: number;
  breath?: boolean;
}) {
  const cls = breath ? "sumi-breath" : state === "recognized" ? "sumi-ember" : "";
  return (
    <image
      className={cls}
      src={sumiUrl(glyph, state)}
      style={{
        width: `${size}px`,
        height: `${size}px`,
        // Ash marks sit quietly under the ground; bone/gold read at full strength.
        opacity: state === "unmanifest" ? 0.4 : 1,
      }}
    />
  );
}
