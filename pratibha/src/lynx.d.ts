// Type declarations for Lynx JSX elements
import { CSSProperties } from "react";

// Extend CSSProperties to include React Native style properties used by Lynx
interface LynxStyle extends CSSProperties {
  paddingVertical?: number | string;
  paddingHorizontal?: number | string;
  marginVertical?: number | string;
  marginHorizontal?: number | string;
  gap?: number | string;
  flex?: number;
  flexDirection?: "row" | "column" | "row-reverse" | "column-reverse";
  justifyContent?: string;
  alignItems?: string;
  alignSelf?: string;
}

interface LynxElementProps {
  style?: LynxStyle;
  onClick?: (e: any) => void;
  children?: React.ReactNode;
  [key: string]: any;
}

interface InputProps extends LynxElementProps {
  value?: string;
  onInput?: (e: any) => void;
  placeholder?: string;
  type?: string;
  multiline?: boolean;
  rows?: number;
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      view: LynxElementProps;
      text: LynxElementProps;
      input: InputProps;
      image: LynxElementProps & { src?: string; alt?: string };
      "scroll-view": LynxElementProps;
    }
  }
}
