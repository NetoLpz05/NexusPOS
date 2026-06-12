import { test, expect } from '@playwright/test';

import { buildCookieOptions, buildSessionCookie } from '../src/lib/cookies';

test.describe('Cookies de sesión', () => {
  test('no usa Secure en localhost/http', () => {
    const options = buildCookieOptions({ maxAge: 60 * 60 * 24 * 7, secure: false });

    expect(options).toContain('SameSite=Lax');
    expect(options).not.toContain('Secure');
  });

  test('añade Secure solo cuando la conexión es https', () => {
    const options = buildCookieOptions({ maxAge: 60 * 60 * 24 * 7, secure: true });

    expect(options).toContain('Secure');
  });

  test('genera una cookie de sesión válida para el navegador', () => {
    const cookie = buildSessionCookie('sb-access-token', 'abc123', 604800, false);

    expect(cookie).toContain('sb-access-token=abc123');
    expect(cookie).toContain('path=/');
    expect(cookie).toContain('max-age=604800');
    expect(cookie).not.toContain('Secure');
  });
});
