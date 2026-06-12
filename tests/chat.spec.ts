import { test, expect } from '@playwright/test';

test.describe('Pruebas del Asistente Virtual - Nexus AI', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/'); // Tomará el baseURL (http://localhost:4321) configurado
  });

  test('Debería abrir y cerrar la ventana del chat correctamente', async ({ page }) => {
    const chatButton = page.locator('#nexus-bot-toggle');
    const chatWindow = page.locator('#nexus-bot-window');

    await expect(chatWindow).toBeHidden();

    await chatButton.click();

    await expect(chatWindow).toBeVisible();

    await chatButton.click();

    await expect(chatWindow).toBeHidden();
  });

  test('Debería enviar un mensaje y recibir respuesta de Nexus AI', async ({ page }) => {
    await page.route('**/api/chat', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          response: '¡Hola! Soy Nexus AI y puedo ayudarte con juegos, keys y soporte de Nexus POS.',
        }),
      });
    });

    const chatButton = page.locator('#nexus-bot-toggle');
    const chatInput = page.locator('#nexus-bot-input');
    const chatMessages = page.locator('#nexus-bot-messages');

    await chatButton.click();

    const mensajeUsuario = 'Hola, ¿tienen juegos de Nintendo?';
    await chatInput.fill(mensajeUsuario);
    await chatInput.press('Enter');

    await expect(chatMessages).toContainText(mensajeUsuario);

    await expect(chatMessages).toContainText('Nexus AI');
    await expect(chatMessages).toContainText('juegos, keys y soporte');
  });
});