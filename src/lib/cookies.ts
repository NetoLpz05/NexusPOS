export type CookieOptions = {
  maxAge?: number;
  secure?: boolean;
  expires?: string;
};

export function isSecureContext() {
  return typeof window !== "undefined" && window.location.protocol === "https:";
}

export function buildCookieOptions({
  maxAge,
  secure = isSecureContext(),
  expires,
}: CookieOptions = {}) {
  const parts = ["path=/", "SameSite=Lax"];

  if (typeof maxAge === "number") {
    parts.push(`max-age=${maxAge}`);
  }

  if (expires) {
    parts.push(`expires=${expires}`);
  }

  if (secure) {
    parts.push("Secure");
  }

  return parts.join("; ");
}

export function buildCookie(
  name: string,
  value: string,
  options: CookieOptions = {},
) {
  const secure = options.secure ?? isSecureContext();

  return [
    `${name}=${encodeURIComponent(value)}`,
    buildCookieOptions({ ...options, secure }),
  ].join("; ");
}

export function buildSessionCookie(
  name: string,
  value: string,
  maxAge: number,
  secure = isSecureContext(),
) {
  return buildCookie(name, value, { maxAge, secure });
}
