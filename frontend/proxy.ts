import { NextRequest, NextResponse } from "next/server";

const SESSION_COOKIE =
  process.env.SESSION_COOKIE_NAME ?? "adaptive_session";

export function proxy(request: NextRequest) {
  const hasSession = request.cookies.has(SESSION_COOKIE);
  const isAuthRoute =
    request.nextUrl.pathname === "/login" ||
    request.nextUrl.pathname === "/register";

  if (request.nextUrl.pathname.startsWith("/profile") && !hasSession) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  if (isAuthRoute && hasSession) {
    return NextResponse.redirect(new URL("/profile", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/login", "/register", "/profile/:path*"],
};
