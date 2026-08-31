import type { SVGProps } from "react";

function BrandIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 24 24"
      width="1em"
      height="1em"
      fill="currentColor"
      aria-hidden="true"
      {...props}
    />
  );
}

export function InstagramIcon() {
  return (
    <BrandIcon>
      <path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm10 2H7a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm-5 3.2A3.8 3.8 0 1 1 8.2 12 3.8 3.8 0 0 1 12 8.2zm0 1.8a2 2 0 1 0 2 2 2 2 0 0 0-2-2zM17.35 6.4a1.15 1.15 0 1 1-1.15 1.15 1.15 1.15 0 0 1 1.15-1.15z" />
    </BrandIcon>
  );
}

export function TikTokIcon() {
  return (
    <BrandIcon>
      <path d="M14.2 3c.4 2.4 1.8 4.1 4.1 4.4v2.4c-1.4 0-2.7-.4-3.9-1.2v6.5c0 3.4-2.6 5.9-6.1 5.9S2.2 18.5 2.2 15.1c0-3.3 2.5-5.8 5.8-5.9v2.5c-1.8.1-3.2 1.6-3.2 3.4 0 1.9 1.5 3.4 3.4 3.4s3.4-1.5 3.4-3.4V3h2.6z" />
    </BrandIcon>
  );
}

export function XIcon() {
  return (
    <BrandIcon>
      <path d="M3 3h4.2l4.7 6.4L16.9 3H21l-7.2 9.2L21.2 21h-4.2l-5.2-7.1L7.1 21H3l7.6-9.7z" />
    </BrandIcon>
  );
}

export function WhatsAppIcon() {
  return (
    <BrandIcon>
      <path d="M12 3.1A8.9 8.9 0 0 0 4.4 16.6L3 21l4.5-1.3A8.9 8.9 0 1 0 12 3.1zm0 16.2a7.2 7.2 0 0 1-3.7-1l-.3-.2-2.7.8.8-2.6-.2-.3a7.2 7.2 0 1 1 6.1 3.3zm4-5.3c-.2-.1-1.3-.6-1.5-.7s-.3-.1-.5.1-.5.7-.7.8-.3.2-.5.1a5.9 5.9 0 0 1-1.7-1.1 6.4 6.4 0 0 1-1.2-1.5c-.1-.2 0-.3.1-.5l.4-.4.1-.3c0-.1 0-.3 0-.4s-.5-1.2-.7-1.6-.4-.4-.5-.4h-.4c-.2 0-.4.1-.6.3a2 2 0 0 0-.6 1.5 3.5 3.5 0 0 0 .7 1.9 8 8 0 0 0 3 3 10 10 0 0 0 1.9.7 3.2 3.2 0 0 0 1.8.1 2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c0-.1-.2-.2-.4-.3z" />
    </BrandIcon>
  );
}

export function SignalIcon() {
  return (
    <BrandIcon>
      <path d="M12 3.2A8.8 8.8 0 0 0 5.4 18.3L4 20.8l2.7-.7A8.8 8.8 0 1 0 12 3.2zm0 1.8a7 7 0 1 1 0 14 7 7 0 0 1 0-14zm0 2.2a4.8 4.8 0 0 0-4.8 4.8h1.8A3 3 0 1 1 12 15.8v1.8A4.8 4.8 0 0 0 12 7.2z" />
    </BrandIcon>
  );
}

export const SHARE_DEST_ICONS = {
  instagram_story: InstagramIcon,
  instagram_post: InstagramIcon,
  tiktok: TikTokIcon,
  x: XIcon,
  whatsapp: WhatsAppIcon,
  signal: SignalIcon,
} as const;
